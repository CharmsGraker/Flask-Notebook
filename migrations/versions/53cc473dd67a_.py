"""empty message

Revision ID: 53cc473dd67a
Revises: 7e52b531ff6b
Create Date: 2021-04-14 00:30:27.044472

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '53cc473dd67a'
down_revision = '7e52b531ff6b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('articles', 'create_time')
    op.add_column('roles', sa.Column('default', sa.Boolean(), nullable=True))
    op.add_column('roles', sa.Column('permissions', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_roles_default'), 'roles', ['default'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_roles_default'), table_name='roles')
    op.drop_column('roles', 'permissions')
    op.drop_column('roles', 'default')
    op.add_column('articles', sa.Column('create_time', sa.VARCHAR(length=65), nullable=True))
    # ### end Alembic commands ###
