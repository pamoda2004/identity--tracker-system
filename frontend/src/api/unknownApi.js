import axios from "axios";
import { API_BASE } from "../utils/constants";

export const getUnknowns = () => axios.get(`${API_BASE}/unknowns`);