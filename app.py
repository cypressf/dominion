from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['HEROKU_POSTGRESQL_BLUE_URL']
db = SQLAlchemy(app)



class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    expansion = db.Column(db.String(80), unique=False)

    def __init__(self, name, expansion):
        self.name = name
        self.expansion = expansion

    def __repr__(self):
        return '<Card %r>' % self.name

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)