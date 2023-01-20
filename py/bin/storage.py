class Config:
    def __init__(self, serverid,db):
        self.serverid = str(serverid)
        self.db = db[str(serverid)]
        self.default = db['default']

    def read(self, module, key):
        return self.db.find_one({'module': module})[key]

    def write(self, module, key, value):
        self.db.update_one({'module': str(module)}, {'$set': {str(key): str(value)}}, upsert=True)
        return True
    
    def updateguild(self):
        for doc in self.default.find():
            existing_doc = self.db.find_one({"module": doc["module"]})
            if existing_doc:
                for key, value in doc.items():
                    if key not in existing_doc:
                        existing_doc[key] = value
                self.db.replace_one({"module": doc["module"]}, existing_doc)
            else:
                self.db.insert_one(doc)



