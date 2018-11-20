import React, { Component } from 'react';

class Room extends Component {
	constructor(props){
		super(props)
		console.log(props.match.params['id'])

	}

	componentWillMount() {
        console.log("should ping socket here")
    }

    render() {
    	return (
            <div> Hello! This is room {this.props.match.params['id']}
            </div>

        )
    }


}

export default Room;