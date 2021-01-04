import React, { Component } from "react";
import ReactDOM from "react-dom";

import ServerStatus from "./ServerStatus.js"
import ServerInteraction from "./ServerInteraction.js"

import {API_ENDPOINTS} from "../../api/api-endpoints.js"

class ServerInterface extends Component {
  constructor() {
    super();

    this.state = {
      "isRunning": false,
      "ipAddress": null,
      "servers": [],
    };

  }

  componentDidMount() {
    this.fetchServerList();
    this.fetchServerStatus();
    this.timer = setInterval(() => this.fetchServerStatus(), 5000);
  }

  componentWillUnmount() {
    clearInterval(this.timer);
    this.timer = null;
  }

  fetchServerList() {
    fetch(API_ENDPOINTS["get_configs"])
      .then(res => res.json())
      .then(
        (result) => {
          this.setState({
            servers: result.servers
          });
        },
        (error) => {
        }
      )
  }

  fetchServerStatus() {
    fetch(API_ENDPOINTS["server_status"])
      .then(res => res.json())
      .then(
        (result) => {
          this.setState({
            isLoaded: true,
            isRunning: result.isRunning,
            ipAddress: result.ipAdress,
          });
        },
        (error) => {
          this.setState({
            isLoaded: true,
            error
          });
        }
      )
  }

  render() {
    return (
      <div>
        <ServerStatus isRunning={this.state.isRunning} ipAddress={this.state.ipAddress}/>
        <ServerInteraction servers={this.state.servers} isRunning={this.state.isRunning}/>
      </div>
    );
  }
}

export default ServerInterface;

const wrapper = document.getElementById("container");
wrapper ? ReactDOM.render(<ServerInterface />, wrapper) : false;