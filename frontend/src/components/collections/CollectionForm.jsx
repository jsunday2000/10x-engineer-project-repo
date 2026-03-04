import { useState } from "react";

import Button from "../shared/Button";

function CollectionForm({ onSubmit, isSubmitting }) {
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError("");

    if (!name.trim()) {
      setError("Collection name is required.");
      return;
    }

    await onSubmit({
      name: name.trim(),
      description: description.trim() || null,
    });

    setName("");
    setDescription("");
  };

  return (
    <section className="panel">
      <h2>New Collection</h2>
      <form className="collection-form" onSubmit={handleSubmit}>
        <label>
          <span>Name</span>
          <input
            type="text"
            value={name}
            maxLength={100}
            onChange={(event) => setName(event.target.value)}
            required
          />
        </label>

        <label>
          <span>Description</span>
          <textarea
            value={description}
            maxLength={500}
            rows={3}
            onChange={(event) => setDescription(event.target.value)}
          />
        </label>

        {error ? <p className="form-error">{error}</p> : null}

        <Button type="submit" variant="primary" isLoading={isSubmitting}>
          Add Collection
        </Button>
      </form>
    </section>
  );
}

export default CollectionForm;
