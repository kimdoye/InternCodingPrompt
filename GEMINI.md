# Gemini CLI Project Instructions: Intern Coding Prompt

## Project Overview
This project is a task management API designed as a migration exercise from **Flask** to **FastAPI**. It features a standard CRUD interface for tasks using in-memory storage. The project emphasizes modern Python development practices, including the use of `uv` for package management and containerization with Docker.

### Key Technologies
- **Language:** Python 3.11+
- **Current Framework:** Flask 3.0.0
- **Target Framework:** FastAPI
- **Package Management:** `uv`
- **Validation:** Pydantic (for FastAPI migration)
- **Testing:** Pytest
- **Deployment:** Docker

## Project Structure
- `app.py`: The entry point of the application.
- `api/`: Contains the core logic.
    - `routes.py`: Endpoint definitions (Flask Blueprints).
    - `controllers.py`: Business logic and in-memory task storage.
- `tests/`: Comprehensive test suite using Pytest.
- `Dockerfile`: Containerization configuration.
- `pyproject.toml`: Dependency management and project metadata.

## Building and Running

### Local Development
Ensure you have `uv` installed.

1.  **Install dependencies:**
    ```bash
    uv sync
    ```
2.  **Run the application (Flask - Current):**
    ```bash
    uv run python app.py
    ```
3.  **Run the application (FastAPI - Post-Migration):**
    ```bash
    uv run uvicorn app:app --reload
    ```
4.  **Run tests:**
    ```bash
    uv run pytest
    ```

### Docker
1.  **Build image:**
    ```bash
    docker build -t intern-coding-prompt .
    ```
2.  **Run container:**
    ```bash
    docker run -p 5000:5000 intern-coding-prompt
    ```
    *(Note: Change port to 8000 after FastAPI migration)*

## Development Conventions

### Migration Rules
- **Contract Fidelity:** Maintain the exact API contract (endpoint paths, methods, and response structures) to ensure existing tests pass.
- **FastAPI Idioms:** Use dependency injection, Pydantic models for request/response validation, and `async/await` where appropriate.
- **Error Handling:** Implement robust error handling using FastAPI's exception handlers to match the expected JSON error responses (e.g., `{"error": "..."}`).

### Testing
- **Do Not Edit Tests:** The files in `tests/` are the ground truth for success. Your migration is complete only when all tests pass unmodified.
- **Coverage:** Aim for high code coverage. A GitHub Actions workflow is expected for automated testing.

### Docker
- Use `python:3.11-slim` or similar lightweight images.
- Utilize `uv` inside the Dockerfile for fast dependency installation.
- Implement multi-stage builds if optimization is required.

## API Endpoints
| Method | Endpoint            | Description                   |
| :----- | :------------------ | :---------------------------- |
| GET    | `/tasks`            | List all tasks                |
| GET    | `/tasks/{task_id}`   | Get a specific task by ID     |
| POST   | `/tasks`            | Create a new task             |
| PUT    | `/tasks/{task_id}`   | Update an existing task       |
| DELETE | `/tasks/{task_id}`   | Delete a task                 |
| GET    | `/health`           | System health check           |
