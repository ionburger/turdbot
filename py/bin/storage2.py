from pymongo import MongoClient
serverid = "default"
db = MongoClient('server', 5004,username='admin',password='passwordmyassword')['data']
class Storage:
    def __init__(self, serverid,db):
        self.serverid = serverid
        self.db = db[serverid]
        self.default = db['default']

    def read(self, module, key):
        return self.db.find_one({'module': module})[key] or self.default.find({'module': module})[key]

    def write(self, module, key, value):
        self.db.update_one({'module': module}, {'$set': {key: value}}, upsert=True)
        return True
    
    def w(self, module, key, value):
        return self.write(module, key, value)

    def r(self, module, key):
        return self.read(module, key)


