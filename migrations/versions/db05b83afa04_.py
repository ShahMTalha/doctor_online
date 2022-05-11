"""empty message

Revision ID: db05b83afa04
Revises: 27b7e6ef58d1
Create Date: 2022-05-11 11:01:40.992460

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'db05b83afa04'
down_revision = '27b7e6ef58d1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('created_at', sa.DateTime(), nullable=False))
    op.add_column('users', sa.Column('modified_at', sa.DateTime(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'modified_at')
    op.drop_column('users', 'created_at')
    # ### end Alembic commands ###