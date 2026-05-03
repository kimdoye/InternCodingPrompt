# Intern Coding Prompt: Task Management API (FastAPI)

## Overview

This repository contains a FastAPI application that provides a CRUD (Create, Read, Update, Delete) API for task management. This project was migrated from Flask to FastAPI to utilize modern Python features, Pydantic for data validation, and `uv` for high-performance package management.

## Features

- **FastAPI Framework:** High performance, easy to use, and automatic OpenAPI documentation.
- **Pydantic Validation:** Strict data typing and validation for request and response models.
- **`uv` Package Management:** Fast and reliable dependency resolution and environment management.
- **In-Memory Storage:** Efficient task storage using Python dictionaries.
- **Comprehensive Testing:** Robust unit test suite ensuring API stability.

## API Endpoints

- **GET /tasks** - Retrieve all tasks
- **GET /tasks/{task_id}** - Retrieve a specific task by ID
- **POST /tasks** - Create a new task
- **PUT /tasks/{task_id}** - Update an existing task
- **DELETE /tasks/{task_id}** - Delete a task
- **GET /health** - Health check endpoint

## Getting Started

### Prerequisites

- Python 3.11 or higher
- [uv](https://github.com/astral-sh/uv) installed on your system

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd intern-coding-prompt
    ```

2.  **Sync dependencies:**
    Use `uv` to create a virtual environment and install all dependencies:
    ```bash
    uv sync
    ```

### Running the Application

Start the FastAPI application using `uv`:

```bash
uv run uvicorn app:app --host 0.0.0.0 --port 5000 --reload
```

The API will be available at `http://localhost:5000`.

### API Documentation

Once the application is running, you can access the interactive API documentation at:
- **Swagger UI:** `http://localhost:5000/docs`
- **ReDoc:** `http://localhost:5000/redoc`

## Running Tests

To run the unit test suite and ensure everything is working correctly:

```bash
uv run pytest
```

## Example API Usage

```bash
# Create a task
curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Complete Step 2", "description": "Update README with uv instructions"}'

# Get all tasks
curl http://localhost:5000/tasks

# Get a specific task
curl http://localhost:5000/tasks/{task_id}

# Update a task
curl -X PUT http://localhost:5000/tasks/{task_id} \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'

# Delete a task
curl -X DELETE http://localhost:5000/tasks/{task_id}

# Health check
curl http://localhost:5000/health
```

## Project Structure

```text
.
├── api/                # FastAPI application logic
│   ├── controllers.py  # Business logic and CRUD handlers
│   ├── models.py       # Pydantic schemas (Request/Response)
│   └── routes.py       # API route definitions
├── tests/              # Legacy unit tests (untouched)
├── app.py              # Application entry point & Compatibility layer
├── Dockerfile          # Multi-stage production Docker build
├── pyproject.toml      # Project dependencies and metadata
└── .github/            # GitHub Actions CI workflow
```

## CI/CD

This project uses **GitHub Actions** for continuous integration. On every push or pull request to the `main` or `master` branches, the workflow:
1. Sets up a Python 3.12 environment.
2. Installs dependencies using `uv`.
3. Runs the full test suite with `pytest`.
4. Generates a code coverage report using `pytest-cov`.

## Docker Support

The project is containerized using a high-performance **multi-stage Docker build**:
- **Builder stage:** Uses the `uv` image to resolve dependencies and build the virtual environment.
- **Runtime stage:** Uses a slim Python 3.12 image to host the application, resulting in a minimized production image size.

To build and run the application in a container:

```bash
docker build -t task-api .
docker run -p 5000:5000 task-api
```
