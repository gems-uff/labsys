import csv
import io

from flask import make_response

from ..extensions import db


def filter_table_name(source):
    if source in ['products', 'stock_products', 'transactions']:
        return source
    else:
        raise ValueError('{} is not a valid table name or \
            was not included in the allowed tables list'.format(source))


export_products_query = "SELECT \
    id,\
    name as reativo,\
    manufacturer as fabricante,\
    catalog as catalogo,\
    stock_unit as unidade_de_estoque,\
    min_stock as estoque_minimo\
    FROM products"

export_stock_products_query = "SELECT \
    sp.id,\
    p.name as reativo,\
    amount as quantidade,\
    lot_number as lote,\
    expiration_date as data_de_validade\
    FROM stock_products as sp\
        JOIN products as p ON (sp.product_id = p.id)\
        JOIN stocks as s ON (sp.stock_id = s.id)\
    ORDER BY p.name, sp.expiration_date ASC;"

export_transactions_query = "SELECT \
    t.id,\
    p.name as reativo,\
    t.amount as quantidade,\
    t.transaction_date as data_da_transacao,\
    u.email as email_usuario,\
    t.invoice_type as tipo_nota,\
    t.invoice as nota,\
    t.financier as financiador,\
    t.details as observacao\
    FROM transactions as t\
    JOIN products as p ON (t.product_id = p.id)\
    JOIN users as u ON (t.user_id = u.id);"


def get_query(table_name):
    table_name = filter_table_name(table_name)
    if table_name == 'products':
        query = export_products_query
    elif table_name == 'stock_products':
        query = export_stock_products_query
    elif table_name == 'transactions':
        query = export_transactions_query
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
