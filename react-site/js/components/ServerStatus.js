import React, { Component } from "react";
import DOMPurify from "dompurify";

class ServerStatus extends Component {
  constructor() {
    super();
  }

  getComponentHtml() {
    var html = "<h3>Server Status: ".concat(this.props.isRunning ? "Online" : "Offline").concat("</h3>"); 
    if (this.props.isRunning) {
      html = html.concat(" <br/> Server IP: ").concat(this.props.ipAddress);
    }
    return html
  }
  render() {
   
    return (
      <div dangerouslySetInnerHTML={{__html: DOMPurify.sanitize(this.getComponentHtml())}}/>
    );
  }
}

export default ServerStatus;