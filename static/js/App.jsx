import React, { Component } from 'react';
import { Route, Switch } from 'react-router-dom';

import Homepage from "./Homepage.jsx"
import Custom from "./Custom.jsx"
import Room from "./Room.jsx"


class App extends Component {
    render() {
        console.log("rendering app")
        const App = () => (
            <div>
                <Switch>
                    <Route exact path="/" component={Homepage}/>
                    <Route exact path="/room" component={Custom}/>
                    <Route exact path="/room/:id" component={Room}/>
                </Switch>
            </div>
        )

        return (
            <App/>
        );
    }
}

export default App;
