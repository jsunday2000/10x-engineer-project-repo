"""SQLite storage for PromptLab

This module provides SQLite-based persistent storage for prompts and collections.
Data is stored in a local promptlab.db file.
"""

from typing import List, Optional
from datetime import datetime
import os
from sqlalchemy import create_engine, Column, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from app.models import Prompt, Collection

# Database setup - use absolute path to ensure consistency
DB_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(DB_DIR, 'promptlab.db')
DATABASE_URL = f"sqlite:///{DB_PATH}"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# SQLAlchemy models
class PromptModel(Base):
    """SQLAlchemy model for Prompt."""
    __tablename__ = "prompts"
    
    id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    description = Column(String, nullable=True)
    collection_id = Column(String, nullable=True, index=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class CollectionModel(Base):
    """SQLAlchemy model for Collection."""
    __tablename__ = "collections"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    created_at = Column(DateTime)


class Storage:
    """SQLite-based storage for PromptLab."""
    
    def __init__(self):
        # Create tables on first initialization
        Base.metadata.create_all(bind=engine)
    
    def _get_session(self):
        """Get a new database session."""
        return SessionLocal()
    
    # ============== Prompt Operations ==============
    
    def create_prompt(self, prompt: Prompt) -> Prompt:
        """Create a new prompt in the database."""
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
        """Retrieve a prompt by ID."""
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
        """Retrieve all prompts."""
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
        """Update an existing prompt."""
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
        """Delete a prompt."""
        session = self._get_session()
        try:
            db_prompt = session.query(PromptModel).filter(PromptModel.id == prompt_id).first()
            if not db_prompt:
                return False
            session.delete(db_prompt)
            session.commit()
            return True
        finally:
            session.close()
    
    # ============== Collection Operations ==============
    
    def create_collection(self, collection: Collection) -> Collection:
        """Create a new collection."""
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
        """Retrieve a collection by ID."""
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
        """Retrieve all collections."""
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
        """Delete a collection."""
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
        """Retrieve all prompts belonging to a collection."""
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
        """Clear all data from the database (for testing)."""
        session = self._get_session()
        try:
            session.query(PromptModel).delete()
            session.query(CollectionModel).delete()
            session.commit()
        finally:
            session.close()


# Global storage instance
storage = Storage()
