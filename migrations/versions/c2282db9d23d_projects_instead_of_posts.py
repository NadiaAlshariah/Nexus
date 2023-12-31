"""projects instead of posts

Revision ID: c2282db9d23d
Revises: 96cfd25c0908
Create Date: 2023-10-08 11:33:15.645016

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c2282db9d23d'
down_revision = '96cfd25c0908'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('title', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('description', sa.String(length=10000), nullable=True))
        batch_op.add_column(sa.Column('start_date', sa.Date(), nullable=True))
        batch_op.add_column(sa.Column('end_date', sa.Date(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.drop_column('end_date')
        batch_op.drop_column('start_date')
        batch_op.drop_column('description')
        batch_op.drop_column('title')

    # ### end Alembic commands ###
