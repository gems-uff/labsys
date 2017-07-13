"""empty message

Revision ID: 15741cc426db
Revises: 0bab97a3cbf1
Create Date: 2017-07-13 15:51:17.524617

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '15741cc426db'
down_revision = '0bab97a3cbf1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('countries',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name_en_us', sa.String(length=255), nullable=True),
    sa.Column('name_pt_br', sa.String(length=255), nullable=True),
    sa.Column('abbreviation', sa.String(length=2), nullable=True),
    sa.Column('bacen_code', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('regions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('country_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=16), nullable=True),
    sa.Column('region_code', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['country_id'], ['countries.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('states',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('region_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('uf_code', sa.String(length=2), nullable=True),
    sa.Column('ibge_code', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['region_id'], ['regions.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('cities',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('state_id', sa.Integer(), nullable=True),
    sa.Column('ibge_code', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.ForeignKeyConstraint(['state_id'], ['states.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('addresses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('patient_id', sa.Integer(), nullable=True),
    sa.Column('country_id', sa.Integer(), nullable=True),
    sa.Column('state_id', sa.Integer(), nullable=True),
    sa.Column('city_id', sa.Integer(), nullable=True),
    sa.Column('neighborhood', sa.String(length=255), nullable=True),
    sa.Column('details', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['city_id'], ['cities.id'], ),
    sa.ForeignKeyConstraint(['country_id'], ['countries.id'], ),
    sa.ForeignKeyConstraint(['patient_id'], ['patients.id'], ),
    sa.ForeignKeyConstraint(['state_id'], ['states.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('addresses')
    op.drop_table('cities')
    op.drop_table('states')
    op.drop_table('regions')
    op.drop_table('countries')
    # ### end Alembic commands ###
