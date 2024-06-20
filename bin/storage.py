class storage:
    def __init__(self, server_id, db):
        self.server_id = str(server_id)
        self.db = db
        self.collection = db['turdbot']
    
    async def store(self, module, key=None, value=None):
        document = await self.collection.find_one({"server_id": self.server_id})
        
        if not document:
            document = {
                "server_id": self.server_id,
                "modules": {}
            }
        
        modules = document.get("modules", {})
        
        if module not in modules:
            modules[module] = {}
        
        if key is None:
            return modules.get(module)
        
        if value is not None:
            modules[module][key] = value
            await self.collection.update_one(
                {"server_id": self.server_id},
                {"$set": {"modules": modules}},
                upsert=True
            )
        
        return modules[module].get(key)