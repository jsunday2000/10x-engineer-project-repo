"""API tests for PromptLab

These tests verify the API endpoints work correctly.
Students should expand these tests significantly in Week 3.
"""

import pytest
from fastapi.testclient import TestClient


class TestHealth:
    """Tests for health endpoint."""
    
    def test_health_check(self, client: TestClient):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data


class TestPrompts:
    """Tests for prompt endpoints."""
    
    def test_create_prompt(self, client: TestClient, sample_prompt_data):
        response = client.post("/prompts", json=sample_prompt_data)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == sample_prompt_data["title"]
        assert data["content"] == sample_prompt_data["content"]
        assert "id" in data
        assert "created_at" in data
    
    def test_list_prompts_empty(self, client: TestClient):
        response = client.get("/prompts")
        assert response.status_code == 200
        data = response.json()
        assert data["prompts"] == []
        assert data["total"] == 0
    
    def test_list_prompts_with_data(self, client: TestClient, sample_prompt_data):
        # Create a prompt first
        client.post("/prompts", json=sample_prompt_data)
        
        response = client.get("/prompts")
        assert response.status_code == 200
        data = response.json()
        assert len(data["prompts"]) == 1
        assert data["total"] == 1
    
    def test_get_prompt_success(self, client: TestClient, sample_prompt_data):
        # Create a prompt first
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]
        
        response = client.get(f"/prompts/{prompt_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == prompt_id
    
    def test_get_prompt_not_found(self, client: TestClient):
        """Test that getting a non-existent prompt returns 404.
        
        NOTE: This test currently FAILS due to Bug #1!
        The API returns 500 instead of 404.
        """
        response = client.get("/prompts/nonexistent-id")
        # This should be 404, but there's a bug...
        assert response.status_code == 404  # Will fail until bug is fixed
    
    def test_delete_prompt(self, client: TestClient, sample_prompt_data):
        # Create a prompt first
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]
        
        # Delete it
        response = client.delete(f"/prompts/{prompt_id}")
        assert response.status_code == 204
        
        # Verify it's gone
        get_response = client.get(f"/prompts/{prompt_id}")
        # Note: This might fail due to Bug #1
        assert get_response.status_code in [404, 500]  # 404 after fix
    
    def test_update_prompt(self, client: TestClient, sample_prompt_data):
        # Create a prompt first
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]
        original_updated_at = create_response.json()["updated_at"]
        
        # Update it
        updated_data = {
            "title": "Updated Title",
            "content": "Updated content for the prompt",
            "description": "Updated description"
        }
        
        import time
        time.sleep(0.1)  # Small delay to ensure timestamp would change
        
        response = client.put(f"/prompts/{prompt_id}", json=updated_data)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"
        
        # NOTE: This assertion will fail due to Bug #2!
        # The updated_at should be different from original
        # assert data["updated_at"] != original_updated_at  # Uncomment after fix
    
    def test_update_prompt_updates_timestamp(self, client: TestClient, sample_prompt_data):
        """Test that updated_at timestamp changes when prompt is updated.
        
        Verifies Bug #2 is fixed - updated_at should reflect the current time.
        """
        import time
        from datetime import datetime
        
        # Create a prompt
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]
        original_updated_at = create_response.json()["updated_at"]
        
        # Wait a bit to ensure time passes
        time.sleep(0.2)
        
        # Update the prompt
        updated_data = {
            "title": "Updated Title",
            "content": "Updated content",
            "description": "Updated description"
        }
        
        update_response = client.put(f"/prompts/{prompt_id}", json=updated_data)
        new_updated_at = update_response.json()["updated_at"]
        
        # Verify the timestamp was updated
        assert new_updated_at != original_updated_at, \
            "Bug #2: updated_at should change when prompt is updated"
    
    def test_update_prompt_timestamp_is_current(self, client: TestClient, sample_prompt_data):
        """Test that updated_at is approximately the current time after update.
        
        Verifies the timestamp is not stale or incorrect.
        """
        import time
        from datetime import datetime
        
        # Create a prompt
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]
        
        # Record time before update
        time_before_update = datetime.utcnow()
        
        # Update the prompt
        updated_data = {
            "title": "New Title",
            "content": "New content here",
            "description": "New desc"
        }
        
        update_response = client.put(f"/prompts/{prompt_id}", json=updated_data)
        updated_at_str = update_response.json()["updated_at"]
        
        # Parse the returned datetime
        # Handle both ISO format strings and datetime objects
        if isinstance(updated_at_str, str):
            updated_at = datetime.fromisoformat(updated_at_str.replace('Z', '+00:00'))
        else:
            updated_at = datetime.fromisoformat(str(updated_at_str))
        
        time_after_update = datetime.utcnow()
        
        # Verify updated_at is between before and after (within 1 second tolerance)
        assert time_before_update <= updated_at <= time_after_update, \
            "updated_at should be approximately current time, not stale"
    
    def test_update_prompt_preserves_created_at(self, client: TestClient, sample_prompt_data):
        """Test that created_at stays the same but updated_at changes.
        
        Verifies that only the updated_at timestamp is modified, not created_at.
        """
        import time
        
        # Create a prompt
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]
        original_created_at = create_response.json()["created_at"]
        original_updated_at = create_response.json()["updated_at"]
        
        # Wait briefly
        time.sleep(0.2)
        
        # Update the prompt
        updated_data = {
            "title": "Modified Title",
            "content": "Modified content text",
            "description": "Modified description"
        }
        
        update_response = client.put(f"/prompts/{prompt_id}", json=updated_data)
        new_created_at = update_response.json()["created_at"]
        new_updated_at = update_response.json()["updated_at"]
        
        # Verify created_at hasn't changed
        assert new_created_at == original_created_at, \
            "created_at should not change when updating a prompt"
        
        # Verify updated_at did change
        assert new_updated_at != original_updated_at, \
            "updated_at should change when updating a prompt"
    
    def test_sorting_order(self, client: TestClient):
        """Test that prompts are sorted newest first.
        
        NOTE: This test might fail due to Bug #3!
        """
        import time
        
        # Create prompts with delay
        prompt1 = {"title": "First", "content": "First prompt content"}
        prompt2 = {"title": "Second", "content": "Second prompt content"}
        
        client.post("/prompts", json=prompt1)
        time.sleep(0.1)
        client.post("/prompts", json=prompt2)
        
        response = client.get("/prompts")
        prompts = response.json()["prompts"]
        
        # Newest (Second) should be first
        assert prompts[0]["title"] == "Second"  # Will fail until Bug #3 fixed
    
    def test_patch_partial_update_single_field(self, client: TestClient, sample_prompt_data):
        """Test PATCH endpoint with only one field updated.
        
        Verifies that PATCH can update just the title while preserving
        content and description.
        """
        import time
        
        # Create a prompt
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]
        original_content = create_response.json()["content"]
        original_description = create_response.json()["description"]
        
        time.sleep(0.1)
        
        # Patch with only title
        patch_data = {"title": "Patched Title"}
        response = client.patch(f"/prompts/{prompt_id}", json=patch_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Patched Title"
        assert data["content"] == original_content, "Content should be preserved"
        assert data["description"] == original_description, "Description should be preserved"
    
    def test_patch_partial_update_multiple_fields(self, client: TestClient, sample_prompt_data):
        """Test PATCH endpoint with multiple fields but not all.
        
        Verifies that PATCH can update title and content while preserving
        description.
        """
        import time
        
        # Create a prompt
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]
        original_description = create_response.json()["description"]
        
        time.sleep(0.1)
        
        # Patch with title and content, but not description
        patch_data = {
            "title": "New Patched Title",
            "content": "New patched content here"
        }
        response = client.patch(f"/prompts/{prompt_id}", json=patch_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "New Patched Title"
        assert data["content"] == "New patched content here"
        assert data["description"] == original_description, "Description should be preserved when not provided"
    
    def test_patch_updates_timestamp(self, client: TestClient, sample_prompt_data):
        """Test that PATCH updates the updated_at timestamp.
        
        Verifies that even partial updates correctly set updated_at to
        current time while preserving created_at.
        """
        import time
        from datetime import datetime
        
        # Create a prompt
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]
        original_created_at = create_response.json()["created_at"]
        original_updated_at = create_response.json()["updated_at"]
        
        time.sleep(0.2)
        
        # Patch with just one field
        patch_data = {"title": "Patched Title"}
        patch_response = client.patch(f"/prompts/{prompt_id}", json=patch_data)
        
        assert patch_response.status_code == 200
        data = patch_response.json()
        
        # Verify created_at didn't change
        assert data["created_at"] == original_created_at, \
            "created_at should not change with PATCH"
        
        # Verify updated_at did change
        assert data["updated_at"] != original_updated_at, \
            "updated_at should change with PATCH"


class TestCollections:
    """Tests for collection endpoints."""
    
    def test_create_collection(self, client: TestClient, sample_collection_data):
        response = client.post("/collections", json=sample_collection_data)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == sample_collection_data["name"]
        assert "id" in data
    
    def test_list_collections(self, client: TestClient, sample_collection_data):
        client.post("/collections", json=sample_collection_data)
        
        response = client.get("/collections")
        assert response.status_code == 200
        data = response.json()
        assert len(data["collections"]) == 1
    
    def test_get_collection_not_found(self, client: TestClient):
        response = client.get("/collections/nonexistent-id")
        assert response.status_code == 404
    
    def test_delete_collection_with_prompts(self, client: TestClient, sample_collection_data, sample_prompt_data):
        """Test deleting a collection that has prompts.
        
        NOTE: Bug #4 - prompts become orphaned after collection deletion.
        This test documents the current (buggy) behavior.
        After fixing, update the test to verify correct behavior.
        """
        # Create collection
        col_response = client.post("/collections", json=sample_collection_data)
        collection_id = col_response.json()["id"]
        
        # Create prompt in collection
        prompt_data = {**sample_prompt_data, "collection_id": collection_id}
        prompt_response = client.post("/prompts", json=prompt_data)
        prompt_id = prompt_response.json()["id"]
        
        # Delete collection
        client.delete(f"/collections/{collection_id}")
        # The prompt still exists but has invalid collection_id
        # This is Bug #4 - should be handled properly
        prompts = client.get("/prompts").json()["prompts"]

        assert len(prompts) == 0, "Prompts should be deleted when the collection is deleted"
   


class TestUpdateTimestamp:
    """Tests for verifying updated_at timestamp is properly updated."""
    
    def test_update_prompt_updates_timestamp(self, client: TestClient, sample_prompt_data):
        """Test that updated_at timestamp changes when prompt is updated.
        
        Verifies Bug #2 is fixed - updated_at should reflect the current time.
        """
        import time
        from datetime import datetime
        
        # Create a prompt
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]
        original_updated_at = create_response.json()["updated_at"]
        
        # Wait a bit to ensure time passes
        time.sleep(0.2)
        
        # Update the prompt
        updated_data = {
            "title": "Updated Title",
            "content": "Updated content",
            "description": "Updated description"
        }
        
        update_response = client.put(f"/prompts/{prompt_id}", json=updated_data)
        new_updated_at = update_response.json()["updated_at"]
        
        # Verify the timestamp was updated
        assert new_updated_at != original_updated_at, \
            "Bug #2: updated_at should change when prompt is updated"
    
    def test_update_prompt_timestamp_is_current(self, client: TestClient, sample_prompt_data):
        """Test that updated_at is approximately the current time after update.
        
        Verifies the timestamp is not stale or incorrect.
        """
        import time
        from datetime import datetime
        
        # Create a prompt
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]
        
        # Record time before update
        time_before_update = datetime.utcnow()
        
        # Update the prompt
        updated_data = {
            "title": "New Title",
            "content": "New content here",
            "description": "New desc"
        }
        
        update_response = client.put(f"/prompts/{prompt_id}", json=updated_data)
        updated_at_str = update_response.json()["updated_at"]
        
        # Parse the returned datetime
        # Handle both ISO format strings and datetime objects
        if isinstance(updated_at_str, str):
            updated_at = datetime.fromisoformat(updated_at_str.replace('Z', '+00:00'))
        else:
            updated_at = datetime.fromisoformat(str(updated_at_str))
        
        time_after_update = datetime.utcnow()
        
        # Verify updated_at is between before and after (within 1 second tolerance)
        assert time_before_update <= updated_at <= time_after_update, \
            "updated_at should be approximately current time, not stale"
    
    def test_update_prompt_preserves_created_at(self, client: TestClient, sample_prompt_data):
        """Test that created_at stays the same but updated_at changes.
        
        Verifies that only the updated_at timestamp is modified, not created_at.
        """
        import time
        
        # Create a prompt
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]
        original_created_at = create_response.json()["created_at"]
        original_updated_at = create_response.json()["updated_at"]
        
        # Wait briefly
        time.sleep(0.2)
        
        # Update the prompt
        updated_data = {
            "title": "Modified Title",
            "content": "Modified content text",
            "description": "Modified description"
        }
        
        update_response = client.put(f"/prompts/{prompt_id}", json=updated_data)
        new_created_at = update_response.json()["created_at"]
        new_updated_at = update_response.json()["updated_at"]
        
        # Verify created_at hasn't changed
        assert new_created_at == original_created_at, \
            "created_at should not change when updating a prompt"
        
        # Verify updated_at did change
        assert new_updated_at != original_updated_at, \
            "updated_at should change when updating a prompt"
