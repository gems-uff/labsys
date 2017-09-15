import io
import csv

from labsys import db

def export_inventory(file_name='estoque.csv'):
    memory = io.StringIO()
    csv_writer = csv.writer(memory)
    db_response = db.session.execute('SELECT * FROM products')
    rows = db_response.fetchall()
    csv_writer.writerow([header for header in db_response.keys()])
    csv_writer.writerows(rows)
    response = make_response(memory.getvalue())
    response.headers['Content-Disposition'] = \
        'attachment; filename=estoque.csv'
    response.mimetype = 'text/csv'

    return response
