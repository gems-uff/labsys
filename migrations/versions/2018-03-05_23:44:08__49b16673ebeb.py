"""empty message

Revision ID: 49b16673ebeb
Revises:
Create Date: 2018-03-05 23:44:08.620582

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '49b16673ebeb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('countries',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name_pt_br', sa.String(
                        length=255), nullable=True),
                    sa.Column('abbreviation', sa.String(
                        length=2), nullable=True),
                    sa.Column('name_en_us', sa.String(
                        length=255), nullable=True),
                    sa.Column('bacen_code', sa.Integer(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('methods',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(length=64), nullable=True),
                    sa.Column('primary', sa.Boolean(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('patients',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(length=255), nullable=True),
                    sa.Column('birth_date', sa.Date(), nullable=True),
                    sa.Column('age', sa.Integer(), nullable=True),
                    sa.Column('age_unit', sa.String(length=1), nullable=True),
                    sa.Column('gender', sa.String(length=1), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('pre_allowed_users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('full_name', sa.String(
                        length=128), nullable=True),
                    sa.Column('email', sa.String(length=128), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('products',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(length=128), nullable=False),
                    sa.Column('stock_minimum', sa.Integer(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('roles',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(length=64), nullable=True),
                    sa.Column('default', sa.Boolean(), nullable=True),
                    sa.Column('permissions', sa.Integer(), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('name')
                    )
    op.create_index(op.f('ix_roles_default'), 'roles',
                    ['default'], unique=False)
    op.create_table('stocks',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(length=128), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('symptoms',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(length=64), nullable=True),
                    sa.Column('primary', sa.Boolean(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('regions',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('country_id', sa.Integer(), nullable=True),
                    sa.Column('name', sa.String(length=16), nullable=True),
                    sa.Column('region_code', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(
                        ['country_id'], ['countries.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('specifications',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('product_id', sa.Integer(), nullable=False),
                    sa.Column('manufacturer', sa.String(
                        length=128), nullable=False),
                    sa.Column('catalog_number', sa.String(
                        length=128), nullable=False),
                    sa.Column('units', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('manufacturer', 'catalog_number',
                                        name='manufacturer_catalog')
                    )
    op.create_table('stock_products',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('stock_id', sa.Integer(), nullable=False),
                    sa.Column('product_id', sa.Integer(), nullable=False),
                    sa.Column('lot_number', sa.String(
                        length=64), nullable=False),
                    sa.Column('expiration_date', sa.Date(), nullable=True),
                    sa.Column('amount', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
                    sa.ForeignKeyConstraint(['stock_id'], ['stocks.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('product_id', 'stock_id',
                                        'lot_number', name='stock_product')
                    )
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(length=64), nullable=True),
                    sa.Column('password_hash', sa.String(
                        length=128), nullable=True),
                    sa.Column('confirmed', sa.Boolean(), nullable=True),
                    sa.Column('stock_mail_alert', sa.Boolean(), nullable=True),
                    sa.Column('role_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_table('orders',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('created_on', sa.DateTime(), nullable=True),
                    sa.Column('updated_on', sa.DateTime(), nullable=True),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('invoice', sa.String(length=128), nullable=True),
                    sa.Column('invoice_type', sa.String(
                        length=128), nullable=True),
                    sa.Column('financier', sa.String(
                        length=128), nullable=True),
                    sa.Column('notes', sa.String(length=256), nullable=True),
                    sa.Column('order_date', sa.DateTime(), nullable=False),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
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
    op.create_table('transactions',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('created_on', sa.DateTime(), nullable=True),
                    sa.Column('updated_on', sa.DateTime(), nullable=True),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('product_id', sa.Integer(), nullable=False),
                    sa.Column('stock_id', sa.Integer(), nullable=False),
                    sa.Column('amount', sa.Integer(), nullable=False),
                    sa.Column('category', sa.Integer(), nullable=False),
                    sa.CheckConstraint(
                        'amount > 0', name='amount_is_positive'),
                    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
                    sa.ForeignKeyConstraint(['stock_id'], ['stocks.id'], ),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
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
    op.create_table('order_items',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('item_id', sa.Integer(), nullable=False),
                    sa.Column('order_id', sa.Integer(), nullable=False),
                    sa.Column('amount', sa.Integer(), nullable=False),
                    sa.Column('lot_number', sa.String(
                        length=64), nullable=False),
                    sa.Column('expiration_date', sa.Date(), nullable=True),
                    sa.Column('added_to_stock', sa.Boolean(), nullable=True),
                    sa.ForeignKeyConstraint(
                        ['item_id'], ['specifications.id'], ),
                    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('addresses',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('neighborhood', sa.String(
                        length=255), nullable=True),
                    sa.Column('zone', sa.Integer(), nullable=True),
                    sa.Column('details', sa.String(length=255), nullable=True),
                    sa.Column('patient_id', sa.Integer(), nullable=True),
                    sa.Column('country_id', sa.Integer(), nullable=True),
                    sa.Column('state_id', sa.Integer(), nullable=True),
                    sa.Column('city_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['city_id'], ['cities.id'], ),
                    sa.ForeignKeyConstraint(
                        ['country_id'], ['countries.id'], ),
                    sa.ForeignKeyConstraint(['patient_id'], ['patients.id'], ),
                    sa.ForeignKeyConstraint(['state_id'], ['states.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('admissions',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('id_lvrs_intern', sa.String(
                        length=32), nullable=True),
                    sa.Column('first_symptoms_date', sa.Date(), nullable=True),
                    sa.Column('semepi_symptom', sa.Integer(), nullable=True),
                    sa.Column('health_unit', sa.String(
                        length=128), nullable=True),
                    sa.Column('requesting_institution',
                              sa.String(length=128), nullable=True),
                    sa.Column('details', sa.String(length=255), nullable=True),
                    sa.Column('state_id', sa.Integer(), nullable=True),
                    sa.Column('city_id', sa.Integer(), nullable=True),
                    sa.Column('patient_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['city_id'], ['cities.id'], ),
                    sa.ForeignKeyConstraint(['patient_id'], ['patients.id'], ),
                    sa.ForeignKeyConstraint(['state_id'], ['states.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('id_lvrs_intern')
                    )
    op.create_table('clinical_evolutions',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('death', sa.Boolean(), nullable=True),
                    sa.Column('date', sa.Date(), nullable=True),
                    sa.Column('admission_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(
                        ['admission_id'], ['admissions.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('hospitalizations',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('occurred', sa.Boolean(), nullable=True),
                    sa.Column('date', sa.Date(), nullable=True),
                    sa.Column('admission_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(
                        ['admission_id'], ['admissions.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('observed_symptoms',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('observed', sa.Boolean(), nullable=True),
                    sa.Column('details', sa.String(length=255), nullable=True),
                    sa.Column('symptom_id', sa.Integer(), nullable=True),
                    sa.Column('admission_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(
                        ['admission_id'], ['admissions.id'], ),
                    sa.ForeignKeyConstraint(['symptom_id'], ['symptoms.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('samples',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('_ordering', sa.Integer(), nullable=True),
                    sa.Column('admission_date', sa.Date(), nullable=True),
                    sa.Column('collection_date', sa.Date(), nullable=True),
                    sa.Column('semepi', sa.Integer(), nullable=True),
                    sa.Column('details', sa.String(length=128), nullable=True),
                    sa.Column('method_id', sa.Integer(), nullable=True),
                    sa.Column('admission_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(
                        ['admission_id'], ['admissions.id'], ),
                    sa.ForeignKeyConstraint(['method_id'], ['methods.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('uti_hospitalizations',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('occurred', sa.Boolean(), nullable=True),
                    sa.Column('date', sa.Date(), nullable=True),
                    sa.Column('admission_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(
                        ['admission_id'], ['admissions.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('vaccines',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('applied', sa.Boolean(), nullable=True),
                    sa.Column('last_dose_date', sa.Date(), nullable=True),
                    sa.Column('admission_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(
                        ['admission_id'], ['admissions.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('cdc_exam',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('flu_type', sa.String(length=16), nullable=True),
                    sa.Column('flu_subtype', sa.String(
                        length=16), nullable=True),
                    sa.Column('dominant_ct', sa.Integer(), nullable=True),
                    sa.Column('details', sa.String(length=255), nullable=True),
                    sa.Column('sample_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['sample_id'], ['samples.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('cdc_exam')
    op.drop_table('vaccines')
    op.drop_table('uti_hospitalizations')
    op.drop_table('samples')
    op.drop_table('observed_symptoms')
    op.drop_table('hospitalizations')
    op.drop_table('clinical_evolutions')
    op.drop_table('admissions')
    op.drop_table('addresses')
    op.drop_table('order_items')
    op.drop_table('cities')
    op.drop_table('transactions')
    op.drop_table('states')
    op.drop_table('orders')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_table('stock_products')
    op.drop_table('specifications')
    op.drop_table('regions')
    op.drop_table('symptoms')
    op.drop_table('stocks')
    op.drop_index(op.f('ix_roles_default'), table_name='roles')
    op.drop_table('roles')
    op.drop_table('products')
    op.drop_table('pre_allowed_users')
    op.drop_table('patients')
    op.drop_table('methods')
    op.drop_table('countries')
    # ### end Alembic commands ###
