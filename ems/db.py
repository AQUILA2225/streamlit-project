import pymysql 

def dbConnection():
    try:
        con = pymysql.connect(
            host = "localhost",
            user = "root",
            password = "root",
            database = "ems"
        )
        print("Database connected successfully!!!")
        return con
    except Exception as e:
        print("Connection error:", e)
        return None

def getCursor():
    con = dbConnection()
    if con:
        return con.curObj(), con
    else:
        return None, None
    
def closeConnection(con):
    if con:
        con.close()