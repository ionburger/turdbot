class storage:
    def __init__(self, serverid, db):
        self.serverdb = db[str(serverid)]
        self.defaultdb = db["default"]

    def db(self, module, key, value=None):
        r = self.serverdb.find_one({"module": module})[key]
        if value is not None:
            self.serverdb.update_one({"module": module}, {"$set": {key: value}})
        return r
    
    def update_guild(self):
        for doc in self.defaultdb.find():
            existing_doc = self.serverdb.find_one({"module": doc["module"]})
            if existing_doc:
                for key, value in doc.items():
                    if key not in existing_doc:
                        existing_doc[key] = value
                self.serverdb.replace_one({"module": doc["module"]}, existing_doc)
            else:
                self.serverdb.insert_one(doc)        