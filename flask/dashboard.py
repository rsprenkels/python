from flask_bootstrap import Bootstrap
from flask import Flask, render_template
import flask_table as ft
import sys

app = Flask(__name__)

bootstrap = Bootstrap(app)

@app.route('/')
def index():
    message = 'Welcome to Your First Flask Application!'
    name = "Ron Sprenkels"
    version = sys.version
    return render_template('user.html',
                           message=message, name=name)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == "__main__":
    app.debug = True  # Comment this out when going into production
    app.run()
