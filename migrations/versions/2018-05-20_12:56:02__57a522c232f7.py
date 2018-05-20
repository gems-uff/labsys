"""empty message

Revision ID: 57a522c232f7
Revises: e9b7f5b6ec33
Create Date: 2018-05-20 12:56:02.228084

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '57a522c232f7'
down_revision = 'e9b7f5b6ec33'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('transactions', sa.Column('patched_transaction_id', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('transactions', 'patched_transaction_id')
    # ### end Alembic commands ###
