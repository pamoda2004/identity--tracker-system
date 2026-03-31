import axios from "axios";
import { API_BASE } from "../utils/constants";

export const getUnknowns = () => axios.get(`${API_BASE}/unknowns`);

export const assignUnknownName = (unknown_id, name) =>
  axios.post(`${API_BASE}/unknowns/assign-name`, {
    unknown_id,
    name,
  });