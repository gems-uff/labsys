"""empty message

Revision ID: 9d4580d70b07
Revises: 38347a40c76e
Create Date: 2017-08-30 14:53:09.171421

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9d4580d70b07'
down_revision = '38347a40c76e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('samples', sa.Column('details', sa.String(length=128), nullable=True))
    op.drop_constraint('vaccines_admission_id_fkey', 'vaccines', type_='foreignkey')
    op.create_foreign_key(None, 'vaccines', 'admissions', ['admission_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'vaccines', type_='foreignkey')
    op.create_foreign_key('vaccines_admission_id_fkey', 'vaccines', 'admissions', ['admission_id'], ['id'], ondelete='CASCADE')
    op.drop_column('samples', 'details')
    # ### end Alembic commands ###
