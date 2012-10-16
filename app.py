from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
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