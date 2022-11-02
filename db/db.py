import os
from pymongo import MongoClient,database
import pymongo

db:database.Database = None

def get_database() -> database.Database:
    global db
    if db != None:
        return db
    client = MongoClient("mongodb://docker:mongopw@localhost:49153")
    db = client["cybersecurity"]
    return db
