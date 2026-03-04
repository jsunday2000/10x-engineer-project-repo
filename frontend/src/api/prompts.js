import { apiRequest } from "./client";

export const getPrompts = ({ collectionId, search } = {}) => {
  return apiRequest("/prompts", {
    query: {
      collection_id: collectionId,
      search,
    },
  });
};

export const getPrompt = (promptId) => {
  return apiRequest(`/prompts/${promptId}`);
};

export const createPrompt = (promptData) => {
  return apiRequest("/prompts", {
    method: "POST",
    data: promptData,
  });
};

export const replacePrompt = (promptId, promptData) => {
  return apiRequest(`/prompts/${promptId}`, {
    method: "PUT",
    data: promptData,
  });
};

export const patchPrompt = (promptId, promptData) => {
  return apiRequest(`/prompts/${promptId}`, {
    method: "PATCH",
    data: promptData,
  });
};

export const deletePrompt = (promptId) => {
  return apiRequest(`/prompts/${promptId}`, {
    method: "DELETE",
  });
};
