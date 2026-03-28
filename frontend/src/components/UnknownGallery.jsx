import CaptureCard from "./CaptureCard";

export default function UnknownGallery({ unknowns }) {
  return (
    <div className="card">
      <h2>Unlabeled Captures</h2>
      <div className="gallery">
        {unknowns.map((item, idx) => (
          <CaptureCard key={`${item.file_name}-${idx}`} item={item} />
        ))}
      </div>
    </div>
  );
}