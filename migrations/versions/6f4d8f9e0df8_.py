"""empty message

Revision ID: 6f4d8f9e0df8
Revises: db05b83afa04
Create Date: 2022-05-11 11:56:11.491900

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6f4d8f9e0df8'
down_revision = 'db05b83afa04'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('doctor_details',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('age', sa.Integer(), nullable=False),
    sa.Column('qualification', sa.String(), nullable=False),
    sa.Column('serving', sa.String(), nullable=False),
    sa.Column('experience', sa.Integer(), nullable=True),
    sa.Column('specialized', sa.String(), nullable=False),
    sa.Column('serving_type', sa.String(length=10), nullable=False),
    sa.Column('verified', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('modified_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('doctor_details')
    # ### end Alembic commands ###