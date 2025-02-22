#!/usr/bin/env python

from model.base import Base
from model.location import Location
from model.box import Box
from model.item import Item, Tag
from model.connection import engine, session

from sqlalchemy import text
from sqlalchemy.sql import func

from pprint import pprint
import yaml
import sys


# main loop
if __name__ == "__main__":
  
  print("start db setup")
  Base.metadata.create_all(bind=engine)
  print("db setup done")
 
  sys.exit(0)

  print("Truncate everything first / very sqlite specific")
  session.execute(text('''DELETE FROM location;'''))
  session.execute(text('''DELETE FROM box;'''))
  session.execute(text('''DELETE FROM item;'''))
  session.commit()
  session.execute(text('''VACUUM;'''))
  session.commit()


  print("start seeding data")
  
# add boxes and items from yaml
  with open('../data/yaml/locations.yaml', 'r') as file:
    locations = yaml.safe_load(file)

    for location in locations['locations']:
      location = locations['locations'][location]
      locationDescription = location['description'] if 'description' in location.keys() else ''
      locationEntry = Location(
        name=location['name'],
        description=locationDescription,
        classification=location['classification']
      )
      session.add(locationEntry)
      session.commit()


  # add boxes and items from yaml
  with open('../data/yaml/boxes.yaml', 'r') as file:
    boxes = yaml.safe_load(file)

    for box in boxes['boxes']:
      box = boxes['boxes'][box]
      boxDescription = box['description'] if 'description' in box.keys() else ''
      locationId = box['locationId'] if 'locationId' in box.keys() else 1
      boxEntry = Box(
        name=box['name'],
        description=boxDescription,
        lastAccess=func.now(),
        locationId=locationId
      )
      session.add(boxEntry)
      session.commit()

      items = []
      for item in box['items']:
        itemDescription = item['description'] if 'description' in item.keys() else ''

        itemEntry = Item(
          name=item['name'],
          amount=item['amount'],
          description=itemDescription,
          image="",
          state='stored',
          lastUsage=func.now(),
          box=boxEntry
        )
        session.add(itemEntry)
        session.commit()



  print("seeding data done")
