import sqlite3 as sql
serverid = "default2"

conn = sql.connect('../data/storage.db')
cur = conn.cursor()
print("Opened database successfully")
def storage(module,key,value="",conn=conn,cur=cur,serverid=serverid,mode="r"):
    read = (cur.execute("select "+module+" from config where serverid=?",(serverid,)).fetchall())[0][0].split(",")  
    data = {}
    for i in range(len(read)):
        data[read[i].split(":")[0]] = read[i].split(":")[1]
    if key not in data:
        readd = (cur.execute("select "+module+" from config where serverid=?",("default",)).fetchall())[0][0].split(",")  
        datad = {}
        for i in range(len(readd)):
            datad[readd[i].split(":")[0]] = readd[i].split(":")[1]
        data[key] = datad[key]
    if mode == "r":
       return data[key]
    elif mode == "w":
        data[key] = value
        write = ""
        i = 0
        for k,v in data.items():
            if i != 0:
                write += ","
            write += k+":"+v
            i += 1
        cur.execute("update config set "+module+" = ? where serverid = ?",(write,serverid))
        return True
    else:
        return False
print(storage("quotequeue","joe"))
conn.commit()

conn.close
