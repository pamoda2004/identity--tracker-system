import Header from "../components/Header";
import VideoFeed from "../components/VideoFeed";
import ActiveIdSidebar from "../components/ActiveIdSidebar";
import UnknownGallery from "../components/UnknownGallery";
import useVideoStream from "../hooks/useVideoStream";

export default function Dashboard() {
  const {
    frameUrl,
    activeIds,
    unknowns,
    running,
    message,
    handleStart,
    handleStop,
  } = useVideoStream();

  return (
    <div className="page">
      <Header running={running} onStart={handleStart} onStop={handleStop} />
      {message && <p style={{ marginBottom: "12px" }}>{message}</p>}

      <div className="layout">
        <VideoFeed frameUrl={frameUrl} />
        <aside className="sidebar">
          <ActiveIdSidebar activeIds={activeIds} />
          <UnknownGallery unknowns={unknowns} />
        </aside>
      </div>
    </div>
  );
}