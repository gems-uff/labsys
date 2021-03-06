"""empty message

Revision ID: 3d2fba07fd93
Revises: b0c3d09f90a3
Create Date: 2018-05-15 17:31:22.162734

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3d2fba07fd93'
down_revision = 'b0c3d09f90a3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('admissions', sa.Column('secondary_risk_factors', sa.String(length=512), nullable=True))
    op.drop_column('risk_factors', 'primary')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('risk_factors', sa.Column('primary', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.drop_column('admissions', 'secondary_risk_factors')
    # ### end Alembic commands ###
