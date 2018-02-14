"""empty message

Revision ID: 395bc1dcdefb
Revises: df33f3613823
Create Date: 2017-07-14 11:50:16.234145

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '395bc1dcdefb'
down_revision = 'df33f3613823'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('admissions', sa.Column('city_id', sa.Integer(), nullable=True))
    op.add_column('admissions', sa.Column('details', sa.String(length=255), nullable=True))
    op.add_column('admissions', sa.Column('health_unit', sa.String(length=128), nullable=True))
    op.add_column('admissions', sa.Column('requesting_institution', sa.String(length=128), nullable=True))
    op.add_column('admissions', sa.Column('state_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'admissions', 'cities', ['city_id'], ['id'])
    op.create_foreign_key(None, 'admissions', 'states', ['state_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'admissions', type_='foreignkey')
    op.drop_constraint(None, 'admissions', type_='foreignkey')
    op.drop_column('admissions', 'state_id')
    op.drop_column('admissions', 'requesting_institution')
    op.drop_column('admissions', 'health_unit')
    op.drop_column('admissions', 'details')
    op.drop_column('admissions', 'city_id')
    # ### end Alembic commands ###