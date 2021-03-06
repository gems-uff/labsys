"""empty message

Revision ID: 032d311ba5f9
Revises: 3d2fba07fd93
Create Date: 2018-05-16 16:43:39.625749

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '032d311ba5f9'
down_revision = '3d2fba07fd93'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('antiviral',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('usage', sa.String(length=255), nullable=True),
    sa.Column('other', sa.String(length=255), nullable=True),
    sa.Column('start_date', sa.Date(), nullable=True),
    sa.Column('admission_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['admission_id'], ['admissions.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('antiviral')
    # ### end Alembic commands ###
