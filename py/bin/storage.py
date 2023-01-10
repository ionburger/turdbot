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
    
    def w(self, module, key, value):
        return self.write(module,key,value)

    def r(self, module, key):
        return self.read(module,key)

    def updateguild(self):
        print("Updating guild")
        # Iterate through all documents in default
        for doc in self.default.find():
        # Check if the document already exists in self.db
            existing_doc = self.db.find_one({"module": doc["module"]})
            if existing_doc:
            # Update the document in self.db with any new values from default
                for key, value in doc.items():
                    if key not in existing_doc:
                        existing_doc[key] = value
                self.db.replace_one({"module": doc["module"]}, existing_doc)
            else:
            # Insert the document into self.db if it does not already exist
                self.db.insert_one(doc)



