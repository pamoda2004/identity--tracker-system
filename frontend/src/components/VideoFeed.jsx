export default function VideoFeed({ frameUrl }) {
  return (
    <section className="video-panel">
      <h2>Video Feed</h2>
      {frameUrl ? (
        <img src={frameUrl} alt="Processed frame" className="video-frame" />
      ) : (
        <div className="placeholder">No frame yet</div>
      )}
    </section>
  );
}