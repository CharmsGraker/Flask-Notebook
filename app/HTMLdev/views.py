import os
import uuid

from flask import current_app, render_template, request, session, redirect, url_for, \
    flash, abort, make_response, jsonify, send_from_directory
from flask_login import current_user


import cv2

from . import dev
from .forms import UploadImgForm
from .. import db
from ..models import Article


@dev.route('/t', methods=['GET'])
def testview():
    return render_template('searchPage.html')


@dev.route('/livesearch', methods=['GET', 'POST'])
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


@dev.route('/upload', methods=['GET'])
def upload():
    return render_template('uploader.html')


@dev.route('/upload_image', methods=['GET', 'POST'])
def upload_image():
    """
    处理上传文件请求
    :return:
    """
    form = UploadImgForm(request.form)
    if request.method == 'POST':
        # 如果文件格式及大小符合要求，处理上传请求
        if request.files:
            fileStorageInstance = request.files['file']
            # f = form.image.data
            filename = fileStorageInstance.filename
            # print(file_size)
            # file_bytes = fileStorageInstance.read()
            # file_size = len(file_bytes)
            if not allowed_file(filename):
                flash('请检查文件格式或大小后重试', 'warn')
                return redirect(request.url)
            else:
                # 确保文件名安全，不危害服务器
                new_filename = reNameFileByRandomly(filename)
                    # qualified_image = UploadImage()
                    # qualified_image.filename = filename
                    # qualified_image.image = f
                    # qualified_image.owner = current_user
                    #
                    # db.session.add(qualified_image)
                    # db.session.commit()
                fpath = os.path.join(current_app.config['UPLOAD_IMAGE_SAVE_DIR'], new_filename)
                fileStorageInstance.save(fpath)
                flash('上传图片成功', 'success')
                return render_template('uploader.html', form=form)

        else:
            flash('不能上传空文件！')
            return render_template('uploader.html', form=form)
    else:
        # 不是POST，直接重新渲染表单
        return render_template('uploader.html', form=form)


@dev.route('/get_file/<path:filename>')
def get_file(filename):
    """
    返回用户上传的文件，让用户可以查看
    :param filename:
    :return:
    """
    # 使用send_from_directory生成下载连接
    return send_from_directory(current_app.config['UPLOAD_IMAGE_SAVE_DIR'], filename)

@dev.route('/')
def devindex():
    return render_template('new_index.html')

def allowed_file(filename):
    """
    检查文件是否符合规范
    :param file:
    :return:
    """
    filesize = int(request.cookies.get("filesize"))
    print(filesize)
    return check_file_extension(filename) and check_file_size(filesize)


def check_file_extension(filename):
    ext = os.path.splitext(filename)[1]
    return ext.lower() in current_app.config['ALLOWED_IMAGED_EXT']


def check_file_size(filesize):
    return current_app.config['ALLOWED_MAX_IMG_SIZE'] >= filesize


def reNameFileByRandomly(filename):
    """
    为防止恶意用户注入路径，重命名文件
    :param filename:
    :return:
    """
    # 获取扩展格式
    print(filename)
    file_extension = os.path.splitext(filename)[1]
    new_filename = uuid.uuid4().hex + file_extension
    return new_filename


@dev.route('/topic')
def topic():
    return render_template('topicTemplate.html', user=current_user)


@dev.route('/note_ui')
def note():
    return render_template('dashboard_ui.html')
