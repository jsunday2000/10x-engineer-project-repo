import Button from "../shared/Button";

function PromptCard({
  prompt,
  collectionName,
  isSelected,
  onSelect,
  onEdit,
  onDelete,
}) {
  return (
    <article
      className={`prompt-card ${isSelected ? "prompt-card-selected" : ""}`}
      onClick={onSelect}
      onKeyDown={(event) => {
        if (event.key === "Enter") {
          onSelect();
        }
      }}
      role="button"
      tabIndex={0}
      aria-label={`Open prompt ${prompt.title}`}
    >
      <div className="prompt-card-header">
        <h3>{prompt.title}</h3>
        <span className="prompt-chip">{collectionName || "Unassigned"}</span>
      </div>

      <p className="prompt-card-description">{prompt.description || "No description"}</p>

      <p className="prompt-card-content">{prompt.content}</p>

      <div className="prompt-card-actions">
        <Button
          variant="secondary"
          size="sm"
          onClick={(event) => {
            event.stopPropagation();
            onEdit();
          }}
        >
          Edit
        </Button>
        <Button
          variant="danger"
          size="sm"
          onClick={(event) => {
            event.stopPropagation();
            onDelete();
          }}
        >
          Delete
        </Button>
      </div>
    </article>
  );
}

export default PromptCard;
