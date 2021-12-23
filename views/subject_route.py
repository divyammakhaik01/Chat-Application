from os import name
from app import app
from flask import  *
from werkzeug.exceptions import FailedDependency
from models import subject,user,chat
from flask_mysqldb import MySQL
# from project.models import user

sub_route = Blueprint("sub_route" , __name__)

mysql = MySQL()

@sub_route.route("/rooms")
def subjects():
    subject_data = subject.getSubjectsData(mysql);
    print(subject_data)
    if subject_data:
        return render_template('subjects.html' , subject_data = subject_data   ) 
    else:
        return render_template('subjects.html')


@sub_route.route("/create_sub")
def create_sub():
    return render_template("create_subject.html")


@sub_route.route("/create_subject" ,methods = [ 'GET','POST' ])
def create_subject():
    if request.method == 'POST':
        user_id = session['id']
        subject_name = request.form["subject_name"]
        subject_password = request.form["subject_pass"]
        subject_content = request.form["subject_desc"]
        subject_require = request.form["require"]

        if int(subject_require) == 1 and subject_password == "":
            flash('you must give a password')
            return redirect(request.referrer)

        if subject.create_subject(user_id, subject_name, subject_password, subject_content, subject_require, mysql):
            flash("Room created", "message")
            print("Room created")
            return redirect("/rooms")


        else:
            flash("Error creating subject - name might be taken", "error")
            return redirect(request.referrer)



@sub_route.route("/checkRoomPass" ,methods = [ 'GET','POST' ])
def checkRoomPass():
    if request.method == 'POST':
        user_id = session['id']
        Entered_password = request.form["pass"]
        roomID = request.form["roomID"]
        roomName = subject.findRoomName(roomID,mysql)
        if subject.room_pass_check(roomID, Entered_password, mysql) == True :
            # print('\n\n\n room Name > : ' , roomName)
            new_data = chat.get_messages(roomName,mysql);

            names = []
            time = []
            messages = []
            
            for val in new_data :
                cur  = mysql.connection.cursor()
                cur.execute("SELECT username from chat.user where id = %s" , [val[0]]) 
                USERNAME = cur.fetchone()[0]
                cur.execute("SELECT room_name from chat.rooms where id = %s" , [val[1]])
                ROOMNAME = cur.fetchone()[0]
                names.append(USERNAME)
                time.append(val[3])
                messages.append(val[2])

            return render_template('enterRoom.html' , id = roomID, user = session['username'] ,roomName = roomName,data = zip(names,time,messages))
        else:
            flash('password Incorrect')
            return redirect('/rooms')


@sub_route.route("/enter_room/<int:id>")
def enter_room(id):
    req_permission = subject.isPermissionReq(id , mysql)
    if session['admin'] == True or subject.user_Room_Permission(id,mysql) == True or req_permission == False  :
        roomName = subject.findRoomName(id,mysql)
        new_data = chat.get_messages(roomName,mysql);

        names = []
        time = []
        messages = []
        for val in new_data :
            cur  = mysql.connection.cursor()
            cur.execute("SELECT username from chat.user where id = %s" , [val[0]]) 
            USERNAME = cur.fetchone()[0]
            cur.execute("SELECT room_name from chat.rooms where id = %s" , [val[1]])
            ROOMNAME = cur.fetchone()[0]
            names.append(USERNAME)
            time.append(val[3])
            messages.append(val[2])

        return render_template('enterRoom.html' ,id =  id , user = session['username'] , roomName = roomName , data = zip(names,time,messages))
    else:
        return render_template('roomLogin.html' ,id  = id , fail = 0)


