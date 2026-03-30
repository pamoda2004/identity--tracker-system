import axios from "axios";

const API_BASE = "http://127.0.0.1:8000";

export async function startVideo() {
  const res = await axios.post(`${API_BASE}/video/start`);
  return res.data;
}

export async function stopVideo() {
  const res = await axios.post(`${API_BASE}/video/stop`);
  return res.data;
}

export async function getFrame() {
  const res = await axios.get(`${API_BASE}/tracker/frame`);
  return res.data;
}

export async function getUnknowns() {
  const res = await axios.get(`${API_BASE}/unknowns`);
  return res.data;
}