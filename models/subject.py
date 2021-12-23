from flask import *
from app import app , mysql
from models import user 
from views import subject_route


def room_pass_check(roomID , Entered_password , mysql):
    cur = mysql.connection.cursor()
    res = cur.execute("SELECT id from chat.rooms where  id= %s and password = %s" , [roomID, Entered_password] )
    data = cur.fetchone()
    # print('room_pass_check :  ' , data)
    if data:
        return True
    else:
        return False

def user_Room_Permission(id,  mysql):
    cur = mysql.connection.cursor()
    res = cur.execute("SELECT id from chat.room_right where user_id = %s and room_id = %s" , [session['id'], id] )
    data = cur.fetchone()
    # print('user_Room_Permission :  ' , data)
    if data:
        return True
    else:
        return False

def isPermissionReq(id , mysql):
    cur = mysql.connection.cursor()
    res = cur.execute("SELECT require_permission from chat.rooms where id = %s" , [id] )
    data = cur.fetchone()[0] 
    print('data : ' , data)
    if data == 0:
        return False
    else:
        return True


def getSubjectsData(self):
    cur = mysql.connection.cursor()
    sql = "SELECT id ,room_name , require_permission from chat.rooms"
    res = cur.execute(sql)
    data = cur.fetchall() 
    return data


def getRoom(id , mysql):
    curr = mysql.connection.cursor()
    sql = "SELECT * from chat.rooms"
    res = curr.execute(sql)
    data = curr.fetchone()[0]
    print("id : " , id)
    return data 



def isSecret(subject_id , mysql):
    curr = mysql.connection.cursor()
    res = curr.execute("SELECT COUNT(*)  from  chat.rooms where id = %s and require_permission = 1 " ,[subject_id])
    data = curr.fetchall()[0]
    return data[0] > 0


def hasRight( subject_id ,mysql):
    user_id = session['id']
    if session['admin']:
       return True 
    else:
        if isSecret(subject_id , mysql):
            curr = mysql.connection.cursor()
            res = curr.execute( "SELECT COUNT(*)  from  chat.room_right where room_id = %s and  user_id = %s" , [subject_id,user_id])
            data = curr.fetchone()[0]

            if data > 0 :   
                print("user has right.......")
                return True 
            else :
                print("User do not have right.......")
                return False
        else:
            return True 
                       
def add_right(user_id , subject_name , mysql):
    try:
        cur  = mysql.connection.cursor()
        cur.execute("""INSERT into chat.room_right (user_id , room_id)
             values (%s,(SELECT id from chat.rooms where room_name = %s ))"""  , [user_id , subject_name])     
        mysql.connection.commit()
    except:
        print("Error while adding rights........." , )    


def create_subject(user_id, subject_name, subject_password, subject_content, subject_require, mysql):
    if subject_password == "":
        subject_password = "1234"
    
    try:
        cur  = mysql.connection.cursor()
        cur.execute("INSERT into chat.rooms (room_name , password , content , require_permission) values (%s,%s,%s,%s)"  , (subject_name, subject_password,subject_content,subject_require))     
        mysql.connection.commit()
    except:
        return False    

    if subject_password != "":
        add_right(session["id"], subject_name, mysql)
        return True

def findRoomName(roomID,mysql):
        cur = mysql.connection.cursor()
        cur.execute("SELECT room_name from  chat.rooms where id = %s  " , [roomID])
        data = cur.fetchall()[0]
        return data[0] 

