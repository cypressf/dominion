import csv
from app import db
from app import Card
import re

def to_int(str):
    m = re.search(r'\d+', str)
    if m:
        return int(m.group())
    else:
        return 0

def modify_card(card_name, attr, value):
    card = Card.query.filter_by(name=card_name).first()
    if not card:
        return False
    try:
        setattr(card, attr, value)
        db.session.commit()
    except:
        db.session.rollback()
        print "something went wrong trying to set %s = %s on %s" % (attr, value, card)
        return False
    print "success! %s:%s = %s" % (card.name, attr, getattr(card, attr))
    return card

def run():
    with open('cards.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            name = row[0]
            expansion = row[1]
            is_action = bool(to_int(row[2]))
            is_attack = bool(to_int(row[3]))
            is_curse = bool(to_int(row[4]))
            is_duration = bool(to_int(row[5]))
            is_reaction = bool(to_int(row[6]))
            is_treasure = bool(to_int(row[7]))
            is_victory = bool(to_int(row[8]))
            cost_treasure = to_int(row[9])
            cost_potions = to_int(row[10])
            plus_actions = to_int(row[11])
            plus_buys = to_int(row[12])
            plus_cards = to_int(row[13])
            plus_treasure = to_int(row[14])
            victory_points = to_int(row[15])
            description = row[16]
            if name == "Name" or name == "":
                continue

            # modify_card(name, "plus_treasure", plus_treasure)
            # modify_card(name, "plus_cards", plus_cards)
            # modify_card(name, "plus_buys", plus_buys)
            # modify_card(name, "plus_actions", plus_actions)
            modify_card(name, "is_attack", is_attack)
            modify_card(name, "is_reaction", is_reaction)

            if is_treasure:
                modify_card(name, "plus_treasure", 0)
                modify_card(name, "treasure", plus_treasure)
            else:
                modify_card(name, "treasure", 0)
            modify_card(name, "cost_treasure", cost_treasure)
            modify_card(name, "cost_potions", cost_potions)
            modify_card(name, "victory_points", victory_points)





if __name__ == "__main__":
    run()