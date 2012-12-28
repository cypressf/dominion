from app import db, Card, Expansion
Dominion = \
[{"name": "Cellar"},
{"name": "Chapel"},
{"name": "Moat"},
{"name": "Chancellor"},
{"name": "Village"},
{"name": "Woodcutter"},
{"name": "Workshop"},
{"name": "Bureaucrat"},
{"name": "Feast"},
{"name": "Gardens"},
{"name": "Militia"},
{"name": "Moneylender"},
{"name": "Remodel"},
{"name": "Smithy"},
{"name": "Spy"},
{"name": "Thief"},
{"name": "Throne Room"},
{"name": "Council Room"},
{"name": "Festival"},
{"name": "Laboratory"},
{"name": "Library"},
{"name": "Market"},
{"name": "Mine"},
{"name": "Witch"},
{"name": "Adventurer"}]

Dark_Ages = \
[{"name": "Black Market"},
{"name": "Envoy"},
{"name": "Walled Village"},
{"name": "Governor"},
{"name": "Stash"},
{"name": "Altar"},
{"name": "Armory"},
{"name": "Band of Misfits"},
{"name": "Bandit Camp"},
{"name": "Beggar"},
{"name": "Catacombs"},
{"name": "Count"},
{"name": "Counterfeit"},
{"name": "Cultist"},
{"name": "Death Cart"},
{"name": "Feodum"},
{"name": "Forager"},
{"name": "Fortress"},
{"name": "Graverobber"},
{"name": "Hermit"},
{"name": "Hunting Grounds"},
{"name": "Ironmonger"},
{"name": "Junk Dealer"},
{"name": "Madman"},
{"name": "Marauder"},
{"name": "Market Square"},
{"name": "Mercenary"},
{"name": "Mystic"},
{"name": "Pillage"},
{"name": "Poor House"},
{"name": "Procession"},
{"name": "Rats"},
{"name": "Rebuild"},
{"name": "Rogue"},
{"name": "Sage"},
{"name": "Scavenger"},
{"name": "Spoils"},
{"name": "Squire"},
{"name": "Storeroom"},
{"name": "Urchin"},
{"name": "Vagrant"},
{"name": "Wandering Minstrel"},
{"name": "Knights"}]

Intrigue = \
[{"name": "Courtyard"},
{"name": "Pawn"},
{"name": "Secret Chamber"},
{"name": "Great Hall"},
{"name": "Masquerade"},
{"name": "Shanty Town"},
{"name": "Steward"},
{"name": "Swindler"},
{"name": "Wishing Well"},
{"name": "Baron"},
{"name": "Bridge"},
{"name": "Conspirator"},
{"name": "Coppersmith"},
{"name": "Ironworks"},
{"name": "Mining Village"},
{"name": "Scout"},
{"name": "Duke"},
{"name": "Minion"},
{"name": "Saboteur"},
{"name": "Torturer"},
{"name": "Trading Post"},
{"name": "Tribute"},
{"name": "Upgrade"},
{"name": "Harem"},
{"name": "Nobles"}]


Prosperity = \
[{"name": "Loan"},
{"name": "Trade Route"},
{"name": "Watchtower"},
{"name": "Bishop"},
{"name": "Monument"},
{"name": "Quarry"},
{"name": "Talisman"},
{"name": "Worker's Village"},
{"name": "City"},
{"name": "Contraband"},
{"name": "Counting House"},
{"name": "Mint"},
{"name": "Mountebank"},
{"name": "Rabble"},
{"name": "Royal Seal"},
{"name": "Vault"},
{"name": "Venture"},
{"name": "Goons"},
{"name": "Grand Market"},
{"name": "Hoard"},
{"name": "Bank"},
{"name": "Expand"},
{"name": "Forge"},
{"name": "King's Court"},
{"name": "Peddler"}]


Seaside = \
[{"name": "Embargo"},
{"name": "Haven"},
{"name": "Lighthouse"},
{"name": "Native Village"},
{"name": "Pearl Diver"},
{"name": "Ambassador"},
{"name": "Fishing Village"},
{"name": "Lookout"},
{"name": "Smugglers"},
{"name": "Warehouse"},
{"name": "Caravan"},
{"name": "Cutpurse"},
{"name": "Island"},
{"name": "Navigator"},
{"name": "Pirate Ship"},
{"name": "Salvager"},
{"name": "Sea Hag"},
{"name": "Treasure Map"},
{"name": "Bazaar"},
{"name": "Explorer"},
{"name": "Ghost Ship"},
{"name": "Merchant Ship"},
{"name": "Outpost"},
{"name": "Tactician"},
{"name": "Treasury"},
{"name": "Wharf"}]


Cornucopia = \
[{"name": "Hamlet"},
{"name": "Fortune Teller"},
{"name": "Menagerie"},
{"name": "Farming Village"},
{"name": "Horse Traders"},
{"name": "Remake"},
{"name": "Tournament"},
{"name": "Young Witch"},
{"name": "Harvest"},
{"name": "Horn of Plenty"},
{"name": "Hunting Party"},
{"name": "Jester"},
{"name": "Fairgrounds"}]


Alchemy = \
[{"name": "Transmute"},
{"name": "Apothecary"},
{"name": "Herbalist"},
{"name": "Scrying Pool"},
{"name": "University"},
{"name": "Alchemist"},
{"name": "Familiar"},
{"name": "Philosopher's Stone"},
{"name": "Golem"},
{"name": "Apprentice"},
{"name": "Possession"},
{"name": "Vineyard"}]


Hinterlands = \
[{"name": "Crossroads"},
{"name": "Duchess"},
{"name": "Fool's Gold"},
{"name": "Develop"},
{"name": "Oasis"},
{"name": "Oracle"},
{"name": "Scheme"},
{"name": "Tunnel"},
{"name": "Jack of All Trades"},
{"name": "Noble Brigand"},
{"name": "Nomad Camp"},
{"name": "Silk Road"},
{"name": "Spice Merchant"},
{"name": "Trader"},
{"name": "Cache"},
{"name": "Cartographer"},
{"name": "Embassy"},
{"name": "Haggler"},
{"name": "Highway"},
{"name": "Ill-Gotten Gains"},
{"name": "Inn"},
{"name": "Mandarin"},
{"name": "Margrave"},
{"name": "Stables"},
{"name": "Border Village"},
{"name": "Farmland"}]

# cards = {"Dominion": Dominion,
#         "Hinterlands": Hinterlands,
#         "Alchemy": Alchemy,
#         "Intrigue": Intrigue,
#         "Seaside": Seaside,
#         "Cornucopia": Cornucopia,
#         "Prosperity": Prosperity,
#         "Dark Ages": Dark_Ages}
cards = {"Dark Ages": Dark_Ages}
def add_expansions():
    for e_name in cards:
        expansion = Expansion(e_name)
        try:
            db.session.add(expansion)
            db.session.commit()
            print "added expansion %s" % e_name
        except:
            db.session.rollback()
            print "adding %s failed (probably already exists in the database)" % e_name

def get_expansions():
    e_query = Expansion.query.all()
    for e in e_query:
        print e.name

def add_cards():
    add_expansions()
    for e_name in cards:
        expansion = Expansion.query.filter_by(name=e_name).first()
        for c in cards[e_name]:
            card = Card(c["name"], expansion)
            try:
                db.session.add(card)
                db.session.commit()
                print "added card %s" % c["name"]
            except:
                db.session.rollback()
                print "adding card %s failed (probably already exists in the dabtabase)" % c["name"]

def print_cards(expansion):
    c_query = Card.query.filter_by(expansion = expansion)
    for c in c_query:
        print c

add_cards()