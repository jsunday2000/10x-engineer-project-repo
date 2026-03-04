import PromptCard from "./PromptCard";
import LoadingSpinner from "../shared/LoadingSpinner";

function PromptList({
  prompts,
  selectedPromptId,
  collectionsById,
  onSelect,
  onEdit,
  onDelete,
  isLoading,
}) {
  if (isLoading) {
    return <LoadingSpinner label="Loading prompts..." />;
  }

  if (!prompts.length) {
    return (
      <section className="panel empty-state">
        <h2>No prompts found</h2>
        <p>Create your first prompt or adjust your search and filters.</p>
      </section>
    );
  }

  return (
    <section className="prompt-list">
      {prompts.map((prompt) => (
        <PromptCard
          key={prompt.id}
          prompt={prompt}
          collectionName={collectionsById[prompt.collection_id]}
          isSelected={selectedPromptId === prompt.id}
          onSelect={() => onSelect(prompt.id)}
          onEdit={() => onEdit(prompt)}
          onDelete={() => onDelete(prompt)}
        />
      ))}
    </section>
  );
}

export default PromptList;
