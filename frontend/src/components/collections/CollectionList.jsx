import Button from "../shared/Button";
import LoadingSpinner from "../shared/LoadingSpinner";

function CollectionList({
  collections,
  selectedCollectionId,
  onSelect,
  onDelete,
  isLoading,
  promptCountsByCollection,
}) {
  if (isLoading) {
    return <LoadingSpinner label="Loading collections..." />;
  }

  return (
    <section className="panel collection-list-panel">
      <h2>Collections</h2>

      <button
        type="button"
        className={`collection-item ${selectedCollectionId === "" ? "selected" : ""}`}
        onClick={() => onSelect("")}
      >
        <span>All Prompts</span>
      </button>

      {!collections.length ? (
        <p className="empty-note">No collections yet.</p>
      ) : (
        <ul className="collection-list" aria-label="Collections">
          {collections.map((collection) => (
            <li key={collection.id}>
              <button
                type="button"
                className={`collection-item ${
                  selectedCollectionId === collection.id ? "selected" : ""
                }`}
                onClick={() => onSelect(collection.id)}
              >
                <span>{collection.name}</span>
                <span className="count-pill">
                  {promptCountsByCollection[collection.id] || 0}
                </span>
              </button>
              <Button
                variant="ghost"
                size="sm"
                className="collection-delete"
                onClick={() => onDelete(collection)}
              >
                Delete
              </Button>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}

export default CollectionList;
