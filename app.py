from flask import Flask, request, redirect, render_template, url_for, make_response, jsonify
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
_VALID_ARGS = ["min_cost_treasure",
               "max_cost_treasure",
               "min_cost_potion",
               "max_cost_potions",
               "min_plus_actions",
               "max_plus_actions",
               "min_plus_treasure",
               "max_plus_treasure",
               "min_plus_cards",
               "max_plus_cards",
               "min_plus_buys",
               "max_plus_buys",
               "min_victory_points",
               "max_victory_points",
               "min_trashes",
               "max_trashes",
               "is_attack",
               "is_reaction",
               "min_treasure",
               "max_treasure",
               "min_victory_points",
               "max_victory_points"]

_VALID_CARD_PARAMS = [
                "name",
                "cost_treasure",
                "cost_potions",
                "description",
                "plus_actions",
                "plus_cards",
                "plus_treasure",
                "plus_buys",
                "trashes",
                "is_attack",
                "is_reaction",
                "treasure",
                "victory_points",
                "expansion_id"]

##################
# Database classes
# TODO: make this a seperate module and import it
##################

collections = db.Table('collections',
    db.Column('card_id', db.Integer, db.ForeignKey('card.id')),
    db.Column('collection_id', db.Integer, db.ForeignKey('collection.id'))
)

class Expansion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    cards = db.relationship('Card', backref='expansion', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Expansion %r>' % self.name

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    cost_treasure = db.Column(db.Integer)
    cost_potions = db.Column(db.Integer)
    description = db.Column(db.String(500))

    plus_actions = db.Column(db.Integer)
    plus_cards = db.Column(db.Integer)
    plus_treasure = db.Column(db.Integer)
    plus_buys = db.Column(db.Integer)
    trashes = db.Column(db.Integer)
    is_attack = db.Column(db.Boolean)
    is_reaction = db.Column(db.Boolean)
    treasure = db.Column(db.Integer)
    victory_points = db.Column(db.Integer)

    expansion_id = db.Column(db.Integer, db.ForeignKey('expansion.id'))

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

@app.route("/api/")
def api():
    """
    Return instructions on how to use the api
    """
    pass

@app.route("/api/expansions")
def api_expansions():
    """
    Return a list of expansions, and their cards, in json form.

    e.g.
    {
        Dominion:
        ["Cellar": {name: "Cellar"},
        "Chapel": {name: "Chapel"},
        "Moat": {name: "Moat"}, ... ],

        Intrigue:
        ["Courtyard": {name: "Courtyard"},
        "Pawn": {name: "Pawn"},
        "Secret Chamber": {name: "Secret Chamber"}, ... ],

        ...
    }
    """
    expansions = {}
    expansion_query = Expansion.query.all()
    for e in expansion_query:
        # put the names of the cards in a list
        card_names = [{"name": c.name} for c in e.cards]
        card_dict = {}
        for card in e.cards:
            card_dict[card.name] = dict_from_card(card)

        # store this list as the value under the expansion's name
        # in the expansions dictionary
        expansions[e.name] = card_dict
    return jsonify(expansions)

@app.route("/api/cards/")
def api_cards():
    """
    Return a dictionary of cards, in json form.

    e.g.
        {"Cellar": {name: "Cellar"},
        "Chapel": {name: "Chapel"},
        "Moat": {name: "Moat"},
        "Courtyard": {name: "Courtyard"},
        "Pawn": {name: "Pawn"},
        "Secret Chamber": {name: "Secret Chamber"}, ... ]

    This will be more useful when cards contain more
    information.
    """
    sql_parameters = parse_args(request.args)
    if sql_parameters:
        try:
            card_query = Card.query.filter(*sql_parameters)
        except:
            db.session.rollback()
            return jsonify({"error": "something was malformed in your request params"})
    else:
        card_query = Card.query.all()
    
    card_dict = {}
    for card in card_query:
        card_dict[card.name] = dict_from_card(card)
    return jsonify(card_dict)

@app.route("/api/cards/<id>", methods=['POST', 'GET'])
def api_card(id):
    """
    Return a card matching an id.
    """

    if request.method == "POST":
        errors = api_modify_card(id, request)
        if not errors:
            return redirect(url_for("api_card", id=id))
        return errors

    if request.method == "GET":
        return api_get_card(id)


def api_modify_card(id, request):
    card = get_card(id)
    if not card:
        return jsonify({"error": "no cards match"})

    for param in request.form:
        if param in _VALID_CARD_PARAMS:
            value = request.form[param]
            setattr(card, param, value)
    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"error": "invalid modification parameters"})
    return False


def api_get_card(id):
    card = get_card(id)

    if card:
        card_dict = {}
        card_dict[card.name] = dict_from_card(card)
        return jsonify(card_dict)
    else:
        return jsonify({"error": "no cards match"})

def get_card(id):
    try:
        id = int(id)
        card = Card.query.get(int(id))
    except:
        card = None

    return card

def parse_args(args):
    """
    Given args from an api request, return a list of parameters to pass to Card.query.filter()
    """
    sql_parameters = []
    args_dict = dict(args)
    for arg in args_dict:
        if arg in _VALID_ARGS:
            if "min_" in arg:
                arg += " >= " + str(int(args_dict[arg][0]))
                arg = arg.replace("min_", "")
            if "max_" in arg:
                arg += " <= " + str(int(args_dict[arg][0]))
                arg = arg.replace("max_", "")

            if "is_" in arg:
                arg += " == " + str(bool(int(args_dict[arg][0])))
            sql_parameters.append(arg)
    return sql_parameters



def dict_from_card(card):
    """
    Given a database Card object, return a python dict equivalent.
    """
    return {"name": card.name,
            "id": card.id,
            "cost_treasure": card.cost_treasure,
            "cost_potions": card.cost_potions,
            "description": card.description,
            "expansion": card.expansion.name,
            "plus_actions": card.plus_actions,
            "plus_cards": card.plus_cards,
            "plus_treasure": card.plus_treasure,
            "plus_buys": card.plus_buys,
            "trashes": card.trashes,
            "is_attack": card.is_attack,
            "is_reaction": card.is_reaction,
            "treasure": card.treasure,
            "victory_points": card.victory_points}


@app.route("/edit")
def edit():
    """
    Allow one to edit the cards in the database
    """
    return render_template('edit.html')


@app.route("/")
def home():
    """
    Display the form that allows someone to select expansions.
    If GET["expansion"] is part of the request, display a list of randomized cards.
    """
    # expansions = get_expansions(request)
    # cards = get_random_cards(expansions)
    all_expansions = Expansion.query.all()
    all_expansions = [e.name for e in all_expansions]
    
    # if not cards:
    return render_template('home.html', all_expansions = all_expansions)

    # this is a hack. in order to direct the user's attention to the
    # randomized cards, for small screens, the action of the form points to #cards
    # this has a side effect of caching the page, unless a random string
    # is put in the url. We use this random string in the template by placing it
    # in the form as <input type="hidden">
    # rand = "".join([random.choice(string.letters + string.digits) for i in xrange(3)] )
    # resp = make_response(render_template('home.html', cards = cards, expansions=expansions, all_expansions = all_expansions, rand=rand))
    
    # put the selected expansions in a cookie
    # expansions_cookie = " ".join(expansions)
    # resp.set_cookie('expansions', expansions_cookie)

    # return resp

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

def get_expansions(request):
    """
    Given a request, return a list of expansion names.
    """
    print "getting expansions"
    expansions = request.args.getlist("expansion")

    if not expansions:
        print "getting from cookie"
        expansions_cookie = request.cookies.get('expansions')
        if expansions_cookie:
            expansions = expansions_cookie.split(" ")

    if expansions: return expansions
    return []


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

        expansion = Expansion.query.filter_by(name=e).first()
        card_query = Card.query.filter_by(expansion=expansion).order_by(func.random()).limit(ran[i])
        
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
    expansion_query = Expansion.query.all()
    all_expansions = [e.name for e in expansion_query]
    assert isinstance(expansions, list)

    valid_expansions = [e for e in expansions if e in all_expansions]
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

