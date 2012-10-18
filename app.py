from flask import Flask, request, redirect, render_template, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from urlparse import urlparse, urljoin
from sqlalchemy.sql.expression import func, select
import os
import random
import string

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['HEROKU_POSTGRESQL_BLUE_URL']
db = SQLAlchemy(app)

_EXPANSIONS = ["Dominion", "Intrigue", "Prosperity", "Seaside",  "Cornucopia", "Alchemy", "Hinterlands"]


collections = db.Table('collections',
    db.Column('card_id', db.Integer, db.ForeignKey('card.id')),
    db.Column('collection_id', db.Integer, db.ForeignKey('collection.id'))
)

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    expansion = db.Column(db.String(80), unique=False)

    def __init__(self, name, expansion):
        self.name = name
        self.expansion = expansion

    def __repr__(self):
        return '<Card %r>' % self.name

class Collection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cards = db.relationship('Card', secondary=collections, backref='collections')


@app.route("/")
def home():
    expansions = request.args.getlist("expansion")

    if not expansions:
        return render_template('home.html', all_expansions = _EXPANSIONS)

    # get a random number of cards for each expansion
    ran = constrained_random(len(expansions), 10)
    cards = {}
    for i, e in enumerate(expansions):
        # don't do anything if there are no cards
        if not ran[i]:
            continue

        cards[e] = []

        # if the cards are from prosperity, select 
        # whether or not playing with Colony and Platinum
        if e == "Prosperity" and random.randint(1,10) <= ran[i]:
            cards[e] = ["Platinum", "Colony"]

        card_query = Card.query.filter_by(expansion=e).order_by(func.random()).limit(ran[i])
        
        for card in card_query:
            cards[e].append(card.name)

    rand = "".join([random.choice(string.letters + string.digits) for i in xrange(3)] )
    return render_template('home.html', cards = cards, expansions=expansions, all_expansions = _EXPANSIONS, rand=rand)

@app.route("/save_collection", methods=['POST'])
def save_collection():
    make_collection_from_strings(request.form.getlist("cards"))
    return redirect(url_for('home'))



@app.route("/saved_sets")
def collections():
    collection_query = Collection.query.all()
    collections = []
    for c in collection_query:
        collections.append(c.cards)

    return render_template('collections.html', collections = collections)


def constrained_random(n, total):
    """Return a randomly chosen list of n nonnegative integers summing to total.
    Each such list is equally likely to occur."""

    return [x - 1 for x in constrained_sum_sample_pos(n, total + n)]

def constrained_sum_sample_pos(n, total):
    """Return a randomly chosen list of n positive integers summing to total.
    Each such list is equally likely to occur."""

    dividers = sorted(random.sample(xrange(1, total), n - 1))
    return [a - b for a, b in zip(dividers + [total], [0] + dividers)]

def make_collection_from_strings(card_strings):
    cards = []
    for c in card_strings:
        print c
        card = Card.query.filter_by(name=c).first()
        if card:
            cards.append(card)
    make_collection(cards)

def make_collection(cards):
    c = Collection()
    for card in cards:
        if c != "Platinum" and c != "Colony":
            c.cards.append(card)
    db.session.commit()

if __name__ == "__main__":
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

