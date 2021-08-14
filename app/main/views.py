from flask import current_app, render_template, request, session, redirect, url_for, \
    flash, abort, make_response
from flask_login import login_required, current_user

from . import main
from ..models import User
from .forms import EditProfileForm, PostForm, ModifyForm, CommentForm, DeletePostForm
from ..models import Permission, Post, Comment

from app import db
from app.decorators import permission_required
from app import moment


@main.app_context_processor
def context():
    return dict(Permission=Permission, redirect=redirect)


@main.route('/', methods=['GET'])
def index():
    if current_user.is_authenticated:
        return render_template('welcome.html')
    return render_template('index.html')


@main.route('/community', methods=['GET', 'POST'])
def community():
    form = PostForm(request.form)
    if request.method =='POST' and current_user.can(Permission.WRITE_ARTICLES) and form.validate():
        post = Post(body=form.body.data, author=current_user._get_current_object())
        db.session.add(post)
        flash('成功评论', 'info')
        return redirect(url_for('.community'))
    page = request.args.get('page', 1, type=int)  # 获取模板里的page参数,及会出现在路由里的page=?
    show_followed = False
    if current_user.is_authenticated:
        show_followed = bool(request.cookies.get('show_followed', ''))
    if show_followed:
        query = current_user.followed_posts
    else:
        query = Post.query
    pagination = query.order_by(Post.timestamp.desc()).paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
    posts = pagination.items
    return render_template('community.html', form=form, posts=posts, pagination=pagination, show_followed=show_followed)


@main.route('/all')
@login_required
def show_all():
    resp = make_response(redirect(url_for('main.community')))
    resp.set_cookie('show_followed', '', max_age=30*24*60*60)
    return resp


@main.route('/followed')
@login_required
def show_followed():
    resp = make_response(redirect(url_for('main.community')))
    resp.set_cookie('show_followed', '1',  max_age=30*24*60*60)
    return resp


@main.route('/about_us', methods=['GET'])
def about_us():
    return render_template("about_us.html")


@main.route('/user/<int:user_id>', methods=['GET'])
def _user(user_id):
    # 避免视图函数名字和蓝本名字冲突
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        abort(400)
    posts = user.posts.order_by(Post.timestamp.desc()).all()
    return render_template('user.html', user=user, posts=posts)


@main.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(request.form)
    # 修改资料不规范时，应把以前的资料填充到显示页面
    if request.method == 'POST' and form.validate():
        # 提交表单到数据库会话
        current_user.username = form.username.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash('你的资料已更新~', 'success')
        return redirect(url_for('main._user', user_id=current_user.id))
    form.username.data = current_user.username
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)


@main.route('post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def post(post_id):
    # 用于显示post，及其comment
    _post = Post.query.get_or_404(post_id)
    form = CommentForm(request.form)
    if request.method == 'POST' and form.validate():
        # 有人想在这篇post评论
        comment = Comment(body=form.body.data, post=_post, author=current_user._get_current_object())
        db.session.add(comment)
        flash('你的评论已发布', 'success')
        return redirect(url_for('main.post', post_id=_post.id, page=-1))
    page = request.args.get('page', 1, type=int)  # 无设置时默认导航到page=1
    if page == -1:
        # 导航到最后一页
        # 设置一位偏移位再做除法
        page = ((_post.comments.count() -1) / current_app.config['FLASKY_COMMENTS_PER_PAGE']) + 1
    pagination = _post.comments.order_by(Comment.timestamp.asc()).paginate(page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'], error_out=False)
    comments = pagination.items
    return render_template('post.html', posts=[_post], form=form, comments=comments, pagination=pagination)


@main.route('edit_post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    pass


@main.route('delete_post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    form = DeletePostForm(request.form)
    if not form.validate():
        flash('未定义的行为','danger')
        redirect(url_for('main.index'))
    else:
        post = Post.query.filter_by(id=post_id).first()
        if post is None:
            flash('无效的删除！', 'danger')
            return redirect(url_for('main.community'))
        else:
            db.session.delete(post)
            db.session.commit()
            flash('留言已删除','warning')
            return redirect(url_for('main.community'))


@main.route('delete/post-comment/<int:comment_id>', methods=['GET'])
def delete_comment(comment_id):
    comment_to_del = Comment.query.get_or_404(comment_id)
    form = CommentForm(request.form)
    post = Post.query.filter_by(id=comment_to_del.post_id).first()
    db.session.delete(comment_to_del)
    db.session.commit()
    flash('已删除该评论','warning')
    return redirect(url_for('main.post', post_id=post.id))


@main.route('/modify_user_info/<user_id>', methods=['GET', 'POST'])
@login_required
def modify_user_info(user_id):
    _user = User.query.filter_by(id=user_id).first()  # 不要漏写first()
    form = ModifyForm(request.form)
    if _user and request.method == 'POST' and form.validate():
        _user.username = form.username.data
        _user.email = form.email.data
        db.session.add(_user)
        flash('更改档案成功', 'success')
        return redirect(url_for('main.community'))
    else:
        form.email.data = _user.email
        form.username.data = _user.username
        return render_template('modify_user_info.html', form=form, user=_user)


@main.route('follow/<int:user_id>', methods=['GET'])
@login_required
def follow(user_id):
    # 确保在用户登录后操作
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        flash('无效的用户！', 'danger')
        return redirect('main.index')
    if current_user.is_following(user):
        flash('你已关注该用户', 'warning')
        return redirect(url_for('main._user', user_id=user_id))
    # 用在模型中已创建好的函数实现关注
    current_user.follow(user)
    flash('你现在正在关注%s。' % user.username)
    return redirect(url_for('main._user', user_id=user_id))


@main.route('unfollow/<int:user_id>',methods=['GET'])
@login_required
def unfollow(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        flash('无效的用户', 'danger')
        return redirect('main.index')
    if not current_user.is_following(user):
        flash('未关注该用户！', 'danger')
        return redirect(url_for('main._user', user_id=user_id))
    current_user.unfollow(user)
    flash('你已取消关注%s' % user.username, 'warning')
    return redirect(url_for('main._user', user_id=user_id))


@main.route('followers/<int:user_id>')
def followers(user_id):
    # 找到要显示用户的粉丝
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        flash('无效的用户！', 'danger')
        return redirect(url_for('main.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followers.paginate(
        page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
        error_out=False)
    # 使用列表推导式创建列表，这样每个列表元素都是字典
    follows = [{'user': item.follower, 'timestamp': item.timestamp} for item in pagination.items]
    if user == current_user:
        title = '关注我的'
    else:
        title = '关注%s的人' % user.username
    return render_template('followers.html', title=title, user=user, follows=follows)


@main.route('followed_by/<int:user_id>')
def followed_by(user_id):
    # 找到要用户的关注
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        flash('无效的用户！', 'danger')
        return redirect(url_for('main.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followed.paginate(
        page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
        error_out=False)
    # 使用列表推导式创建列表，这样每个列表元素都是字典。
    # 分页对象里的每一个都是一个User，但是为了区分加以理解，创建一个字典为follows
    follows = [{'user': item.followed, 'timestamp': item.timestamp} for item in pagination.items]
    return render_template('followers.html', title='%s的关注' % user.username, user=user, follows=follows)


@main.route('moderate')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate():
    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.order_by(Comment.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'], error_out=False)
    comments = pagination.items
    return render_template('moderate_comments.html', comments=comments,pagination=pagination, page=page)







