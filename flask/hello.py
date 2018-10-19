from flask import Flask, render_template

app = Flask(__name__)
# based on 'Python Business Intelligence cookbook' from safari online

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.debug = True  # Comment this out when going into production
    app.run()