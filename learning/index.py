from flask import Flask, render_template
import flask_table as ft
import sys

app = Flask(__name__)
# based on 'Python Business Intelligence cookbook' from safari online
# and https://flask-table.readthedocs.io/en/stable/


class ItemTable(ft.Table):
    name = ft.Col('Name')
    description = ft.Col('Description')

class Item(object):
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __str__(self):
        return f"name:{self.name} descr:{self.description}"

items = [Item('Ron', 'descr Ron'),
         Item('Joyce', 'descr Joyce')]

table = ItemTable(items)

@app.route('/')
def index():
    message = 'Welcome to Your First Flask Application!'
    version = sys.version
    return render_template('index.html',
                           message=message, version=version, table=table, items=items)


if __name__ == "__main__":
    app.debug = True  # Comment this out when going into production
    app.run()

