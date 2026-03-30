import { useState } from "react";
import { API_BASE } from "../utils/constants";
import { assignUnknownName } from "../api/unknownApi";

export default function CaptureCard({ item }) {
  const [name, setName] = useState(item.assigned_name || "");
  const [status, setStatus] = useState("");

  const handleAssign = async () => {
    if (!name.trim()) {
      setStatus("Enter a name");
      return;
    }

    try {
      await assignUnknownName(item.unknown_id, name.trim());
      setStatus("Saved");
    } catch (error) {
      console.error(error);
      setStatus("Save failed");
    }
  };

  return (
    <div className="capture-card">
      <img
        src={`${API_BASE}${item.file_path}?t=${Date.now()}`}
        alt={item.file_name}
      />
      <div className="caption">{item.file_name}</div>
      <div className="caption">ID: {item.unknown_id}</div>

      <input
        type="text"
        value={name}
        placeholder="Enter person name"
        onChange={(e) => setName(e.target.value)}
        style={{
          width: "100%",
          marginTop: "8px",
          padding: "6px",
          borderRadius: "6px",
          border: "1px solid #374151"
        }}
      />

      <button
        onClick={handleAssign}
        style={{
          marginTop: "8px",
          width: "100%",
          padding: "8px",
          borderRadius: "6px",
          border: "none",
          cursor: "pointer"
        }}
      >
        Save Name
      </button>

      {item.assigned_name && (
        <div className="caption" style={{ marginTop: "6px" }}>
          Assigned: {item.assigned_name}
        </div>
      )}

      {status && (
        <div className="caption" style={{ marginTop: "6px" }}>
          {status}
        </div>
      )}
    </div>
  );
}