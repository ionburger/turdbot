class storage:
    def __init__(self, serverid, db):
        self.serverdb = db[str(serverid)]

    def db(self, module, key, value=None):
        try : r = self.serverdb.find_one({"module": module}).get(key) 
        except AttributeError: r = None
        if value is not None:
            self.serverdb.update_one({"module": module}, {"$set": {key: value}}, upsert=True)
        return r