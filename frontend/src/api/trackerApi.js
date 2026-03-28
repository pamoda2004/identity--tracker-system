import axios from "axios";
import { API_BASE } from "../utils/constants";

export const getFrame = () => axios.get(`${API_BASE}/tracker/frame`);
export const getActiveIds = () => axios.get(`${API_BASE}/tracker/active-ids`);