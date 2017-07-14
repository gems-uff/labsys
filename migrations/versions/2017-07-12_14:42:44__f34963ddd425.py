"""empty message

Revision ID: f34963ddd425
Revises: 77adb3584ff6
Create Date: 2017-07-12 14:42:44.289747

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f34963ddd425'
down_revision = '77adb3584ff6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('vaccines',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('applied', sa.Boolean(), nullable=True),
    sa.Column('last_dose_date', sa.Date(), nullable=True),
    sa.Column('admission_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['admission_id'], ['admissions.id'],
                            ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )

    op.create_table('clinical_evolutions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('death', sa.Boolean(), nullable=True),
    sa.Column('date', sa.Date(), nullable=True),
    sa.Column('admission_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['admission_id'], ['admissions.id'],
                            ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )

    op.create_table('hospitalizations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('occurred', sa.Boolean(), nullable=True),
    sa.Column('date', sa.Date(), nullable=True),
    sa.Column('admission_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['admission_id'], ['admissions.id'],
                            ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )

    op.create_table('uti_hospitalizations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('occurred', sa.Boolean(), nullable=True),
    sa.Column('date', sa.Date(), nullable=True),
    sa.Column('admission_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['admission_id'], ['admissions.id'],
                            ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('uti_hospitalizations')
    op.drop_table('hospitalizations')
    op.drop_table('clinical_evolutions')
    op.drop_table('vaccines')
    # ### end Alembic commands ###