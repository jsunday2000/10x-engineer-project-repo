import { useCallback, useEffect, useMemo, useState } from "react";

import {
  createPrompt,
  deletePrompt,
  getPrompts,
  patchPrompt,
} from "./api/prompts";
import {
  createCollection,
  deleteCollection,
  getCollections,
} from "./api/collections";
import Layout from "./components/layout/Layout";
import Header from "./components/layout/Header";
import Sidebar from "./components/layout/Sidebar";
import PromptList from "./components/prompts/PromptList";
import PromptDetail from "./components/prompts/PromptDetail";
import PromptForm from "./components/prompts/PromptForm";
import Modal from "./components/shared/Modal";
import ErrorMessage from "./components/shared/ErrorMessage";
import Notification from "./components/shared/Notification";

const VIEW_LIST = "list";
const VIEW_CREATE = "create";
const VIEW_DETAIL = "detail";
const VIEW_EDIT = "edit";

function App() {
  const [prompts, setPrompts] = useState([]);
  const [collections, setCollections] = useState([]);
  const [selectedPromptId, setSelectedPromptId] = useState(null);
  const [selectedCollectionId, setSelectedCollectionId] = useState("");
  const [searchQuery, setSearchQuery] = useState("");
  const [view, setView] = useState(VIEW_LIST);

  const [isLoadingPrompts, setIsLoadingPrompts] = useState(false);
  const [isLoadingCollections, setIsLoadingCollections] = useState(false);
  const [isSubmittingPrompt, setIsSubmittingPrompt] = useState(false);
  const [isSubmittingCollection, setIsSubmittingCollection] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);

  const [error, setError] = useState("");
  const [notification, setNotification] = useState(null);
  const [confirmDialog, setConfirmDialog] = useState(null);

  const selectedPrompt = useMemo(
    () => prompts.find((prompt) => prompt.id === selectedPromptId) || null,
    [prompts, selectedPromptId],
  );

  const collectionNameById = useMemo(() => {
    return collections.reduce((accumulator, collection) => {
      accumulator[collection.id] = collection.name;
      return accumulator;
    }, {});
  }, [collections]);

  const promptCountsByCollection = useMemo(() => {
    return prompts.reduce((accumulator, prompt) => {
      if (prompt.collection_id) {
        accumulator[prompt.collection_id] =
          (accumulator[prompt.collection_id] || 0) + 1;
      }
      return accumulator;
    }, {});
  }, [prompts]);

  const showNotification = useCallback((type, message) => {
    setNotification({ type, message });
  }, []);

  const loadCollections = useCallback(async () => {
    setIsLoadingCollections(true);
    try {
      const response = await getCollections();
      setCollections(response.collections);
    } catch (apiError) {
      setError(apiError.message || "Failed to load collections.");
    } finally {
      setIsLoadingCollections(false);
    }
  }, []);

  const loadPrompts = useCallback(
    async (filters = {}) => {
      const collectionId =
        filters.collectionId !== undefined
          ? filters.collectionId
          : selectedCollectionId;
      const search = filters.search !== undefined ? filters.search : searchQuery;

      setIsLoadingPrompts(true);
      setError("");
      try {
        const response = await getPrompts({ collectionId, search });
        setPrompts(response.prompts);

        if (
          selectedPromptId &&
          !response.prompts.some((prompt) => prompt.id === selectedPromptId)
        ) {
          setSelectedPromptId(null);
          setView(VIEW_LIST);
        }
      } catch (apiError) {
        setError(apiError.message || "Failed to load prompts.");
      } finally {
        setIsLoadingPrompts(false);
      }
    },
    [searchQuery, selectedCollectionId, selectedPromptId],
  );

  useEffect(() => {
    void loadCollections();
  }, [loadCollections]);

  useEffect(() => {
    const debounceId = setTimeout(() => {
      void loadPrompts();
    }, 250);

    return () => {
      clearTimeout(debounceId);
    };
  }, [loadPrompts, searchQuery, selectedCollectionId]);

  useEffect(() => {
    if (!notification) {
      return undefined;
    }

    const timeoutId = setTimeout(() => {
      setNotification(null);
    }, 3500);

    return () => {
      clearTimeout(timeoutId);
    };
  }, [notification]);

  const handleCreatePrompt = async (formData) => {
    setIsSubmittingPrompt(true);
    try {
      const createdPrompt = await createPrompt(formData);
      showNotification("success", "Prompt created successfully.");
      setSelectedPromptId(createdPrompt.id);
      setView(VIEW_DETAIL);
      await loadPrompts();
    } catch (apiError) {
      showNotification("error", apiError.message || "Failed to create prompt.");
    } finally {
      setIsSubmittingPrompt(false);
    }
  };

  const handleUpdatePrompt = async (formData) => {
    if (!selectedPromptId) {
      return;
    }

    setIsSubmittingPrompt(true);
    try {
      await patchPrompt(selectedPromptId, formData);
      showNotification("success", "Prompt updated successfully.");
      setView(VIEW_DETAIL);
      await loadPrompts();
    } catch (apiError) {
      showNotification("error", apiError.message || "Failed to update prompt.");
    } finally {
      setIsSubmittingPrompt(false);
    }
  };

  const handleDeletePrompt = async (promptId) => {
    setIsDeleting(true);
    try {
      await deletePrompt(promptId);
      showNotification("success", "Prompt deleted successfully.");
      if (selectedPromptId === promptId) {
        setSelectedPromptId(null);
        setView(VIEW_LIST);
      }
      await loadPrompts();
    } catch (apiError) {
      showNotification("error", apiError.message || "Failed to delete prompt.");
    } finally {
      setIsDeleting(false);
      setConfirmDialog(null);
    }
  };

  const handleCreateCollection = async (formData) => {
    setIsSubmittingCollection(true);
    try {
      await createCollection(formData);
      showNotification("success", "Collection created successfully.");
      await loadCollections();
      await loadPrompts();
    } catch (apiError) {
      showNotification(
        "error",
        apiError.message || "Failed to create collection.",
      );
    } finally {
      setIsSubmittingCollection(false);
    }
  };

  const handleDeleteCollection = async (collection) => {
    setIsDeleting(true);
    try {
      await deleteCollection(collection.id);
      showNotification(
        "success",
        `Collection "${collection.name}" deleted successfully.`,
      );
      if (selectedCollectionId === collection.id) {
        setSelectedCollectionId("");
      }
      await loadCollections();
      await loadPrompts({ collectionId: "" });
    } catch (apiError) {
      showNotification(
        "error",
        apiError.message || "Failed to delete collection.",
      );
    } finally {
      setIsDeleting(false);
      setConfirmDialog(null);
    }
  };

  const openDeletePromptModal = (prompt) => {
    setConfirmDialog({
      type: "prompt",
      item: prompt,
      title: "Delete prompt",
      message: `Delete "${prompt.title}"? This action cannot be undone.`,
      confirmLabel: "Delete Prompt",
    });
  };

  const openDeleteCollectionModal = (collection) => {
    setConfirmDialog({
      type: "collection",
      item: collection,
      title: "Delete collection",
      message:
        `Delete "${collection.name}"? This will also delete all prompts in this collection.`,
      confirmLabel: "Delete Collection",
    });
  };

  const handleConfirmDelete = async () => {
    if (!confirmDialog) {
      return;
    }

    if (confirmDialog.type === "prompt") {
      await handleDeletePrompt(confirmDialog.item.id);
      return;
    }

    await handleDeleteCollection(confirmDialog.item);
  };

  const handleSelectPrompt = (promptId) => {
    setSelectedPromptId(promptId);
    setView(VIEW_DETAIL);
  };

  const handleStartCreate = () => {
    setView(VIEW_CREATE);
  };

  const handleStartEdit = (prompt) => {
    setSelectedPromptId(prompt.id);
    setView(VIEW_EDIT);
  };

  const handleCancelForm = () => {
    if (selectedPromptId) {
      setView(VIEW_DETAIL);
      return;
    }
    setView(VIEW_LIST);
  };

  const handleRefresh = async () => {
    await Promise.all([loadCollections(), loadPrompts()]);
    showNotification("success", "Data refreshed.");
  };

  return (
    <>
      <Layout
        header={
          <Header
            searchQuery={searchQuery}
            onSearchChange={setSearchQuery}
            onCreatePrompt={handleStartCreate}
            onRefresh={handleRefresh}
            isRefreshing={isLoadingPrompts || isLoadingCollections}
          />
        }
        sidebar={
          <Sidebar
            collections={collections}
            selectedCollectionId={selectedCollectionId}
            onSelectCollection={setSelectedCollectionId}
            onDeleteCollection={openDeleteCollectionModal}
            onCreateCollection={handleCreateCollection}
            isLoading={isLoadingCollections}
            isSubmitting={isSubmittingCollection}
            promptCountsByCollection={promptCountsByCollection}
          />
        }
      >
        {error ? <ErrorMessage message={error} onDismiss={() => setError("")} /> : null}

        {view === VIEW_CREATE ? (
          <PromptForm
            title="Create Prompt"
            submitLabel="Create Prompt"
            collections={collections}
            onSubmit={handleCreatePrompt}
            onCancel={handleCancelForm}
            isSubmitting={isSubmittingPrompt}
          />
        ) : null}

        {view === VIEW_EDIT && selectedPrompt ? (
          <PromptForm
            title="Edit Prompt"
            submitLabel="Save Changes"
            collections={collections}
            initialData={selectedPrompt}
            onSubmit={handleUpdatePrompt}
            onCancel={handleCancelForm}
            isSubmitting={isSubmittingPrompt}
          />
        ) : null}

        {view === VIEW_DETAIL && selectedPrompt ? (
          <PromptDetail
            prompt={selectedPrompt}
            collectionName={collectionNameById[selectedPrompt.collection_id] || "Unassigned"}
            onEdit={() => handleStartEdit(selectedPrompt)}
            onDelete={() => openDeletePromptModal(selectedPrompt)}
          />
        ) : null}

        {view === VIEW_LIST ? (
          <PromptList
            prompts={prompts}
            selectedPromptId={selectedPromptId}
            collectionsById={collectionNameById}
            onSelect={handleSelectPrompt}
            onEdit={(prompt) => handleStartEdit(prompt)}
            onDelete={(prompt) => openDeletePromptModal(prompt)}
            isLoading={isLoadingPrompts}
          />
        ) : null}
      </Layout>

      <Notification
        notification={notification}
        onClose={() => setNotification(null)}
      />

      <Modal
        isOpen={Boolean(confirmDialog)}
        title={confirmDialog?.title || "Confirm"}
        onClose={() => setConfirmDialog(null)}
        onConfirm={handleConfirmDelete}
        confirmLabel={confirmDialog?.confirmLabel || "Confirm"}
        isConfirmLoading={isDeleting}
      >
        <p className="modal-message">{confirmDialog?.message}</p>
      </Modal>
    </>
  );
}

export default App;
