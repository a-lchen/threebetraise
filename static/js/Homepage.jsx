import React, { Component } from 'react';
import * as Cookies from 'js-cookie';

class Homepage extends Component {

	constructor(props) {
        super(props);

        this.state = {
            username: undefined
        };

        this.onEnterKeyPress = this.onEnterKeyPress.bind(this);

    }

    fetchUserInfo(){
    	console.log("fetching")
	    let session = Cookies.get('session');
        if (session){
            console.log("found a cookie: it is " + session)
            fetch('/api/get_user', {
                method: 'GET'
            }).then(res => res.json()).then(resJson => {
                console.log(resJson)
                if (resJson.success) {
                    this.setState({
                        username: resJson.user.username,
                    });

                    console.log(this.state)
                } else {
                    // user has session but is not in database, cookie has been cleared by server
                    console.log("server issue...")

                }
            });
        }
    }


    checkOrRegisterUser() {
        let newName = document.getElementById("username").value;
        fetch('/api/set_username', {
            method: 'POST',
            credentials: 'include',

          	headers : { 
					    'Content-Type': 'application/json',
					    'Accept': 'application/json'
            },
            body: JSON.stringify({username: newName})
        }).then(res => res.json()).then(resJson => { // returns a promise with resolve value true if username is valid, false if not
            console.log(resJson)
            if (resJson.success) { // successfully registered
                console.log(resJson);
                this.setState({
                    username: resJson.username
                });
                document.getElementById("username").disabled = true;
            } else { // failed to register
                console.log("Failed to register")
                document.getElementById("username").focus();
            }

        });

    };

    onEnterKeyPress(e) {
        if (e.charCode === 13) {
            console.log("key press enter");
            e.preventDefault();
            this.checkOrRegisterUser();
            document.getElementById("username").blur();
        }
    };


    componentWillMount() {
        this.fetchUserInfo()
    }

    render() {

        return (
            <div> Hello! This is the homepage! :Dsdssdgasdgsd:)

                <form onKeyPress={this.onEnterKeyPress} action="#" >
                    <input disabled={this.state.username ? true : undefined} id="username" placeholder="Username" value={this.state.username}>
                    </input>
                </form>
            </div>

        )
    }


}

export default Homepage;