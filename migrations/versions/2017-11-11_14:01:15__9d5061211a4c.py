"""empty message

Revision ID: 9d5061211a4c
Revises: 1e457e3de2d2
Create Date: 2017-11-11 14:01:15.095173

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9d5061211a4c'
down_revision = '1e457e3de2d2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('stock_products', 'amount',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('stock_products', 'amount',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
