import React, { Component } from 'react';
import io from 'socket.io-client'



var socket = io()

class Room extends Component {
	constructor(props){
		super(props)
		console.log(props.match.params['room_id'])


	}

	componentWillMount() {
        console.log("should ping socket here")
        socket.emit("join", {room: this.props.match.params['room_id']})
        socket.on('join_room', function(data) {
	        console.log("a client connected he is " + data['user_id'])
	        console.log("now the occupants of the room are" + data['current_occupants'])
	    });

    }

    render() {
    	return (
            <div> Hello! This is room {this.props.match.params['room_id']}
            </div>

        )
    }


}

export default Room;