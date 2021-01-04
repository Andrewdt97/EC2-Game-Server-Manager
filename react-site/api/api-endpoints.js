import {API_ROOT} from "./api-config";

export const API_ENDPOINTS = {
    get_configs: `${API_ROOT}/get-servers`,
    server_status: `${API_ROOT}/server-status`,
    start_server:  `${API_ROOT}/start-server`,
    stop_server:  `${API_ROOT}/stop-server`,
}