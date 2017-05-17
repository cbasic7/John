import yaml
import os
import sys
from sqlite3_adapter import Sqlite3Adapter

def load_database():
    database_config_file = open('database.yml', 'r')
    database_config = yaml.load(database_config_file)

    if database_config.get('adapter') == 'sqlite3':
        database = Sqlite3Adapter(database_config.get('database_name'))
        database.connect()
        database_config_file.close()
        return database

def args_to_items(args):
    items = {args[0]: {}}
    for arg in args[1:]:
        items[args[0]][arg.split(':')[0]] = arg.split(':')[1]

    return items

def build_schema(items):
    schema_file = open('schema.yml', 'w')
    yaml.dump(items, schema_file, default_flow_style=False)
    schema_file.close()

def create_table(database, items):
    model_name = items.keys()[0]
    attributes_list = []
    for attribute, attribute_type in items[model_name].items():
        attributes_list.append('%s %s NOT NULL' % (attribute, attribute_type.upper()))

    sql = '''CREATE TABLE %s (ID INTEGER PRIMARY KEY NOT NULL, %s);''' % (model_name.lower() + 's', (', ').join(attributes_list))
    database.execute(sql)

if __name__ == "__main__":
    database = load_database()
    items = args_to_items(sys.argv[1:])
    build_schema(items)
    create_table(database, items)
