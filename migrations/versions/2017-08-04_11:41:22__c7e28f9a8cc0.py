"""empty message

Revision ID: c7e28f9a8cc0
Revises: a8c16ba8ac4a
Create Date: 2017-08-04 11:41:22.528875

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c7e28f9a8cc0'
down_revision = 'a8c16ba8ac4a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('products', 'amount')
    op.add_column('transactions', sa.Column('allotment', sa.String(length=64), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('transactions', 'allotment')
    op.add_column('products', sa.Column('amount', sa.INTEGER(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###