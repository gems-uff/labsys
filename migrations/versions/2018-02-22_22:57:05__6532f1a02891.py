"""empty message

Revision ID: 6532f1a02891
Revises: f5234f5f739c
Create Date: 2018-02-22 22:57:05.072746

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6532f1a02891'
down_revision = 'f5234f5f739c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order_items', sa.Column('added_to_stock', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('order_items', 'added_to_stock')
    # ### end Alembic commands ###
