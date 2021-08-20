from flask import render_template, request, flash, redirect, url_for, current_app
from flask_login import current_user

from . import community

# @community.route('/page', default={'page_idx': 1})
# @community.route('/page/<int:page_idx>', methods=['GET'])
# def pool(page_idx):
#      return render_template('index.html')
from .forms import PostForm
from .. import db
from ..models import Article, Permission, Post
from ..notes.forms import ArticleForm


@community.route('/', methods=['GET', 'POST'])
def pool():
    form = PostForm(request.form)
    if request.method == 'POST' and current_user.can(Permission.WRITE_ARTICLES) and form.validate():
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
    pagination = query.order_by(Post.timestamp.desc()).paginate(page,
                                                                per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
                                                                error_out=False)
    posts = pagination.items
    return render_template('topicTemplate.html', user=current_user,topic=None, pagination=pagination)
