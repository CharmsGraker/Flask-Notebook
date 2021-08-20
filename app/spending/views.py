import os
import pickle

import cv2
from flask import render_template, request, flash, redirect, url_for, g, current_app
from flask_login import current_user, login_required

import app
from . import spending
from .forms import SpendingRecordForm
from .labelHash import LabelProjection
from .models import SpendingRecord

from sqlalchemy import func

from app import db


def render_SpendingData():
    pass


@spending.route('/', methods=['GET'])
@login_required
def index():
    form = SpendingRecordForm(request.form)
    show_list = None
    hasher = g.label_hash
    labelProjection = hasher.getInt2StrHashTable()

    print('hash', labelProjection)
    render_SpendingData()
    return render_template('spendingTemplate.html', form=form,
                           user=current_user,
                           label=labelProjection)


@spending.route('/insert', methods=['GET', 'POST'])
@login_required
def insertRecord():
    form = SpendingRecordForm(request.form)
    print(form)
    if request.method == 'POST' and form.validate():
        # 就是时间出问题了
        # 用户未上传头图，默认按类别生成一个头图
        if form.banner_image.data is None:
            Hasher = g.label_hash
            form.banner_image.data = Hasher.getDefaultBanner(label=form.spending_tag.data)

        # 对时间安全转换?
        sp_record = SpendingRecord(img=form.banner_image.data,
                                   title=form.title.data,
                                   tag=form.spending_tag.data,
                                   costs=form.costs.data,
                                   description=form.description.data,
                                   recordTimestamp=form.spending_record_date.data,
                                   public=form.public.data,
                                   user_id=current_user.id)

        print(form.spending_record_date.data)
        # db.session.add(sp_record)
        # db.session.commit()
        flash('已新增一条记账，快去看看吧', 'success')
        return redirect(url_for('spending.index'))
    return render_template('insertSpending.html', form=form)


@spending.route('/update/<int:id>')
def updateRecord(id):
    pass


@spending.route('/delete/<int:id>')
def DeleteRecord(id):
    pass


@spending.before_request
def before_bp_request():
    print('load-----------------------')
    config_path = current_app.config['SPENDING_LABEL_HASH_DIR']
    g.label_hash = LabelProjection(path_prefix=config_path)
