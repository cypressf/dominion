from flask import Flask, request, redirect, render_template, url_for, make_response
from flask.ext.sqlalchemy import SQLAlchemy
from urlparse import urlparse, urljoin
from sqlalchemy.sql.expression import func, select
import os
import random
import string


#################
# Globals
#################
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['HEROKU_POSTGRESQL_BLUE_URL']
db = SQLAlchemy(app)

_EXPANSIONS = ["Dominion", "Intrigue", "Prosperity", "Seaside",  "Cornucopia", "Alchemy", "Hinterlands"]


##################
# Database classes
# TODO: make this a seperate module and import it
##################

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

    def __init__(cards):
        self.cards = cards


################
# Routes
################
@app.route("/")
def home():
    """
    Display the form that allows someone to select expansions.
    If GET["expansion"] is part of the request, display a list of randomized cards.
    """
    expansions = request.args.getlist("expansion")

    if not expansions:
        expansions_cookie = request.cookies.get('expansions')
        if expansions_cookie:
            expansions = expansions_cookie.split(" ")

    cards = get_random_cards(expansions)

    if not cards:
        return render_template('home.html', all_expansions = _EXPANSIONS)

    # this is a hack. in order to direct the user's attention to the
    # randomized cards, for small screens, the action of the form points to #cards
    # this has a side effect of caching the page, unless a random string
    # is put in the url. We use this random string in the template by placing it
    # in the form as <input type="hidden">
    rand = "".join([random.choice(string.letters + string.digits) for i in xrange(3)] )
    resp = make_response(render_template('home.html', cards = cards, expansions=expansions, all_expansions = _EXPANSIONS, rand=rand))
    
    # put the selected expansions in a cookie
    expansions_cookie = " ".join(expansions)
    resp.set_cookie('expansions', expansions_cookie)

    return resp

@app.route("/save_collection", methods=['POST'])
def save_collection():
    """
    If the client POSTS to save a collection of cards, save it to the database
    """
    make_collection_from_strings(request.form.getlist("cards"))
    return redirect(url_for('home'))


@app.route("/saved_sets")
def sets():
    """
    Return a list of all collections of cards, formatted with the collections template.
    """
    collection_query = Collection.query.all()
    collections = []
    for c in collection_query:
        collections.append(c.cards)

    return render_template('collections.html', collections = collections)




###################
# Helper functions
###################

def get_random_cards(expansions):
    """
    Given a list of expansion names, return a dictionary with those expansion
    names as keys, and lists of cards as the values.

    e.g.
    input: ["Prosperity", "Intrigue"]
    output: {
                "Prosperity": [card1, card2, card3, card4],
                "Intrigue": [card5, card6, card7, card8, card9, card10]
            }
    """
    expansions = validate_expansions(expansions)
    if not expansions:
        return False
    
    # get a random number of cards for each expansion
    ran = constrained_random(len(expansions), 10)
    cards = {}
    for i, e in enumerate(expansions):
        # don't do anything if there are no cards to be delt
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

    return cards

def validate_expansions(expansions):
    """
    Given a list of expansion names, return a list of expansion names
    with all invalid expansion names removed.

    e.g.
    input: ["Prosperity", "Intrigue", "Poop"]
    output: ["Prosperity", "Intrigue"]

    input: "alksjdflkajs"
    output: []
    """
    assert isinstance(expansions, list)
    valid_expansions = [e for e in expansions if e in _EXPANSIONS]
    return valid_expansions


# TODO: combine constrained_random and constrained_sum_sample_pos

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
    """
    Given a string of card namese, link them in a collection.
    """
    cards = []
    for c in card_strings:
        card = Card.query.filter_by(name=c).first()
        if card:
            cards.append(card)
    
    c = Collection(cards)
    db.session.commit()


if __name__ == "__main__":
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

