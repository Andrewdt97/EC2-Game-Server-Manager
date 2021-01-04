// Code courtsey of David Ceddia
// https://daveceddia.com/multiple-environments-with-react/
let backendHost;
const apiVersion = 'v1';
const productionHostname = "";
const productionApiHostname = "";

const hostname = window && window.location && window.location.hostname;

if(hostname === productionHostname) {
  backendHost = productionApiHostname;
} else {
  backendHost = process.env.REACT_APP_BACKEND_HOST || 'http://localhost:8000';
}

export const API_ROOT = `${backendHost}/minecraft/api/${apiVersion}`;