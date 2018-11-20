import React, { Component } from 'react';

class Room extends Component {
	constructor(props){
		super(props)
		console.log(props)

	}

	componentWillMount() {
        console.log("should ping socket here")
    }

    render() {
    	return (
            <div> Hello! This is room {this.props.room_id}
            </div>

        )
    }


}

export default Room;