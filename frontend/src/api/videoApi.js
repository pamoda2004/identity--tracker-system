import axios from "axios";
import { API_BASE } from "../utils/constants";

export const startVideo = () => axios.post(`${API_BASE}/video/start`);
export const stopVideo = () => axios.post(`${API_BASE}/video/stop`);