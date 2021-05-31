"""
  entry point
"""
import sys, os
sys.path.insert(0, os.path.abspath('./'))

from app import app, db_wrapper
from model import *
from resource import *

# drop the schema and data, recreate it
def reset_db():
    model = [User, Ranking, Item, Comparison]
    db_wrapper.database.drop_tables(model)
    db_wrapper.database.create_tables(model)


def main(debug_mode=False):
    app.run(debug=debug_mode)

if __name__ == '__main__':
    reset_db()
    main(debug_mode=True)

