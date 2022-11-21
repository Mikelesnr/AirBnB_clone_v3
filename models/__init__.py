#!/usr/bin/python3
"""
initialize the models package
"""

from os import getenv


storage_t = getenv("HBNB_TYPE_STORAGE")

if storage_t == "db":
    from models.engine import db_storage
    CNC = db_storage.classes
    storage = db_storage.DBStorage()
else:
    from models.engine import file_storage
    CNC = file_storage.classes
    storage = file_storage.FileStorage()
storage.reload()
