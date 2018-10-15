from flask import Flask, render_template

app = Flask(__name__)
# based on 'Python Business Intelligence cookbook' from safari online

@app.route('/')
def index():
    message = 'the message goes here'
    return render_template('index.html', message=message)

@app.route('/user/<name>')
def user(name):
    return '<h1>Hello, {}!'.format(name)

if __name__ == "__main__":
    app.debug = True  # Comment this out when going into production
    app.run()