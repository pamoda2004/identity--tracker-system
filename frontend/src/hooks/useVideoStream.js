import { useRef, useState } from "react";
import { startVideo, stopVideo } from "../api/videoApi";
import { getFrame } from "../api/trackerApi";
import { API_BASE } from "../utils/constants";

export default function useVideoStream() {
  const [frameUrl, setFrameUrl] = useState("");
  const [activeIds, setActiveIds] = useState([]);
  const [unknowns, setUnknowns] = useState([]);
  const [running, setRunning] = useState(false);
  const [message, setMessage] = useState("");
  const timerRef = useRef(null);

  const fetchFrame = async () => {
    try {
      const res = await getFrame();
      const data = res.data;

      if (data.frame_url) {
        setFrameUrl(`${API_BASE}${data.frame_url}?t=${Date.now()}`);
      }
      setActiveIds(data.active_ids || []);
      setUnknowns(data.unknown_captures || []);
      setMessage(data.message || "");
    } catch {
      setMessage("Backend connection error");
    }
  };

  const handleStart = async () => {
    await startVideo();
    setRunning(true);
    setMessage("");
    fetchFrame();

    if (timerRef.current) clearInterval(timerRef.current);
    timerRef.current = setInterval(fetchFrame, 500);
  };

  const handleStop = async () => {
    await stopVideo();
    setRunning(false);
    if (timerRef.current) clearInterval(timerRef.current);
  };

  return {
    frameUrl,
    activeIds,
    unknowns,
    running,
    message,
    handleStart,
    handleStop,
  };
}