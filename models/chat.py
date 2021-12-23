from flask import *
from app import app 
from models import user 
from views import subject_route,chat_route
from time import localtime , strftime




def isOwner(userid , roomid ,mysql):
    if session['admin'] == True:
        return True
    cur = mysql.connection.cursor()
    sql = "SELECT COUNT(*) from chat.messages where user_id = %s and room_id = %s " , [userid,roomid,mysql]
    res = cur.execute(sql)
    data = cur.fetchone()[0] 
    if(data > 0):
        return True
    else:
        return False


def insert_messages(data,mysql):
    try:
        USERNAME = data['username']
        ROOMNAME = data['room']
        MESSAGE = data['message']
        # TIME = strftime('%b-%d %I: %M %p' ,localtime())


        cur  = mysql.connection.cursor()
        cur.execute("SELECT id from chat.user where username = %s" , [USERNAME]) 
        userID = cur.fetchone()[0]
        cur.execute("SELECT id from chat.rooms where room_name = %s" , [ROOMNAME])
        roomID = cur.fetchone()[0]
        print( 'username  : ' , USERNAME, '\n' , userID  , "\n" , roomID)
        cur.execute("""INSERT into chat.messages (user_id , room_id , content ,visible)
             values (%s,%s,%s,%s)"""  , [userID , roomID , MESSAGE  , 1])     
        mysql.connection.commit()
    except:
        print("Error while adding rights........." , ) 
        
        
        
        
def get_messages(room , mysql):
    curr = mysql.connection.cursor()
    curr.execute("SELECT id from chat.rooms where room_name = %s" , [room])
    roomID = curr.fetchone()[0]
    
    res = curr.execute("SELECT user_id , room_id  , content , created_at from chat.messages where room_id = %s and visible = 1 " ,[roomID] )
    data = curr.fetchall()
    
    
    # print('getMessages : ' , data)
    return data 


