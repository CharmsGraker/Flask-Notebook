from flask import render_template, request, session, flash, redirect, url_for, abort, jsonify
from flask_login import login_user, current_user,login_required
import time
from ..models import Article, User
from app import db
from .forms import ArticleForm, DeleteArticleForm
from . import notes


@notes.route('/', methods=['GET'])
@login_required
def dashboard():
    form = DeleteArticleForm()
    notes = Article.query.filter_by(user_id=current_user.id).all()
    session['username'] = current_user.username
    if notes:
        return render_template('searchPage.html', articles=notes, form=form, user=current_user)
    else:
        msg = '暂无笔记信息'
        return render_template('searchPage.html', msg=msg, form=form, user=current_user)


@notes.route('/add_article', methods=['GET', 'POST'])
@login_required
def add_article():
    form = ArticleForm(request.form)
    if request.method == 'POST' and form.validate():
        article = Article(title=form.title.data, content=form.content.data, user_id=current_user.id,
                          create_date=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        db.session.add(article)
        db.session.commit()
        flash('笔记创建成功', 'success')
        return redirect(url_for('.dashboard'))
    return render_template('add_article.html', form=form)


@notes.route('edit_article/<int:article_id>', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    article = Article.query.filter_by(id=article_id).first()
    if not article:
        flash('文章不存在', 'warning')
        return redirect(url_for('.dashboard'))
    else:
        form = ArticleForm(request.form)
        if request.method == 'POST' and form.validate():
            article.title = form.title.data
            article.content = form.content.data
            article.create_date = form.create_date.data
            db.session.add(article)
            flash('笔记更改成功', 'success')
            return redirect(url_for('.dashboard'))
        else:
            # 不是有效的字段更改
            form.title.data = article.title
            form.content.data = article.content
            return render_template('edit_article.html', form=form)


@notes.route('/view_article/<article_id>')
@login_required
def view_article(article_id):
    one_note = Article.query.filter_by(id=article_id).first()
    return render_template('view_article.html', article=one_note)


@notes.route('/delete_article/<int:article_id>', methods=['POST'])
@login_required
def delete_article(article_id):
    # 为了安全，防止XXS攻击，需要给删除文章做一个表单
    to_del = Article.query.filter_by(id=article_id).first()
    if not to_del:
        flash('文章不存在，你无权操作！', 'danger')
    else:
        form = DeleteArticleForm(request.form)
        if request.method == 'POST' and form.validate():
            db.session.delete(to_del)
            db.session.commit()
            flash('笔记删除成功', 'warning')
        else:
            abort(400)
    return redirect(url_for('.dashboard'))


@notes.route('/my_post/<int:user_id>')
@login_required
def my_post(user_id):
    user = User.query.filter_by(id=user_id).first()
    myposts = user.posts.all()
    return render_template('my_post.html', user=user, posts=myposts)


@notes.route('/livesearch', methods=['GET', 'POST'])
@login_required
def livesearch():
    keywords = request.form.get("text")
    if keywords:
        articles = Article.query.filter(Article.title.like('%{}%'.format(keywords))).all()
    else:
        articles = []
    # articles = Article.query.all()
    results = []
    for article in articles:
        results.append(article.to_json())
    # print('aaaaaaaaaaa',result)
    return jsonify(results)

