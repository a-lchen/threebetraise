from __future__ import print_function
import sys
from flask import Flask, render_template, request, make_response, jsonify



app = Flask(__name__, static_folder="../static/dist", template_folder="../static")

@app.route("/hello")
def hello():
    return "Hello World2!"

@app.route('/api/set_username', methods = ['POST'])
def set_cookie():
    print ("setting cookie")
    print (request, file=sys.stderr)
    resp = make_response(jsonify({"success": True}))
    resp.set_cookie('session', 'cookie5')
    return (resp)

@app.route('/api/get_user', methods = ['GET'])
def get_user():
    print ("Getting a user")
    return make_response(jsonify({"success" : True, "username": "placeholder"}))


@app.route("/room/<int:room_id>")
def show_room(room_id):
	return "Hi You're in room " + str(room_id)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
	name = request.cookies.get('session')
	print ("Hi")
	print ("hi1", file=sys.stderr)
	if name:
		print (name, file=sys.stderr)
	return render_template("index.html")
	
if __name__ == '__main__':
    app.run()