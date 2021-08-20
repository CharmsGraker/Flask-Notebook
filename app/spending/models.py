from datetime import datetime

from app import db


class SpendingRecord(db.Model):
    __tablename__ = 'spendingrecords'
    id = db.Column(db.Integer, primary_key=True)
    # 头图
    img = db.Column(db.LargeBinary)

    title = db.Column(db.String(15), nullable=False)
    costs = db.Column(db.Float(precision=2), nullable=False)
    # 介绍
    description = db.Column(db.String(40), nullable=True)
    tag = db.Column(db.SmallInteger, nullable=False)

    recordTimestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow(), nullable=False)
    createTimestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow(), nullable=False)
    # link_ref = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # 是否公众可见
    public = db.Column(db.Boolean, default=False)
