import json
from app import db, Card, Expansion
import sys
def add_expansion(name):
    e = Expansion(name)
    try:
        db.session.add(e)
        db.session.commit()
        print "Added expansion: %s" % name
    except:
        print "expansion %s already exists" % name
        db.session.rollback()
        return Expansion.query.filter_by(name=name).first()
    return e

def add_card(card_dict, expansion):
    c = Card(card_dict["name"], expansion)
    del card_dict["id"], card_dict["expansion"], card_dict["name"]
    print expansion
    try:
        db.session.add(c)
        db.session.commit()
        print "Added card: %s" % c.name
        for key in card_dict:
            setattr(c, key, card_dict[key])
            print "    %s = %s" % (key, getattr(c,key))

    except:
        print "card %s already exists" % c.name
        db.session.rollback()
        return Card.query.filter_by(name=c.name).first()

    return c

def run():
    with open('cards.json') as f:
        cards = json.load(f)
        f.close()
        for expansion in cards:
            e = add_expansion(expansion)
            for card_dict in cards[expansion]:
                add_card(card_dict, e)

if __name__ == "__main__":
    run()