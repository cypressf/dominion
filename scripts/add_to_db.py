import csv
from app import db
from app import Card

with open('cards.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        name = row[0]
        expansion = row[1]

        if name == "Name" or name == "":
            continue

        print "%s: %s" % (name, expansion)

        c = Card(name, expansion)
        db.session.add(c)
        db.session.commit()