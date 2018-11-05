from flask_bootstrap import Bootstrap
from flask import Flask, render_template
import pandas as pd
import dash_dao
import helper


app = Flask(__name__)
bootstrap = Bootstrap(app)

# https://pandas.pydata.org/pandas-docs/stable/reshaping.html

@app.route('/')
def index():
    name = "Ron Sprenkels"
    keys, rows = dash_dao.get_migrations()
    data = helper.get_ftable(keys, rows)
    return render_template('dashboard.html', name=name, table=data, table_title='overview')


@app.route('/table')
def table():
    name = "Ron Sprenkels"
    keys, rows = dash_dao.get_migrations()
    df = pd.DataFrame.from_records(rows, columns=keys)
    table = df.pivot(index='city', columns='date_active', values='migrated')
#    data = helper.get_ftable(*dash_dao.get_migrations())
    pkeys = list(table)
    pkeys.insert(0, 'city')
#    prows = [tuple(x) for x in table.to_records(index=True)]
    prows = table.to_dict('records')
    pdata = helper.get_ftable(pkeys, prows)
    table_html = table.to_html(
        classes=('table', 'table-striped', 'table-bordered'),
        na_rep='',
        float_format="%.0f")
    return render_template('dashboard.html', name=name, table=table_html, table_title='overview')

@app.route('/totals')
def totals():
    keys, rows = dash_dao.get_migrations()
    df = pd.DataFrame.from_records(rows, columns=keys)
    table = df.pivot(index='city', columns='date_active', values='migrated')
    table_html = table.to_html(
        classes=('table', 'table-striped', 'table-bordered'),
        na_rep='',
        float_format="%.0f")
    return render_template('dashboard.html', table=table_html, table_title='overview')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == "__main__":
    app.debug = True  # Comment this out when going into production
    app.run(host="0.0.0.0")
