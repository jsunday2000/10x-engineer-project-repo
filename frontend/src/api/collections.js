import { apiRequest } from "./client";

export const getCollections = () => {
  return apiRequest("/collections");
};

export const createCollection = (collectionData) => {
  return apiRequest("/collections", {
    method: "POST",
    data: collectionData,
  });
};

export const deleteCollection = (collectionId) => {
  return apiRequest(`/collections/${collectionId}`, {
    method: "DELETE",
  });
};
