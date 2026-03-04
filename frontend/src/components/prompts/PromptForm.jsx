import { useEffect, useState } from "react";

import Button from "../shared/Button";

const emptyForm = {
  title: "",
  content: "",
  description: "",
  collection_id: "",
};

function PromptForm({
  title,
  submitLabel,
  collections,
  initialData,
  onSubmit,
  onCancel,
  isSubmitting,
}) {
  const [formData, setFormData] = useState(emptyForm);
  const [formError, setFormError] = useState("");

  useEffect(() => {
    if (initialData) {
      setFormData({
        title: initialData.title || "",
        content: initialData.content || "",
        description: initialData.description || "",
        collection_id: initialData.collection_id || "",
      });
      return;
    }
    setFormData(emptyForm);
  }, [initialData]);

  const handleChange = (field, value) => {
    setFormData((previous) => ({ ...previous, [field]: value }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setFormError("");

    if (!formData.title.trim()) {
      setFormError("Title is required.");
      return;
    }

    if (!formData.content.trim()) {
      setFormError("Content is required.");
      return;
    }

    await onSubmit({
      title: formData.title.trim(),
      content: formData.content.trim(),
      description: formData.description.trim() || null,
      collection_id: formData.collection_id || null,
    });
  };

  return (
    <section className="panel">
      <h2>{title}</h2>
      <form className="prompt-form" onSubmit={handleSubmit}>
        <label>
          <span>Title</span>
          <input
            type="text"
            value={formData.title}
            maxLength={200}
            onChange={(event) => handleChange("title", event.target.value)}
            required
          />
        </label>

        <label>
          <span>Description</span>
          <input
            type="text"
            value={formData.description}
            maxLength={500}
            onChange={(event) => handleChange("description", event.target.value)}
          />
        </label>

        <label>
          <span>Collection</span>
          <select
            value={formData.collection_id}
            onChange={(event) => handleChange("collection_id", event.target.value)}
          >
            <option value="">Unassigned</option>
            {collections.map((collection) => (
              <option key={collection.id} value={collection.id}>
                {collection.name}
              </option>
            ))}
          </select>
        </label>

        <label>
          <span>Prompt Content</span>
          <textarea
            value={formData.content}
            onChange={(event) => handleChange("content", event.target.value)}
            rows={10}
            required
          />
        </label>

        {formError ? <p className="form-error">{formError}</p> : null}

        <div className="form-actions">
          <Button variant="secondary" onClick={onCancel}>
            Cancel
          </Button>
          <Button type="submit" variant="primary" isLoading={isSubmitting}>
            {submitLabel}
          </Button>
        </div>
      </form>
    </section>
  );
}

export default PromptForm;
