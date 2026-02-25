"""Pydantic models for PromptLab"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from uuid import uuid4


def generate_id() -> str:
    """Generate a unique identifier using UUID4.

    Returns:
        A string representation of a UUID4.

    Example:
        >>> id = generate_id()
        >>> len(id)  # UUID4 string length
        36
    """
    return str(uuid4())


def get_current_time() -> datetime:
    """Get the current UTC time.

    Returns:
        The current datetime in UTC.

    Example:
        >>> now = get_current_time()
        >>> isinstance(now, datetime)
        True
    """
    return datetime.utcnow()


# ============== Prompt Models ==============

class PromptBase(BaseModel):
    """Base Pydantic model for Prompt data.

    Defines common fields and validation rules shared by all prompt operations.
    This model serves as the parent for PromptCreate and PromptUpdate.
    """
    title: str = Field(..., min_length=1, max_length=200, description="The prompt's title. Must be between 1 and 200 characters.")
    content: str = Field(..., min_length=1, description="The prompt's main content. Must be at least 1 character long.")
    description: Optional[str] = Field(None, max_length=500, description="Optional detailed description of the prompt. Max 500 characters.")
    collection_id: Optional[str] = Field(None, description="Optional UUID of the collection this prompt belongs to.")


class PromptCreate(PromptBase):
    """Request model for creating a new prompt.

    Used in POST /prompts endpoint. All fields from PromptBase are required
    except description and collection_id which are optional.
    """
    pass

class PromptUpdate(BaseModel):
    """Request model for updating an existing prompt.

    Used in PUT and PATCH endpoints. All fields are optional to allow
    partial updates. Only provided fields will be updated.
    """
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="Updated prompt title. Must be between 1 and 200 characters if provided.")
    content: Optional[str] = Field(None, min_length=1, description="Updated prompt content. Must be at least 1 character if provided.")
    description: Optional[str] = Field(None, max_length=500, description="Updated prompt description. Max 500 characters if provided.")
    collection_id: Optional[str] = Field(None, description="UUID of the collection to reassign this prompt to. Optional.")


class Prompt(PromptBase):
    """Complete Prompt model including database fields.

    Represents a full prompt record from the database with auto-generated
    timestamp and ID fields. Used in responses from GET endpoints and
    returned after POST/PUT/PATCH operations.
    """
    id: str = Field(default_factory=generate_id, description="Unique UUID for the prompt. Auto-generated if not provided.")
    created_at: datetime = Field(default_factory=get_current_time, description="Timestamp when the prompt was created. Auto-generated in UTC.")
    updated_at: datetime = Field(default_factory=get_current_time, description="Timestamp of the last update to the prompt. Auto-generated in UTC.")

    class Config:
        from_attributes = True


class PromptVersion(BaseModel):
    """Snapshot model representing a saved version of a prompt.

    Stores immutable prompt content at a point in time so it can be reviewed
    or restored later.
    """

    id: str = Field(default_factory=generate_id, description="Unique UUID for the prompt version. Auto-generated if not provided.")
    prompt_id: str = Field(..., description="UUID of the prompt this version belongs to.")
    version_number: int = Field(..., ge=1, description="Sequential version number per prompt, starting at 1.")
    title: str = Field(..., min_length=1, max_length=200, description="Snapshot of prompt title at version creation time.")
    content: str = Field(..., min_length=1, description="Snapshot of prompt content at version creation time.")
    description: Optional[str] = Field(None, max_length=500, description="Snapshot of prompt description at version creation time.")
    collection_id: Optional[str] = Field(None, description="Snapshot of prompt collection_id at version creation time.")
    created_at: datetime = Field(default_factory=get_current_time, description="Timestamp when this version snapshot was created in UTC.")

    class Config:
        from_attributes = True


# ============== Collection Models ==============

class CollectionBase(BaseModel):
    """Base Pydantic model for Collection data.

    Defines common fields and validation rules for collection operations.
    Serves as parent for CollectionCreate model.
    """
    name: str = Field(..., min_length=1, max_length=100, description="The collection's name. Must be between 1 and 100 characters.")
    description: Optional[str] = Field(None, max_length=500, description="Optional description of the collection. Max 500 characters.")


class CollectionCreate(CollectionBase):
    """Request model for creating a new collection.

    Used in POST /collections endpoint. Name is required, description is optional.
    """
    pass


class Collection(CollectionBase):
    """Complete Collection model including database fields.

    Represents a full collection record from the database with auto-generated
    timestamp and ID fields. Used in responses from GET endpoints and after
    POST operations.
    """
    id: str = Field(default_factory=generate_id, description="Unique UUID for the collection. Auto-generated if not provided.")
    created_at: datetime = Field(default_factory=get_current_time, description="Timestamp when the collection was created. Auto-generated in UTC.")

    class Config:
        from_attributes = True


# ============== Response Models ==============

class PromptList(BaseModel):
    """Response model for list of prompts.

    Used in GET /prompts endpoint to return a paginated or filtered list
    of prompts along with the total count.
    """
    prompts: List[Prompt] = Field(description="List of Prompt objects returned by the query.")
    total: int = Field(description="Total number of prompts in the result set.")


class PromptVersionList(BaseModel):
    """Response model for list of prompt versions."""

    versions: List[PromptVersion] = Field(description="List of PromptVersion objects for a prompt.")
    total: int = Field(description="Total number of versions in the result set.")


class CollectionList(BaseModel):
    """Response model for list of collections.

    Used in GET /collections endpoint to return all collections
    along with the total count.
    """
    collections: List[Collection] = Field(description="List of Collection objects.")
    total: int = Field(description="Total number of collections in the result set.")


class HealthResponse(BaseModel):
    """Response model for health check endpoint.

    Used in GET /health endpoint to indicate API availability
    and current version.
    """
    status: str = Field(description="Health status of the API. Expected value: 'healthy'.")
    version: str = Field(description="Current version of the PromptLab API.")
