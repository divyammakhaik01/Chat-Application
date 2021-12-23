from app import app
from flask import  *
from models import subject,user
from flask_mysqldb import MySQL
# from project.models import user
chat_route = Blueprint("chat_route" , __name__ )

mysql = MySQL()

@chat_route.route("/chats")
def chats():
    return render_template('enterRoom.html')


