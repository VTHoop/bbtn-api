import os

__author__ = "hooper-p"

import pymongo


class Database(object):
    DATABASE = None

    @staticmethod
    def initialize():
        client = pymongo.MongoClient("localhost", 27017)
        Database.DATABASE = client.bbtn

    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_all(collection):
        return Database.DATABASE[collection].find()

    @staticmethod
    def find_and_sort(collection, query, sorted_by):
        return Database.DATABASE[collection].find(query).sort(sorted_by)

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)

    @staticmethod
    def update(collection, query, update):
        return Database.DATABASE[collection].update(query, update, upsert=True)

    @staticmethod
    def delete(collection, query):
        return Database.DATABASE[collection].remove(query)

    @staticmethod
    def update_many(collection, query, update):
        return Database.DATABASE[collection].update(query, update, multi=True)
