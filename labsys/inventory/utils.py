import csv
import io

from flask import make_response

from ..extensions import db


def filter_table_name(source):
    if source in ['products', 'stock_products', 'transactions', 'orders']:
        return source
    else:
        raise ValueError('{} is not a valid table name or \
            was not included in the allowed tables list'.format(source))


export_products_query = "SELECT \
    p.id,\
    p.name as reativo,\
    spec.manufacturer as fabricante,\
    spec.catalog_number as catalogo,\
    spec.units as unidade_de_estoque,\
    p.stock_minimum as estoque_minimo\
    FROM products as p\
        JOIN specifications as spec ON (p.id = spec.product_id)\
    ORDER BY p.name ASC, spec.units ASC"

export_stock_products_query = "SELECT \
    sp.id,\
    p.name as reativo,\
    amount as quantidade,\
    lot_number as lote,\
    expiration_date as data_de_validade\
    FROM stock_products as sp\
        JOIN products as p ON (sp.product_id = p.id)\
        JOIN stocks as s ON (sp.stock_id = s.id)\
    ORDER BY sp.expiration_date ASC, p.name ASC;"


# select id, CASE WHEN t.category='1' THEN t.amount ELSE -t.amount END FROM transactions as t;
    # CASE WHEN t.category='1' THEN t.amount ELSE -t.amount END\

export_transactions_query = "SELECT \
    t.id,\
    p.name as reativo,\
    CASE WHEN t.category='1' THEN t.amount ELSE -t.amount END as quantidade,\
    t.updated_on at time zone 'utc' at time zone 'America/Sao_Paulo'\
        as data_da_transacao,\
    u.email as email_usuario,\
    s.name as estoque\
    FROM transactions as t\
        JOIN products as p ON (t.product_id = p.id)\
        JOIN stocks as s ON (t.stock_id = s.id)\
        JOIN users as u ON (t.user_id = u.id)\
    ORDER BY t.updated_on DESC;"


export_orders_query = 'SELECT \
o.id, \
o.order_date at time zone \'utc\' at time zone \'America/Sao_Paulo\' as data, \
u.email as email_usuario, \
o.invoice as numero_nota, \
o.invoice_type as tipo_nota, \
o.invoice_value as valor_total_nota, \
o.financier as financiador, \
o.notes as observacoes \
FROM orders o JOIN users u ON o.user_id = u.id'


def get_query(table_name):
    table_name = filter_table_name(table_name)
    if table_name == 'products':
        query = export_products_query
    elif table_name == 'stock_products':
        query = export_stock_products_query
    elif table_name == 'transactions':
        query = export_transactions_query
    elif table_name == 'orders':
        query = export_orders_query
    else:
        raise ValueError('{} table does not exist or its query was not added'.
                         format(table_name))
    return query


def export_table(table_name, output_file_name):
    query = get_query(table_name)
    memory = io.StringIO()
    csv_writer = csv.writer(memory)
    db_response = db.session.execute(query)
    rows = db_response.fetchall()
    csv_writer.writerow([header for header in db_response.keys()])
    csv_writer.writerows(rows)
    response = make_response(memory.getvalue())
    response.headers['Content-Disposition'] = \
        'attachment; filename={}'.format(output_file_name)
    response.mimetype = 'text/csv'

    return response


def stock_is_at_minimum(catalog_product):
    if catalog_product.count_amount_stock_products(
    ) <= catalog_product.min_stock:
        return True
    return False
