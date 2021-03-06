from flask import url_for, jsonify, request, g, request, current_app

from app.api_1_0.authentication import http_auth
from app.api_1_0 import api
from app.models import Post, Permission
from app import db

from .decorators import permission_required
from .errors import forbidden


@api.route('/posts/', methods=['POST'])
@permission_required(Permission.WRITE_ARTICLES)
def new_post():
    post = Post.from_json(request.json)
    post.author = g.current_user
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_json(), 201, \
                   {'loacation': url_for('api.get_post', id=post.id, _external=True)})


"""
    处理文章资源端点
"""


@api.route('/posts')
@http_auth.login_required
def get_posts():
    page = request.args.get('page',1,type=int)
    pagination = Post.query.paginate(
        page, per_page=current_app.config['FLASK_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    if pagination.has_prev:
        prev = url_for('api.get_posts',page=page-1, _external=True)
    if pagination.has_next:
        next = url_for('api.get_posts', page=page - 1, _external=True)
    return jsonify({'posts': [post.to_json() for post in posts],
                    'prev': prev,
                    'next': next,
                    'count': pagination.total
    })


@api.route('/posts/<int:id>')
@http_auth.login_required
def get_post(id):
    post = Post.query.get_or_404(id)
    return jsonify(post.to_json())


@api.route('/posts/<int:id>', methods=['PUT'])
@permission_required(Permission.WRITE_ARTICLES)
def edit_post(id):
    post = Post.query.get_or_404(id)
    if g.current_user != post.author and \
            not g.current_user.can(Permission.ADMINISTER):
        return forbidden('Insufficient permission')
    post.body = request.json.get('body', post.body)  # 防止意外，默认设为之前的body
    db.session.add(post)
    return jsonify(post.to_json)


