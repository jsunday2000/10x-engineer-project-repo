"""SQLite storage for PromptLab

This module provides SQLite-based persistent storage for prompts and collections.
Data is stored in a local promptlab.db file.
"""

from typing import List, Optional
from datetime import datetime
import os
from sqlalchemy import create_engine, Column, String, DateTime, Integer
from sqlalchemy.orm import declarative_base, sessionmaker
from app.models import Prompt, Collection, PromptVersion

# Database setup - use absolute path to ensure consistency
DB_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(DB_DIR, 'promptlab.db')
DATABASE_URL = f"sqlite:///{DB_PATH}"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# SQLAlchemy models
class PromptModel(Base):
    """SQLAlchemy ORM model for Prompt persistence.

    Maps the prompts table in SQLite to Python objects. Used internally by
    the Storage class to interact with the database. Corresponds to the
    Pydantic Prompt model.
    """
    __tablename__ = "prompts"
    
    id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    description = Column(String, nullable=True)
    collection_id = Column(String, nullable=True, index=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class CollectionModel(Base):
    """SQLAlchemy ORM model for Collection persistence.

    Maps the collections table in SQLite to Python objects. Used internally by
    the Storage class to interact with the database. Corresponds to the
    Pydantic Collection model.
    """
    __tablename__ = "collections"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    created_at = Column(DateTime)


class PromptVersionModel(Base):
    """SQLAlchemy ORM model for prompt version snapshots."""

    __tablename__ = "prompt_versions"

    id = Column(String, primary_key=True, index=True)
    prompt_id = Column(String, index=True)
    version_number = Column(Integer, index=True)
    title = Column(String)
    content = Column(String)
    description = Column(String, nullable=True)
    collection_id = Column(String, nullable=True, index=True)
    created_at = Column(DateTime)


class Storage:
    """SQLite-based persistent storage for PromptLab.

    Provides a data access layer for managing prompts and collections.
    Handles all database operations including CRUD (Create, Read, Update, Delete)
    for both prompts and collections. Uses SQLAlchemy ORM for database interactions
    and stores data in a local SQLite database file.

    The storage automatically creates database tables on first initialization.
    Each method manages its own database session, ensuring thread safety and
    proper resource cleanup.

    Attributes:
        None (all data is stored in the SQLite database)
    """
    
    def __init__(self):
        """Initialize the Storage and create database tables.

        Creates all database tables defined in SQLAlchemy models if they don't
        already exist. Called automatically when the module is loaded.
        """
        # Create tables on first initialization
        Base.metadata.create_all(bind=engine)
    
    def _get_session(self):
        """Get a new database session for query execution.

        Creates and returns a new SQLAlchemy session for database operations.
        Each operation should call this method to get a fresh session.

        Returns:
            A new SQLAlchemy session ready for database queries.

        Note:
            Sessions must be closed after use. This is typically handled
            in the finally block of calling methods.
        """
        return SessionLocal()
    
    # ============== Prompt Operations ==============
    
    def create_prompt(self, prompt: Prompt) -> Prompt:
        """Create a new prompt in the database.

        Inserts a prompt into the database and commits the transaction.

        Args:
            prompt: A Prompt object to create. Should have id, title, content,
                created_at, and updated_at fields populated.

        Returns:
            The same Prompt object that was passed in (with all fields).

        Raises:
            SQLAlchemy exceptions: If database operation fails (e.g., database locked,
                constraint violations).

        Example:
            >>> prompt = Prompt(id="abc123", title="My Prompt", content="Content")
            >>> created = storage.create_prompt(prompt)
            >>> created.id
            'abc123'
        """
        session = self._get_session()
        try:
            db_prompt = PromptModel(
                id=prompt.id,
                title=prompt.title,
                content=prompt.content,
                description=prompt.description,
                collection_id=prompt.collection_id,
                created_at=prompt.created_at,
                updated_at=prompt.updated_at
            )
            session.add(db_prompt)
            session.commit()
            return prompt
        finally:
            session.close()
    
    def get_prompt(self, prompt_id: str) -> Optional[Prompt]:
        """Retrieve a prompt from the database by its ID.

        Queries the database for a prompt with the specified ID.

        Args:
            prompt_id: The unique UUID of the prompt to retrieve.

        Returns:
            A Prompt object if found, None if no prompt with the given ID exists.

        Raises:
            SQLAlchemy exceptions: If database operation fails.

        Example:
            >>> prompt = storage.get_prompt("abc123")
            >>> if prompt:
            ...     print(prompt.title)
        """
        session = self._get_session()
        try:
            db_prompt = session.query(PromptModel).filter(PromptModel.id == prompt_id).first()
            if not db_prompt:
                return None
            return Prompt(
                id=db_prompt.id,
                title=db_prompt.title,
                content=db_prompt.content,
                description=db_prompt.description,
                collection_id=db_prompt.collection_id,
                created_at=db_prompt.created_at,
                updated_at=db_prompt.updated_at
            )
        finally:
            session.close()
    
    def get_all_prompts(self) -> List[Prompt]:
        """Retrieve all prompts from the database.

        Fetches every prompt record from the database.

        Returns:
            A list of all Prompt objects in the database. Returns empty list
            if no prompts exist.

        Raises:
            SQLAlchemy exceptions: If database operation fails.

        Example:
            >>> all_prompts = storage.get_all_prompts()
            >>> print(f"Total prompts: {len(all_prompts)}")
        """
        session = self._get_session()
        try:
            db_prompts = session.query(PromptModel).all()
            return [
                Prompt(
                    id=p.id,
                    title=p.title,
                    content=p.content,
                    description=p.description,
                    collection_id=p.collection_id,
                    created_at=p.created_at,
                    updated_at=p.updated_at
                )
                for p in db_prompts
            ]
        finally:
            session.close()
    
    def update_prompt(self, prompt_id: str, prompt: Prompt) -> Optional[Prompt]:
        """Update an existing prompt in the database.

        Modifies all fields of a prompt record. The prompt must already exist.

        Args:
            prompt_id: The UUID of the prompt to update.
            prompt: The new Prompt object with updated field values.

        Returns:
            The updated Prompt object if successful, None if the prompt with
            the given ID does not exist.

        Raises:
            SQLAlchemy exceptions: If database operation fails.

        Example:
            >>> updated_prompt = Prompt(id="abc", title="New Title", ...)
            >>> result = storage.update_prompt("abc", updated_prompt)
            >>> if result:
            ...     print("Update successful")
        """
        session = self._get_session()
        try:
            db_prompt = session.query(PromptModel).filter(PromptModel.id == prompt_id).first()
            if not db_prompt:
                return None
            
            db_prompt.title = prompt.title
            db_prompt.content = prompt.content
            db_prompt.description = prompt.description
            db_prompt.collection_id = prompt.collection_id
            db_prompt.updated_at = prompt.updated_at
            
            session.commit()
            return prompt
        finally:
            session.close()
    
    def delete_prompt(self, prompt_id: str) -> bool:
        """Delete a prompt from the database.

        Removes a prompt record permanently. The operation is committed immediately.

        Args:
            prompt_id: The UUID of the prompt to delete.

        Returns:
            True if a prompt was successfully deleted, False if no prompt with
            the given ID exists.

        Raises:
            SQLAlchemy exceptions: If database operation fails.

        Example:
            >>> success = storage.delete_prompt("abc123")
            >>> if success:
            ...     print("Prompt deleted")
        """
        session = self._get_session()
        try:
            db_prompt = session.query(PromptModel).filter(PromptModel.id == prompt_id).first()
            if not db_prompt:
                return False

            session.query(PromptVersionModel).filter(
                PromptVersionModel.prompt_id == prompt_id
            ).delete()

            session.delete(db_prompt)
            session.commit()
            return True
        finally:
            session.close()

    def create_prompt_version(self, prompt_id: str) -> Optional[PromptVersion]:
        """Create a new version snapshot for a prompt.

        Args:
            prompt_id: UUID of the prompt to snapshot.

        Returns:
            The created PromptVersion if prompt exists, else None.
        """
        session = self._get_session()
        try:
            db_prompt = session.query(PromptModel).filter(PromptModel.id == prompt_id).first()
            if not db_prompt:
                return None

            existing_versions = session.query(PromptVersionModel).filter(
                PromptVersionModel.prompt_id == prompt_id
            ).all()
            next_version_number = len(existing_versions) + 1

            version = PromptVersion(
                prompt_id=prompt_id,
                version_number=next_version_number,
                title=db_prompt.title,
                content=db_prompt.content,
                description=db_prompt.description,
                collection_id=db_prompt.collection_id,
            )

            db_version = PromptVersionModel(
                id=version.id,
                prompt_id=version.prompt_id,
                version_number=version.version_number,
                title=version.title,
                content=version.content,
                description=version.description,
                collection_id=version.collection_id,
                created_at=version.created_at,
            )
            session.add(db_version)
            session.commit()
            return version
        finally:
            session.close()

    def get_prompt_versions(self, prompt_id: str) -> List[PromptVersion]:
        """Get all versions for a prompt in ascending version order."""
        session = self._get_session()
        try:
            db_versions = session.query(PromptVersionModel).filter(
                PromptVersionModel.prompt_id == prompt_id
            ).all()

            versions = [
                PromptVersion(
                    id=v.id,
                    prompt_id=v.prompt_id,
                    version_number=int(v.version_number),
                    title=v.title,
                    content=v.content,
                    description=v.description,
                    collection_id=v.collection_id,
                    created_at=v.created_at,
                )
                for v in db_versions
            ]
            return sorted(versions, key=lambda version: version.version_number)
        finally:
            session.close()

    def get_prompt_version(self, prompt_id: str, version_id: str) -> Optional[PromptVersion]:
        """Get a specific prompt version by version ID and prompt ID."""
        session = self._get_session()
        try:
            db_version = session.query(PromptVersionModel).filter(
                PromptVersionModel.prompt_id == prompt_id,
                PromptVersionModel.id == version_id,
            ).first()
            if not db_version:
                return None

            return PromptVersion(
                id=db_version.id,
                prompt_id=db_version.prompt_id,
                version_number=int(db_version.version_number),
                title=db_version.title,
                content=db_version.content,
                description=db_version.description,
                collection_id=db_version.collection_id,
                created_at=db_version.created_at,
            )
        finally:
            session.close()
    
    # ============== Collection Operations ==============
    
    def create_collection(self, collection: Collection) -> Collection:
        """Create a new collection in the database.

        Inserts a collection into the database and commits the transaction.

        Args:
            collection: A Collection object to create. Should have id, name,
                description, and created_at fields populated.

        Returns:
            The same Collection object that was passed in.

        Raises:
            SQLAlchemy exceptions: If database operation fails.

        Example:
            >>> collection = Collection(id="col1", name="My Collection")
            >>> created = storage.create_collection(collection)
            >>> created.id
            'col1'
        """
        session = self._get_session()
        try:
            db_collection = CollectionModel(
                id=collection.id,
                name=collection.name,
                description=collection.description,
                created_at=collection.created_at
            )
            session.add(db_collection)
            session.commit()
            return collection
        finally:
            session.close()
    
    def get_collection(self, collection_id: str) -> Optional[Collection]:
        """Retrieve a collection from the database by its ID.

        Queries the database for a collection with the specified ID.

        Args:
            collection_id: The unique UUID of the collection to retrieve.

        Returns:
            A Collection object if found, None if no collection with the given
            ID exists.

        Raises:
            SQLAlchemy exceptions: If database operation fails.

        Example:
            >>> collection = storage.get_collection("col1")
            >>> if collection:
            ...     print(collection.name)
        """
        session = self._get_session()
        try:
            db_collection = session.query(CollectionModel).filter(CollectionModel.id == collection_id).first()
            if not db_collection:
                return None
            return Collection(
                id=db_collection.id,
                name=db_collection.name,
                description=db_collection.description,
                created_at=db_collection.created_at
            )
        finally:
            session.close()
    
    def get_all_collections(self) -> List[Collection]:
        """Retrieve all collections from the database.

        Fetches every collection record from the database.

        Returns:
            A list of all Collection objects in the database. Returns empty list
            if no collections exist.

        Raises:
            SQLAlchemy exceptions: If database operation fails.

        Example:
            >>> all_collections = storage.get_all_collections()
            >>> print(f"Total collections: {len(all_collections)}")
        """
        session = self._get_session()
        try:
            db_collections = session.query(CollectionModel).all()
            return [
                Collection(
                    id=c.id,
                    name=c.name,
                    description=c.description,
                    created_at=c.created_at
                )
                for c in db_collections
            ]
        finally:
            session.close()
    
    def delete_collection(self, collection_id: str) -> bool:
        """Delete a collection from the database.

        Removes a collection record permanently. The operation is committed immediately.
        Note: This does NOT automatically delete prompts in the collection.

        Args:
            collection_id: The UUID of the collection to delete.

        Returns:
            True if a collection was successfully deleted, False if no collection
            with the given ID exists.

        Raises:
            SQLAlchemy exceptions: If database operation fails.

        Example:
            >>> success = storage.delete_collection("col1")
            >>> if success:
            ...     print("Collection deleted")
        """
        session = self._get_session()
        try:
            db_collection = session.query(CollectionModel).filter(CollectionModel.id == collection_id).first()
            if not db_collection:
                return False
            session.delete(db_collection)
            session.commit()
            return True
        finally:
            session.close()
    
    def get_prompts_by_collection(self, collection_id: str) -> List[Prompt]:
        """Retrieve all prompts belonging to a specific collection.

        Queries the database for all prompts with the specified collection_id.

        Args:
            collection_id: The UUID of the collection to filter by.

        Returns:
            A list of Prompt objects belonging to the collection. Returns empty
            list if the collection has no prompts or doesn't exist.

        Raises:
            SQLAlchemy exceptions: If database operation fails.

        Example:
            >>> prompts = storage.get_prompts_by_collection("col1")
            >>> all(p.collection_id == "col1" for p in prompts)
            True
        """
        session = self._get_session()
        try:
            db_prompts = session.query(PromptModel).filter(PromptModel.collection_id == collection_id).all()
            return [
                Prompt(
                    id=p.id,
                    title=p.title,
                    content=p.content,
                    description=p.description,
                    collection_id=p.collection_id,
                    created_at=p.created_at,
                    updated_at=p.updated_at
                )
                for p in db_prompts
            ]
        finally:
            session.close()
    
    # ============== Utility ==============
    
    def clear(self):
        """Clear all data from the database.

        Deletes all prompt and collection records from the database. This
        operation is permanent and cannot be undone. Primarily used for testing.

        Raises:
            SQLAlchemy exceptions: If database operation fails.

        Note:
            This is a destructive operation. Use with caution and only in
            testing environments.

        Example:
            >>> storage.clear()  # Database is now empty
        """
        session = self._get_session()
        try:
            session.query(PromptVersionModel).delete()
            session.query(PromptModel).delete()
            session.query(CollectionModel).delete()
            session.commit()
        finally:
            session.close()


# Global storage instance
storage = Storage()
