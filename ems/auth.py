from db import getCursor, closeConnection

def login(username, password, role):
    curObj, con = getCursor() 
    
    if role == "Admin":
        query = "select * from admin where admin_name=%s and password=%s"
    else:
        query = "select * from employee where username=%s and password=%s"
        
    cursor.execute(query,(username, password))
    user = curObj.fetchone()
    
    closeConnection(con)
    return user