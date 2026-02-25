# PromptLab

**Enterprise-Grade AI Prompt Engineering Platform**

[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/fastapi-latest-009688.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## Project Overview

**PromptLab** is a professional-grade platform designed for AI engineers, data scientists, and prompt specialists to collaboratively store, organize, and manage AI prompts with precision and scale.

### Problem Statement

AI teams waste significant time managing prompt variations, searching through ad-hoc documents, and losing institutional knowledge. PromptLab centralizes prompt management through a clean, RESTful API with persistent storage, powerful search capabilities, and intuitive organization through collections.

### Target Audience

- AI/ML engineers and teams
- Prompt specialists managing multiple language models
- Organizations requiring audit trails and version control for prompts
- Development teams integrating LLM capabilities into production applications

### Architecture Overview

PromptLab follows a **three-tier architecture**:

```
┌──────────────────┐
│   FastAPI REST   │  HTTP Layer (OpenAPI spec)
├──────────────────┤
│   Business Logic │  Models, validation, utilities
├──────────────────┤
│  SQLite Storage  │  Persistent data layer
└──────────────────┘
```

---

## Features

### Core Prompt Management
- **Create & Store Prompts**: Store prompts with title, content, description, and metadata
- **Full CRUD Operations**: Complete create, read, update, and delete support for prompts
- **Partial Updates**: PATCH endpoint for targeted field updates without overwriting unchanged data
- **Template Variables**: Support for prompt templating with `{{variable}}` syntax

### Organization & Discovery
- **Collections**: Group related prompts into logical collections
- **Full-Text Search**: Case-insensitive search across prompt titles and descriptions
- **Filtering**: Filter prompts by collection membership
- **Sorting**: Automatic sorting by creation date with ascending/descending options

### API & Integration
- **RESTful Design**: Standard HTTP methods and status codes for predictable integration
- **OpenAPI Documentation**: Auto-generated interactive API documentation at `/docs`
- **Pydantic Validation**: Strict type validation and automatic request/response serialization
- **CORS Support**: Cross-origin requests enabled for frontend integration
- **Production-Ready Error Handling**: Descriptive HTTP exceptions with appropriate status codes

### Data Persistence
- **SQLite Database**: Lightweight, serverless persistence suitable for development and production
- **Transaction Support**: Atomic operations with proper session management
- **Indexed Queries**: Optimized database indexing on frequently queried fields
- **Data Integrity**: Foreign key relationships and validation constraints

---

## Prerequisites

### System Requirements
- **Python**: 3.10 or higher
- **pip**: Package installer for Python
- **Git**: Version control system

### Runtime Dependencies
All dependencies are specified in `requirements.txt`:
- FastAPI 0.104.1
- Uvicorn (ASGI server)
- SQLAlchemy (ORM)
- Pydantic (data validation)
- pytest (testing framework)

### Environment Setup
- No external services required (SQLite is included)
- No special accounts or API keys needed for local development

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/SarasAI-Institute/10x-engineer-project-repo.git
cd 10x-engineer-project-repo/backend
```

### 2. Create Virtual Environment

```bash
# macOS/Linux
python3.10 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment (Optional)

Create a `.env` file in the backend directory:

```env
# Database Configuration
DATABASE_URL=sqlite:///promptlab.db

# API Configuration
API_TITLE=PromptLab API
API_VERSION=1.0.0
API_DESCRIPTION=AI Prompt Engineering Platform

# Server Configuration
DEBUG=False
HOST=0.0.0.0
PORT=8000
```

### 5. Initialize Database

The database is automatically created on first run. No manual migrations are required.

```bash
# Database file will be created at: backend/promptlab.db
```

---

## Quick Start Guide

### Running the Server

```bash
cd backend
python main.py
```

**Expected Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

### Accessing the Application

- **API Endpoint**: http://localhost:8000
- **Interactive API Docs**: http://localhost:8000/docs (Swagger UI)
- **Alternative Docs**: http://localhost:8000/redoc (ReDoc)
- **OpenAPI Schema**: http://localhost:8000/openapi.json

### Example Requests

#### 1. Health Check

```bash
curl -X GET http://localhost:8000/health
```

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

#### 2. Create a Prompt

```bash
curl -X POST http://localhost:8000/prompts \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Customer Service Response",
    "content": "You are a helpful customer service agent. A customer has written: {{customer_inquiry}}. Respond professionally and briefly.",
    "description": "Template for responding to customer inquiries",
    "collection_id": null
  }'
```

**Response:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Customer Service Response",
  "content": "You are a helpful customer service agent. A customer has written: {{customer_inquiry}}. Respond professionally and briefly.",
  "description": "Template for responding to customer inquiries",
  "collection_id": null,
  "created_at": "2024-02-16T10:30:00",
  "updated_at": "2024-02-16T10:30:00"
}
```

#### 3. Search Prompts

```bash
curl -X GET "http://localhost:8000/prompts?search=customer" \
  -H "Accept: application/json"
```

**Response:**
```json
{
  "prompts": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "Customer Service Response",
      "content": "...",
      "description": "Template for responding to customer inquiries",
      "collection_id": null,
      "created_at": "2024-02-16T10:30:00",
      "updated_at": "2024-02-16T10:30:00"
    }
  ],
  "total": 1
}
```

#### 4. Retrieve a Specific Prompt

```bash
curl -X GET http://localhost:8000/prompts/550e8400-e29b-41d4-a716-446655440000
```

---

## API Endpoint Summary

### Prompts

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| GET | `/prompts` | List all prompts (supports search & filter) | None |
| GET | `/prompts/{prompt_id}` | Retrieve a specific prompt | None |
| POST | `/prompts` | Create a new prompt | None |
| PUT | `/prompts/{prompt_id}` | Replace entire prompt | None |
| PATCH | `/prompts/{prompt_id}` | Partially update prompt | None |
| DELETE | `/prompts/{prompt_id}` | Delete a prompt | None |

**Query Parameters for GET /prompts:**
- `search` (optional): Search in title and description
- `collection_id` (optional): Filter by collection

### Collections

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| GET | `/collections` | List all collections | None |
| GET | `/collections/{collection_id}` | Retrieve a collection | None |
| POST | `/collections` | Create a new collection | None |
| DELETE | `/collections/{collection_id}` | Delete collection and all prompts | None |

### Health Check

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| GET | `/health` | API health status | None |

---

## Development Setup

### Running in Development Mode

```bash
cd backend

# With auto-reload on file changes
uvicorn app.api:app --reload --host 0.0.0.0 --port 8000
```

### Running Tests

```bash
cd backend

# Run all tests with verbose output
pytest tests/ -v

# Run specific test file
pytest tests/test_api.py -v

# Run with coverage
pytest tests/ --cov=app
```

### Code Formatting & Linting

```bash
# Format code with Black
black app/ tests/

# Lint with Pylint
pylint app/

# Type checking with mypy
mypy app/
```

### Project Structure

```
backend/
├── app/
│   ├── __init__.py              # Package initialization
│   ├── api.py                   # FastAPI routes and endpoints
│   ├── models.py                # Pydantic data models
│   ├── storage.py               # SQLite database layer
│   └── utils.py                 # Helper and utility functions
├── tests/
│   ├── __init__.py
│   ├── conftest.py              # Pytest configuration and fixtures
│   └── test_api.py              # API endpoint tests
├── main.py                      # Application entry point
├── requirements.txt             # Python dependencies
└── promptlab.db                 # SQLite database (auto-created)
```

### Key Modules

- **api.py**: FastAPI application with all HTTP endpoints
- **models.py**: Pydantic models for request/response validation
- **storage.py**: SQLAlchemy ORM and database operations
- **utils.py**: Helper functions for sorting, filtering, and searching

---

## Contributing Guidelines

### Branching Strategy

We follow a simplified Git Flow:

```
main (production)
  └─ develop (staging)
      └─ feature/*, bugfix/*, docs/*
```

**Branch Naming Convention:**
- Features: `feature/feature-name`
- Bug fixes: `bugfix/issue-description`
- Documentation: `docs/topic-name`
- Example: `feature/add-prompt-versioning`

### Commit Message Format

```
<type>: <subject>

<body>

<footer>
```

**Types:** `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

**Examples:**
```
feat: add support for prompt templates

fix: correct collection deletion cascade behavior

docs: update API endpoint documentation
```

### Pull Request Process

1. **Create a well-scoped PR** against the `develop` branch
2. **Provide a clear description** of changes and motivation
3. **Link related issues** using `#issue-number`
4. **Include test coverage** for new functionality
5. **Request review** from team members
6. **Address feedback** before merging

**PR Template:**
```
## Description
Brief summary of changes

## Related Issues
Fixes #123

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update

## Testing
- [ ] Added unit tests
- [ ] All tests passing
```

### Code Style Expectations

- **Language**: Python 3.10+
- **Formatter**: Black (line length: 88)
- **Linter**: Pylint
- **Type Hints**: Required for function signatures
- **Docstrings**: Google-style docstrings for all public functions and classes
- **Testing**: Minimum 80% code coverage for new features

**Style Guide:**
```python
# Good: Type hints and docstring
def create_prompt(data: PromptCreate) -> Prompt:
    """Create a new prompt in the database.
    
    Args:
        data: Prompt creation request data.
        
    Returns:
        The created Prompt object.
    """
    # implementation
    pass

# Good: Clear variable names
user_prompts = storage.get_prompts_by_collection(collection_id)

# Avoid: Unclear names
ps = storage.get_prompts_by_collection(cid)
```

### Reporting Issues

Use the GitHub issue tracker with these templates:

**Bug Report:**
- Title: `[BUG] Clear, specific title`
- Description: Steps to reproduce, expected behavior, actual behavior
- Example: `[BUG] Creating prompt with empty title raises 500 error`

**Feature Request:**
- Title: `[FEATURE] Clear title`
- Description: Use case, proposed solution, alternatives considered
- Example: `[FEATURE] Add batch import/export for prompts`

---

## Week 3 Submission Summary (Prompt Versions + TDD)

Implemented the **Prompt Versions** feature using a test-driven workflow.

### TDD Flow Used

1. Added failing tests in `backend/tests/test_api.py` for version creation, listing, restore, and single-version retrieval.
2. Implemented version data models in `backend/app/models.py`.
3. Implemented storage support in `backend/app/storage.py` (create/list/get versions and cleanup).
4. Implemented API endpoints in `backend/app/api.py`.
5. Re-ran targeted tests and then full backend tests until all passed.

### Prompt Versions Endpoints Added

- `POST /prompts/{prompt_id}/versions` — create immutable snapshot
- `GET /prompts/{prompt_id}/versions` — list prompt versions
- `GET /prompts/{prompt_id}/versions/{version_id}` — get one version
- `POST /prompts/{prompt_id}/versions/{version_id}/restore` — restore prompt from snapshot

### Verification

- Full backend test suite passes after implementation.
- API documentation updated in `docs/API_REFERENCE.md` with request/response examples and error cases.

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) file for details.

---

## Support & Contact

For issues, feature requests, or questions:
- **GitHub Issues**: [Report an issue](https://github.com/SarasAI-Institute/10x-engineer-project-repo/issues)
- **Documentation**: See `/docs` and `/specs` directories for detailed guides

---

**Last Updated**: February 2024  
**Version**: 1.0.0
