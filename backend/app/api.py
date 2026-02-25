"""FastAPI routes for PromptLab"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

from app.models import (
    Prompt, PromptCreate, PromptUpdate,
    Collection, CollectionCreate,
    PromptList, PromptVersion, PromptVersionList,
    CollectionList, HealthResponse,
    get_current_time
)
from app.storage import storage
from app.utils import sort_prompts_by_date, filter_prompts_by_collection, search_prompts
from app import __version__


app = FastAPI(
    title="PromptLab API",
    description="AI Prompt Engineering Platform",
    version=__version__
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============== Health Check ==============

@app.get("/health", response_model=HealthResponse)
def health_check():
    """Health check endpoint for API status.

    Verifies that the API is running and accessible.

    Returns:
        HealthResponse: Object containing status and current API version.
            status: Always returns 'healthy' if the endpoint is reachable.
            version: Current version of the PromptLab API.

    Raises:
        HTTPException: Not raised by this endpoint.

    Example:
        GET /health
        Response: {"status": "healthy", "version": "1.0.0"}
    """
    return HealthResponse(status="healthy", version=__version__)


# ============== Prompt Endpoints ==============

@app.get("/prompts", response_model=PromptList)
def list_prompts(
    collection_id: Optional[str] = None,
    search: Optional[str] = None
):
    """List all prompts with optional filtering and search.

    Retrieves all prompts from the database with optional filtering by collection
    and full-text search across title and description fields. Results are sorted
    by creation date in descending order (newest first).

    Args:
        collection_id: Optional filter to return only prompts in a specific collection.
            If provided, only prompts with matching collection_id are returned.
        search: Optional search query string. Searches case-insensitively in prompt
            titles and descriptions.

    Returns:
        PromptList: Object containing list of matching prompts and total count.
            prompts: List of Prompt objects sorted by creation date (newest first).
            total: Total number of prompts matching the filters.

    Raises:
        HTTPException: No exceptions raised by this endpoint.

    Example:
        GET /prompts?search=api&collection_id=col-123
        Response: {"prompts": [...], "total": 5}
    """
    prompts = storage.get_all_prompts()
    
    # Filter by collection if specified
    if collection_id:
        prompts = filter_prompts_by_collection(prompts, collection_id)
    
    # Search if query provided
    if search:
        prompts = search_prompts(prompts, search)
    
    # Sort by date (newest first)
    # Note: There might be an issue with the sorting...
    prompts = sort_prompts_by_date(prompts, descending=True)
    
    return PromptList(prompts=prompts, total=len(prompts))


@app.get("/prompts/{prompt_id}", response_model=Prompt)
def get_prompt(prompt_id: str):
    """Retrieve a single prompt by ID.

    Fetches a specific prompt from the database using its unique identifier.

    Args:
        prompt_id: The UUID of the prompt to retrieve. Passed as a path parameter.

    Returns:
        Prompt: The complete Prompt object including all fields (id, title, content,
            description, collection_id, created_at, updated_at).

    Raises:
        HTTPException: 404 Not Found if no prompt with the given ID exists.

    Example:
        GET /prompts/abc123def456
        Response: {"id": "abc123def456", "title": "My Prompt", ...}
    """
    # BUG #1: This will raise a 500 error if prompt doesn't exist
    # because we're accessing .id on None
    # Should return 404 instead!
    prompt = storage.get_prompt(prompt_id)
    
    # This line causes the bug - accessing attribute on None
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return prompt


@app.post("/prompts", response_model=Prompt, status_code=201)
def create_prompt(prompt_data: PromptCreate):
    """Create a new prompt.

    Creates and stores a new prompt in the database. If a collection_id is
    specified, validates that the collection exists before creating the prompt.

    Args:
        prompt_data: Request body containing prompt details.
            - title: Required. Must be 1-200 characters.
            - content: Required. Must be at least 1 character.
            - description: Optional. Max 500 characters.
            - collection_id: Optional. Must reference an existing collection.

    Returns:
        Prompt: The newly created Prompt object with auto-generated id, created_at,
            and updated_at fields.

    Raises:
        HTTPException: 400 Bad Request if collection_id is provided but the
            collection does not exist.
        HTTPException: 422 Unprocessable Entity if request validation fails
            (e.g., title exceeds max length).

    Example:
        POST /prompts
        Body: {"title": "My Prompt", "content": "Prompt content here"}
        Response: {"id": "...", "title": "My Prompt", "created_at": "...", ...}
    """
    # Validate collection exists if provided
    if prompt_data.collection_id:
        collection = storage.get_collection(prompt_data.collection_id)
        if not collection:
            raise HTTPException(status_code=400, detail="Collection not found")
    
    prompt = Prompt(**prompt_data.model_dump())
    return storage.create_prompt(prompt)


@app.put("/prompts/{prompt_id}", response_model=Prompt)
def update_prompt(prompt_id: str, prompt_data: PromptUpdate):
    """Replace an entire prompt (full update).

    Updates a prompt by replacing all fields with provided values. The request
    body must contain complete prompt data. Use PATCH for partial updates.

    Args:
        prompt_id: The UUID of the prompt to update. Passed as a path parameter.
        prompt_data: Request body containing prompt details to replace.
            - title: Optional. Must be 1-200 characters if provided.
            - content: Optional. Must be at least 1 character if provided.
            - description: Optional. Max 500 characters.
            - collection_id: Optional. Must reference an existing collection if provided.

    Returns:
        Prompt: The updated Prompt object with new values and updated_at timestamp.

    Raises:
        HTTPException: 404 Not Found if no prompt with the given ID exists.
        HTTPException: 400 Bad Request if collection_id references a non-existent collection.
        HTTPException: 422 Unprocessable Entity if validation fails.

    Example:
        PUT /prompts/abc123
        Body: {"title": "Updated Title", "content": "New content"}
    """
    existing = storage.get_prompt(prompt_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    # Validate collection if provided
    if prompt_data.collection_id:
        collection = storage.get_collection(prompt_data.collection_id)
        if not collection:
            raise HTTPException(status_code=400, detail="Collection not found")
    
    # BUG #2: We're not updating the updated_at timestamp!
    # The updated prompt keeps the old timestamp
    updated_prompt = Prompt(
        id=existing.id,
        title=prompt_data.title,
        content=prompt_data.content,
        description=prompt_data.description,
        collection_id=prompt_data.collection_id,
        created_at=existing.created_at,
        updated_at=get_current_time()
    )
    
    return storage.update_prompt(prompt_id, updated_prompt)


# NOTE: PATCH endpoint is missing! Students need to implement this.
@app.patch("/prompts/{prompt_id}", response_model=Prompt)
def patch_prompt(prompt_id: str, prompt_data: PromptUpdate):
    """Partially update a prompt.

    Updates a prompt with only the provided fields while preserving existing values
    for fields not included in the request. Use PUT for full updates.

    Args:
        prompt_id: The UUID of the prompt to update. Passed as a path parameter.
        prompt_data: Request body containing fields to update (all optional).
            - title: Optional. Updates title if provided.
            - content: Optional. Updates content if provided.
            - description: Optional. Updates description if provided.
            - collection_id: Optional. Reassigns to collection if provided.

    Returns:
        Prompt: The updated Prompt object with merged values and new updated_at timestamp.

    Raises:
        HTTPException: 404 Not Found if no prompt with the given ID exists.
        HTTPException: 400 Bad Request if collection_id references a non-existent collection.
        HTTPException: 422 Unprocessable Entity if validation fails.

    Example:
        PATCH /prompts/abc123
        Body: {"title": "New Title"}
        (content and other fields remain unchanged)
    """
    existing = storage.get_prompt(prompt_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    # Validate collection if provided
    if prompt_data.collection_id:
        collection = storage.get_collection(prompt_data.collection_id)
        if not collection:
            raise HTTPException(status_code=400, detail="Collection not found")
    
    # Create a new Prompt object with updated fields (only if provided)
    updated_prompt = Prompt(
        id=existing.id,
        title=prompt_data.title if prompt_data.title is not None else existing.title,
        content=prompt_data.content if prompt_data.content is not None else existing.content,
        description=prompt_data.description if prompt_data.description is not None else existing.description,
        collection_id=prompt_data.collection_id if prompt_data.collection_id is not None else existing.collection_id,
        created_at=existing.created_at,
        updated_at=get_current_time()
    )
    
    return storage.update_prompt(prompt_id, updated_prompt)


@app.post("/prompts/{prompt_id}/versions", response_model=PromptVersion, status_code=201)
def create_prompt_version(prompt_id: str):
    """Create a new immutable version snapshot for a prompt.

    Args:
        prompt_id: The UUID of the prompt to version.

    Returns:
        PromptVersion: Newly created prompt version snapshot.

    Raises:
        HTTPException: 404 Not Found if prompt does not exist.
    """
    version = storage.create_prompt_version(prompt_id)
    if not version:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return version


@app.get("/prompts/{prompt_id}/versions", response_model=PromptVersionList)
def list_prompt_versions(prompt_id: str):
    """List all versions of a prompt.

    Args:
        prompt_id: The UUID of the prompt whose versions are requested.

    Returns:
        PromptVersionList: List of prompt versions and total count.

    Raises:
        HTTPException: 404 Not Found if prompt does not exist.
    """
    prompt = storage.get_prompt(prompt_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")

    versions = storage.get_prompt_versions(prompt_id)
    return PromptVersionList(versions=versions, total=len(versions))


@app.get("/prompts/{prompt_id}/versions/{version_id}", response_model=PromptVersion)
def get_prompt_version(prompt_id: str, version_id: str):
    """Retrieve one version snapshot for a prompt.

    Args:
        prompt_id: The UUID of the prompt.
        version_id: The UUID of the prompt version snapshot.

    Returns:
        PromptVersion: The requested version snapshot.

    Raises:
        HTTPException: 404 Not Found if prompt or version does not exist.
    """
    prompt = storage.get_prompt(prompt_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")

    version = storage.get_prompt_version(prompt_id, version_id)
    if not version:
        raise HTTPException(status_code=404, detail="Prompt version not found")

    return version


@app.post("/prompts/{prompt_id}/versions/{version_id}/restore", response_model=Prompt)
def restore_prompt_version(prompt_id: str, version_id: str):
    """Restore a prompt to fields captured in a specific version snapshot.

    Args:
        prompt_id: The UUID of the prompt to restore.
        version_id: The UUID of the version snapshot to restore from.

    Returns:
        Prompt: The updated prompt after restore.

    Raises:
        HTTPException: 404 Not Found if prompt or version does not exist.
    """
    existing = storage.get_prompt(prompt_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Prompt not found")

    version = storage.get_prompt_version(prompt_id, version_id)
    if not version:
        raise HTTPException(status_code=404, detail="Prompt version not found")

    restored_prompt = Prompt(
        id=existing.id,
        title=version.title,
        content=version.content,
        description=version.description,
        collection_id=version.collection_id,
        created_at=existing.created_at,
        updated_at=get_current_time(),
    )

    return storage.update_prompt(prompt_id, restored_prompt)


@app.delete("/prompts/{prompt_id}", status_code=204)
def delete_prompt(prompt_id: str):
    """Delete a prompt by ID.

    Removes a prompt from the database. Returns no content on success.

    Args:
        prompt_id: The UUID of the prompt to delete. Passed as a path parameter.

    Returns:
        None: On successful deletion returns empty response with 204 status code.

    Raises:
        HTTPException: 404 Not Found if no prompt with the given ID exists.

    Example:
        DELETE /prompts/abc123
        Response: 204 No Content
    """
    if not storage.delete_prompt(prompt_id):
        raise HTTPException(status_code=404, detail="Prompt not found")
    return None


# ============== Collection Endpoints ==============

@app.get("/collections", response_model=CollectionList)
def list_collections():
    """List all collections.

    Retrieves all collections from the database.

    Returns:
        CollectionList: Object containing list of all collections and total count.
            collections: List of all Collection objects.
            total: Total number of collections in the database.

    Raises:
        HTTPException: No exceptions raised by this endpoint.

    Example:
        GET /collections
        Response: {"collections": [...], "total": 3}
    """
    collections = storage.get_all_collections()
    return CollectionList(collections=collections, total=len(collections))


@app.get("/collections/{collection_id}", response_model=Collection)
def get_collection(collection_id: str):
    """Retrieve a single collection by ID.

    Fetches a specific collection from the database using its unique identifier.

    Args:
        collection_id: The UUID of the collection to retrieve. Passed as a path parameter.

    Returns:
        Collection: The complete Collection object including id, name, description,
            and created_at timestamp.

    Raises:
        HTTPException: 404 Not Found if no collection with the given ID exists.

    Example:
        GET /collections/col-abc123
        Response: {"id": "col-abc123", "name": "My Collection", ...}
    """
    collection = storage.get_collection(collection_id)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    return collection


@app.post("/collections", response_model=Collection, status_code=201)
def create_collection(collection_data: CollectionCreate):
    """Create a new collection.

    Creates and stores a new collection in the database.

    Args:
        collection_data: Request body containing collection details.
            - name: Required. Must be 1-100 characters.
            - description: Optional. Max 500 characters.

    Returns:
        Collection: The newly created Collection object with auto-generated id
            and created_at timestamp.

    Raises:
        HTTPException: 422 Unprocessable Entity if request validation fails
            (e.g., name exceeds max length or is empty).

    Example:
        POST /collections
        Body: {"name": "My Collection", "description": "Collection description"}
        Response: {"id": "...", "name": "My Collection", "created_at": "...", ...}
    """
    collection = Collection(**collection_data.model_dump())
    return storage.create_collection(collection)


@app.delete("/collections/{collection_id}", status_code=204)
def delete_collection(collection_id: str):
    """Delete a collection and all associated prompts.

    Removes a collection from the database. All prompts belonging to this collection
    are also deleted. Returns no content on success.

    Args:
        collection_id: The UUID of the collection to delete. Passed as a path parameter.

    Returns:
        None: On successful deletion returns empty response with 204 status code.

    Raises:
        HTTPException: 404 Not Found if no collection with the given ID exists.

    Note:
        This operation is cascading - all prompts in the collection will be permanently
        deleted. This cannot be undone.

    Example:
        DELETE /collections/col-abc123
        Response: 204 No Content
    """
    # Check if collection exists first
    if not storage.get_collection(collection_id):
        raise HTTPException(status_code=404, detail="Collection not found")
    
    # Delete all prompts that belong to this collection
    all_prompts = storage.get_all_prompts()
    for prompt in all_prompts:
        if prompt.collection_id == collection_id:
            storage.delete_prompt(prompt.id)
    
    # Now delete the collection
    storage.delete_collection(collection_id)
    
    return None
