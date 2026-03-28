import PersonCard from "./PersonCard";

export default function ActiveIdSidebar({ activeIds }) {
  return (
    <div className="card">
      <h2>Currently Active IDs</h2>
      {activeIds.length === 0 ? (
        <p>No active IDs</p>
      ) : (
        activeIds.map((item) => <PersonCard key={item.person_id} item={item} />)
      )}
    </div>
  );
}