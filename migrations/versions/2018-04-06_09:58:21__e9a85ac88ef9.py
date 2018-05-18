"""empty message

Revision ID: e9a85ac88ef9
Revises: 54b4204d4560
Create Date: 2018-04-06 09:58:21.356537

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e9a85ac88ef9'
down_revision = '54b4204d4560'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('clinical_evolutions', sa.Column('occurred', sa.Boolean(), nullable=True))
    op.drop_column('clinical_evolutions', 'death')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('clinical_evolutions', sa.Column('death', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.drop_column('clinical_evolutions', 'occurred')
    # ### end Alembic commands ###
