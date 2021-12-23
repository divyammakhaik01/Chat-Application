from flask import *
from datetime import datetime, timedelta
from flask.signals import Namespace
from werkzeug.wrappers import ResponseStreamMixin
from flask_mysqldb import MySQL
from models import user,subject,chat
from views.subject_route import sub_route 
from views.chat_route import chat_route 
from flask_socketio import * 
from time import localtime , strftime
import os
import jinja2
import json




with open('config.json'  , 'r') as c :
    params = json.load(c)["params"]


app = Flask(__name__ , static_url_path='/static')

# init sockitIO
socketio = SocketIO(app)

# DB Config
app.secret_key = params["KEY"]
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = params["USER"]
app.config['MYSQL_PASSWORD'] = params["PASSWORD"]
app.config['MYSQL_DB'] = params["DB_NAME"]

# init of DB
mysql = MySQL(app)


app.jinja_env.globals.update(zip=zip)



# Blue prints register
app.register_blueprint(sub_route)
app.register_blueprint(chat_route)



# Home  
@app.route('/')
def hello_world():
    if 'username' in session :
        cur = mysql.connection.cursor();
        currName =  session['username']
        cur.execute('SELECT username FROM chat.user where username = "%s"' , [currName])
        mysql.connection.commit()
        return render_template('intro.html' , user = session['username'])
    else:
        return render_template('intro.html')


#------------------ Authentication Routes ------------------

# Login
@app.route('/login' , methods = [ 'GET','POST' ])
def login():
    if request.method == 'POST':
        name = request.form['username'];
        password = request.form['pass'];
        if user.login(name,password,mysql) == True:
            return redirect('/')
        else:
            return redirect(url_for('register'))
    else:
         return render_template('login.html')

# Register
@app.route('/register' , methods = ['POST','GET'])
def register():
    if request.method == 'POST':
        name = request.form['username'];
        password = request.form['pass'];
        user.register(name,password , mysql)
        return redirect(url_for('login'))
    else:
        return render_template('register.html')

# Logout
@app.route('/logout' , methods = ['POST' , 'GET'])
def logout():
    user.logout()
    return redirect('/')
    




#------------------ message handeling ------------------ 

@socketio.on('message')
def message(data):
    chat.insert_messages(data,mysql)
    send({'message' : data['message'] , 'username' : data['username'] , 'time_stamp' : strftime('%b-%d %I:%M %p',localtime()) } ,broadcast = True,room  = data['room'])


# join room 
@socketio.on('join')
def join(data):
    join_room(data['room'])
    room = data['room']
    new_data = chat.get_messages(data['room'],mysql);
    send({'message' : data['username'] + " has joined the room  " , 'username' : data['username']} ,broadcast = True , room = data['room'])
            

# leaving room 
@socketio.on('leave')
def leave(data):
    leave_room(data['room'])
    send({'message' : data['username'] + " has left the  room" } ,broadcast = True, room = data['room'])






if __name__ == "__main__":
    socketio.run(app )
    # app.run(debug=True)


