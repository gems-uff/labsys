"""empty message

Revision ID: 11793d6ece12
Revises: 395bc1dcdefb
Create Date: 2017-07-14 12:31:33.522124

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '11793d6ece12'
down_revision = '395bc1dcdefb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('addresses', sa.Column('zone', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('addresses', 'zone')
    # ### end Alembic commands ###