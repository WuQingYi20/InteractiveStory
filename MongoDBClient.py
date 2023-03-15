from pymongo import MongoClient

class MongoDBClient:
    def __init__(self, db_url, db_name):
        self.client = MongoClient(db_url)
        self.db = self.client[db_name]
        self.collection = self.db['player_summary']
    
    def insert_document(self, document):
        self.collection.insert_one(document)
    
    def find_document(self, query):
        return self.collection.find_one(query)
    
    def update_document(self, query, document):
        self.collection.update_one(query, {'$set': document})
    
    def delete_document(self, query):
        self.collection.delete_one(query)
