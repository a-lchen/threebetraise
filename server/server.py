from __future__ import print_function
import sys
from flask import Flask, render_template, request, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, join_room, emit, send
import json
import db
import random

"""init"""

app = Flask(__name__, static_folder="../static/dist", template_folder="../static")

database_file = "sqlite:///database.db"

app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)


socketio = SocketIO(app)


"""Database models"""

class User(db.Model, json.JSONEncoder):
    user_id = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    username = db.Column(db.String(80))
    def __init__(self, user_id, username):
        self.user_id = user_id
        self.username = username

    def to_dict(self):
        return {"user_id": self.user_id, "username": self.username}

    def __repr__(self):
        print("printing a user")
        print (self.__dict__)
        return json.dumps({"user_id": self.user_id, "username": self.username})



""" Variables """

rooms = {} # Room Id to Room


@app.route("/hello")
def hello():
    return "Hello World2!"



""" Routes """

# @app.route("/room/<int:room_id>")
# def show_room(room_id):
#     # id = request.cookies.get('session')
#     # on_join(id, room_id)
#     return "Hi You're in room " + str(room_id)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    name = request.cookies.get('session')
    print ("caught in path")
    if name:
        print (name)
    return render_template("index.html")
	

""" API """

@app.route('/api/set_username', methods = ['POST'])
def set_cookie():
    print ("setting cookie")
    print (request.get_json())
    resp = make_response(jsonify({"success": True}))
    id = str(random.randint(0,90000))
    resp.set_cookie('session', id)
    # db.insert_user(id, request.get_json()['username'])
    user = User(user_id=id, username=request.get_json()['username'])
    db.session.add(user)
    db.session.commit()
    return (resp)

@app.route('/api/get_user', methods = ['GET'])
def get_user():
    id = request.cookies.get('session')
    # user = db.get_user(id)
    user = User.query.filter_by(user_id=id).first()
    print ("Getting a user")
    print ("got user")
    print (user)
    print ("hi")
    return make_response(jsonify({"success" : True, "user": user.to_dict()}))

"""Room mechanics"""


@socketio.on('join')
def join_or_create_game_room(data):
    id = request.cookies.get('session')
    print (data)
    room = data["room"]
    if (room in rooms):
        rooms[room].append(id)
    else:
        rooms[room] = [id]
    print ("attempting to have user " + str(id) + "join room " + str(room))
    join_room(str(room))
    print (id + "joined room " + str(room))
    print("current occupants include: " + str(rooms[room]))
    emit("join_room", {"user_id": id, "current_occupants": rooms[room]}, room=room)

# currently not in use
@socketio.on('leave')
def on_leave(data):
    id = request.cookies.get('session')
    room = data['room']
    leave_room(room)
    send(id + ' has left the room.', room=room)


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected ' + request.cookies.get('session'))

if __name__ == '__main__':
    socketio.run(app)