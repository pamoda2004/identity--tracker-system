import { API_BASE } from "../utils/constants";

export default function CaptureCard({ item }) {
  return (
    <div className="capture-card">
      <img
        src={`${API_BASE}${item.file_path}?t=${Date.now()}`}
        alt={item.file_name}
      />
      <div className="caption">{item.file_name}</div>
    </div>
  );
}