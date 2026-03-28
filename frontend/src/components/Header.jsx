export default function Header({ running, onStart, onStop }) {
  return (
    <header className="header">
      <h1>Persistent Identity Tracker</h1>
      <div className="actions">
        <button onClick={onStart} disabled={running}>Start</button>
        <button onClick={onStop} disabled={!running}>Stop</button>
      </div>
    </header>
  );
}