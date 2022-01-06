import json

from pseudo_database import PseudoDatabase


def add_item(category: str, label: str):
    item = PseudoDatabase.Item(label)
    pseudo_database = PseudoDatabase()
    pseudo_database.add(category=category, item=item)


def read_all() -> str:
    pseudo_database = PseudoDatabase()
    db_dict = pseudo_database.read_all()
    json_dict = {}
    for category in db_dict:
        json_dict[category] = json.dumps([z.__dict__ for z in db_dict[category]])
    return json.dumps(json_dict)
