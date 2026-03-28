export default function PersonCard({ item }) {
  return (
    <div className="person-item">
      <strong>ID {item.person_id}</strong>
      <div>Status: {item.status}</div>
      <div>Confidence: {Number(item.confidence).toFixed(2)}</div>
      <div>Gait confidence: {Number(item.movement_confidence || 0).toFixed(2)}</div>
    </div>
  );
}