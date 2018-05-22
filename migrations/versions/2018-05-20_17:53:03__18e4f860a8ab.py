"""empty message

Revision ID: 18e4f860a8ab
Revises: bc16fb9c58a1
Create Date: 2018-05-20 17:53:03.011579

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '18e4f860a8ab'
down_revision = 'bc16fb9c58a1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('cdc_exam', 'dominant_ct',
               existing_type=sa.INTEGER(),
               type_=sa.Numeric(precision=7, scale=2),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('cdc_exam', 'dominant_ct',
               existing_type=sa.Numeric(precision=7, scale=2),
               type_=sa.INTEGER(),
               existing_nullable=True)
    # ### end Alembic commands ###
