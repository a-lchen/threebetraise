import React, { Component } from 'react';
import { Route, Switch } from 'react-router-dom';

import Homepage from "./Homepage.jsx"
import Custom from "./Custom.jsx"

class App extends Component {
    render() {
        const App = () => (
            <div>
                <Switch>
                    <Route exact path="/" component={Homepage}/>
                    <Route exact path="/custom" component={Custom}/>
                </Switch>
            </div>
        )

        return (
            <App/>
        );
    }
}

export default App;
