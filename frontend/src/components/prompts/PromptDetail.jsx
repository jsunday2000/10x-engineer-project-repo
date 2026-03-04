import Button from "../shared/Button";

function PromptDetail({ prompt, collectionName, onEdit, onDelete }) {
  if (!prompt) {
    return (
      <section className="panel empty-state">
        <h2>Prompt not available</h2>
        <p>Select a prompt from the list to see details.</p>
      </section>
    );
  }

  return (
    <section className="panel prompt-detail">
      <div className="prompt-detail-header">
        <div>
          <h2>{prompt.title}</h2>
          <p className="prompt-detail-collection">Collection: {collectionName}</p>
        </div>
        <div className="prompt-detail-actions">
          <Button variant="secondary" onClick={onEdit}>
            Edit
          </Button>
          <Button variant="danger" onClick={onDelete}>
            Delete
          </Button>
        </div>
      </div>

      <div className="prompt-detail-body">
        <h3>Description</h3>
        <p>{prompt.description || "No description"}</p>

        <h3>Content</h3>
        <pre>{prompt.content}</pre>
      </div>
    </section>
  );
}

export default PromptDetail;
