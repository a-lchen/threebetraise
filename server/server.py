from __future__ import print_function
import sys
from flask import Flask, render_template, request, make_response, jsonify
from flask_socketio import SocketIO, join_room, emit
import db
import random

app = Flask(__name__, static_folder="../static/dist", template_folder="../static")
socketio = SocketIO(app)


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
    db.insert_user(id, request.get_json()['username'])
    return (resp)

@app.route('/api/get_user', methods = ['GET'])
def get_user():
    id = request.cookies.get('session')
    user = db.get_user(id)
    print ("Getting a user")
    return make_response(jsonify({"success" : True, "user": user}))

"""Room mechanics"""

# @socketio.on('create')
# def on_create(data):
#     """Create a lobby"""
#     ROOMS[room] = gm
#     join_room(room)
#     emit('join_room', {'room': room})


@socketio.on('join')
def on_join(room, user_id):
    print ("attempting to have user " + str(user_id) + "join room " + str(room))
    join_room(str(room))
    print (user_id + "joined room " + str(room))
    send(user_id + ' has entered the room.', room=room)

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    send(username + ' has left the room.', room=room)

if __name__ == '__main__':
    socketio.run(app)