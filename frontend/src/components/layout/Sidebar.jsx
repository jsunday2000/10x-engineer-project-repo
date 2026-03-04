import CollectionForm from "../collections/CollectionForm";
import CollectionList from "../collections/CollectionList";

function Sidebar({
  collections,
  selectedCollectionId,
  onSelectCollection,
  onDeleteCollection,
  onCreateCollection,
  isLoading,
  isSubmitting,
  promptCountsByCollection,
}) {
  return (
    <div className="sidebar-stack">
      <CollectionForm onSubmit={onCreateCollection} isSubmitting={isSubmitting} />
      <CollectionList
        collections={collections}
        selectedCollectionId={selectedCollectionId}
        onSelect={onSelectCollection}
        onDelete={onDeleteCollection}
        isLoading={isLoading}
        promptCountsByCollection={promptCountsByCollection}
      />
    </div>
  );
}

export default Sidebar;
