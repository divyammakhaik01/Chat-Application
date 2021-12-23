from flask import *
# from flask_mysqldb import MySQL
import os


def login (username , password, mysql):
    if 'username' in session:
        return render_template('index.html')
    else:
        cur = mysql.connection.cursor()
        username_check = cur.execute( 'SELECT * from chat.user where username = %s and password = %s '  , [username , password] )
        if username_check > 0  :
            cur.execute('SELECT id from chat.user where username = %s  '  , [username] )
            user_id = cur.fetchone() 
            cur.execute( 'SELECT role from chat.user where username = %s '  , [username] )
            check_role = cur.fetchone()
            mysql.connection.commit()
            cur.close()
            if check_role[0] == 1: 
                print('User logged in' , check_role)
                session['username'] = username 
                session['id'] = user_id
                session['admin'] = False
                return True
            else:
                print('Admin logged in')
                session['username'] = username 
                session['id'] = user_id 
                session['admin'] = True
                return True
        else:
            return False
       
        

def logout():
    session.pop('username' , None)
    session.pop('admin' , False)
    session.pop('id' , None)





def register (username , password , mysql):
    cur  = mysql.connection.cursor()
    cur.execute("INSERT INTO chat.user  (username , password , role) values (%s,%s,%s) "  , (username, password,1))     
    mysql.connection.commit()



