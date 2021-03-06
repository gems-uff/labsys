"""empty message

Revision ID: 9648c552f308
Revises: 129d36205ad9
Create Date: 2018-06-10 11:29:21.812273

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9648c552f308'
down_revision = '129d36205ad9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('addresses', 'zone',
               existing_type=sa.INTEGER(),
               type_=sa.String(length=255),
               existing_nullable=True)
    op.alter_column('admissions', 'health_unit',
               existing_type=sa.VARCHAR(length=128),
               type_=sa.String(length=255),
               existing_nullable=True)
    op.alter_column('admissions', 'id_lvrs_intern',
               existing_type=sa.VARCHAR(length=32),
               type_=sa.String(length=255),
               nullable=False)
    op.alter_column('patients', 'age_unit',
               existing_type=sa.VARCHAR(length=1),
               type_=sa.String(length=255),
               existing_nullable=True)
    op.alter_column('patients', 'gender',
               existing_type=sa.VARCHAR(length=1),
               type_=sa.String(length=255),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('patients', 'gender',
               existing_type=sa.String(length=255),
               type_=sa.VARCHAR(length=1),
               existing_nullable=True)
    op.alter_column('patients', 'age_unit',
               existing_type=sa.String(length=255),
               type_=sa.VARCHAR(length=1),
               existing_nullable=True)
    op.alter_column('admissions', 'id_lvrs_intern',
               existing_type=sa.String(length=255),
               type_=sa.VARCHAR(length=32),
               nullable=True)
    op.alter_column('admissions', 'health_unit',
               existing_type=sa.String(length=255),
               type_=sa.VARCHAR(length=128),
               existing_nullable=True)
    op.alter_column('addresses', 'zone',
               existing_type=sa.String(length=255),
               type_=sa.INTEGER(),
               existing_nullable=True)
    # ### end Alembic commands ###
