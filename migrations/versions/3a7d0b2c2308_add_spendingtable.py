"""add spendingTable

Revision ID: 3a7d0b2c2308
Revises: 94b1a7ae3b85
Create Date: 2021-08-20 15:29:53.837455

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3a7d0b2c2308'
down_revision = '94b1a7ae3b85'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('spendingrecords',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('img', sa.LargeBinary(), nullable=True),
    sa.Column('title', sa.String(length=15), nullable=False),
    sa.Column('costs', sa.Float(precision=2), nullable=False),
    sa.Column('description', sa.String(length=40), nullable=True),
    sa.Column('tag', sa.SmallInteger(), nullable=False),
    sa.Column('recordTimestamp', sa.DateTime(), nullable=False),
    sa.Column('createTimestamp', sa.DateTime(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('public', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_spendingrecords_user_id_users')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_spendingrecords'))
    )
    with op.batch_alter_table('spendingrecords', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_spendingrecords_createTimestamp'), ['createTimestamp'], unique=False)
        batch_op.create_index(batch_op.f('ix_spendingrecords_recordTimestamp'), ['recordTimestamp'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('spendingrecords', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_spendingrecords_recordTimestamp'))
        batch_op.drop_index(batch_op.f('ix_spendingrecords_createTimestamp'))

    op.drop_table('spendingrecords')
    # ### end Alembic commands ###
