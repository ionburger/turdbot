import sqlite3 as sql
class storage:
    def __init__(self,serverid):
        self.serverid = serverid
        self.conn = sql.connect('data/storage.db')
        self.cur = self.conn.cursor()

    def read(self,module,key):
        read = (self.cur.execute("select "+module+" from config where serverid=?",(self.serverid,)).fetchall())[0][0].split(",")  
        data = {}
        for i in range(len(read)):
            data[read[i].split(":")[0]] = read[i].split(":")[1]
        if key not in data:
            readd = (self.cur.execute("select "+module+" from config where serverid=?",("default",)).fetchall())[0][0].split(",")
            datad = {}
            for i in range(len(readd)):
                datad[readd[i].split(":")[0]] = readd[i].split(":")[1]
            data[key] = datad[key]
        return data[key]

    def write(self,module,key,value):
        read = (self.cur.execute("select "+module+" from config where serverid=?",(self.serverid,)).fetchall())[0][0].split(",")  
        data = {}
        for i in range(len(read)):
            data[read[i].split(":")[0]] = read[i].split(":")[1]
        data[key] = value
        write = ""
        i = 0
        for k,v in data.items():
            if i != 0:
                write += ","
            write += k+":"+str(v)
            i += 1
        self.cur.execute("update config set "+module+" = ? where serverid = ?",(write,self.serverid))
        self.conn.commit()
        return True
