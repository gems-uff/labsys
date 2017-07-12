"""empty message

Revision ID: 77adb3584ff6
Revises: 
Create Date: 2017-07-12 13:19:44.961040

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '77adb3584ff6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('methods',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('primary', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('patients',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('symptoms',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('primary', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('admissions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_lvrs_intern', sa.String(length=32), nullable=True),
    sa.Column('patient_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['patient_id'], ['patients.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id_lvrs_intern')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_table('observed_symptoms',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('observed', sa.Boolean(), nullable=True),
    sa.Column('details', sa.String(length=255), nullable=True),
    sa.Column('symptom_id', sa.Integer(), nullable=True),
    sa.Column('admission_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['admission_id'], ['admissions.id'], ),
    sa.ForeignKeyConstraint(['symptom_id'], ['symptoms.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('samples',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('collection_date', sa.Date(), nullable=True),
    sa.Column('method_id', sa.Integer(), nullable=True),
    sa.Column('admission_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['admission_id'], ['admissions.id'], ),
    sa.ForeignKeyConstraint(['method_id'], ['methods.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('cdc_exam',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('details', sa.String(length=255), nullable=True),
    sa.Column('sample_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['sample_id'], ['samples.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('cdc_exam')
    op.drop_table('samples')
    op.drop_table('observed_symptoms')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_table('users')
    op.drop_table('admissions')
    op.drop_table('symptoms')
    op.drop_table('roles')
    op.drop_table('patients')
    op.drop_table('methods')
    # ### end Alembic commands ###
