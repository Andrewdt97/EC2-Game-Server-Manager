import React, { Component } from "react";
import ReactDOM from "react-dom";

import {API_ENDPOINTS} from "../../api/api-endpoints.js";

class ServerInteraction extends Component {
  constructor() {
    super();

    this.state = {
      server_id: 'spigot', // This is a bad way to set default
      password: '',
      passwordIssue: false,
      awaiting_response: false,
    };

    this.handlePasswordSubmit = this.handlePasswordSubmit.bind(this);
    this.handlePasswordChange = this.handlePasswordChange.bind(this);
    this.handleServerChange = this.handleServerChange.bind(this);
    this.handleStopServer = this.handleStopServer.bind(this);
  }

  handleServerChange(event) {
    const newServer = event.target.value;
    this.setState({
      server_id : newServer
    });
  }

  handlePasswordChange(event) {
    const newPassowrd = event.target.value;
    this.setState({
      password : newPassowrd
    });
  }

  handlePasswordSubmit(event) {
    event.preventDefault();
    this.setState({
      awaiting_response: true,
    });
    const pw = this.state.password;
    const server = this.state.server_id;
    const url = API_ENDPOINTS["start_server"];
    fetch(url, {
      credentials: 'same-origin',
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({password : pw,
                            server_id: server}),
    })
      .then(res => res.json())
      .then(
        (data) => {
          this.setState({
            awaiting_response: false,
          })
        },
        (error) => {
        }
      )
  }

  handleStopServer(event) {
    event.preventDefault();
    const url = API_ENDPOINTS["stop_server"];
    fetch(url, {credentials: 'same-origin'})
      .then(res => res.json())
      .then(
        (data) => {},
        (error) => {}
      )
  }

  createServerItems() {
    let items = [];         
    for (let i = 0; i < this.props.servers.length; i++) {             
         items.push(<option key={this.props.servers[i]["key"]} value={this.props.servers[i]["key"]}>
           {this.props.servers[i]["name"]}
           </option>);   
    }
    return items;
  };

  getStartButton() {
    var opts = {}
    if (this.props.isRunning || this.state.awaiting_response) {
      opts["disabled"] = "disabled";
    }
    return (<input id="start-button" type="submit" 
      value="Start Server" onClick={this.handlePasswordSubmit} {...opts}/>)
  };

  getStopButton() {
    var opts = {}
    if (!this.props.isRunning) {
      opts["disabled"] = "disabled";
    }
    return (<input id="stop-button" type="submit" 
      value="Stop Server" onClick={this.handleStopServer} {...opts}/>)
  }

  render() {
    return (
        <form>
        <label htmlFor="pass">Password: </label>
        <input type="password" name="pass" value={this.state.password} onChange={this.handlePasswordChange}/>
        <br></br>
        <label htmlFor="pass">Server: </label>
        <select type="select" name="server-id" onChange={this.handleServerChange} value={this.state.server_id}>
          {this.createServerItems()}
        </select>
        {this.getStartButton()}
        {this.getStopButton()}
    </form>
    );
  }
}

export default ServerInteraction;