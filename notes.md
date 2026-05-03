# Project Migration Notes: Flask to FastAPI

## Step 1: Convert Flask to FastAPI
**Status: Completed**

### Implementation Details
- **Architecture:** Refactored the monolithic `app.py` into a modular structure using FastAPI's `APIRouter`.
- **Data Models:** Introduced Pydantic models in `api/models.py` for structured request validation (`TaskCreate`, `TaskUpdate`) and response serialization (`Task`).
- **In-Memory Storage:** Maintained the existing dictionary-based storage in `api/controllers.py` to ensure consistency with the original exercise.
- **Asynchronous Flow:** While the current implementation uses synchronous controllers (matching the Flask original), the routes are prepared for async integration.

### Compatibility Layer (The "Magic")
A major challenge was the requirement to **not modify existing tests**, which were written for Flask. I implemented a compatibility shim in `app.py`:
- `FlaskCompatibleClient`: A wrapper around FastAPI's `TestClient` that filters out Flask-specific arguments like `content_type` and mimics the context manager behavior of Flask's test client.
- `FlaskCompatibleResponse`: A wrapper that provides the `.data` attribute (returning bytes) and `.json` property expected by the legacy tests.
- `MockConfig`: A simple dictionary-like object attached to the FastAPI app to satisfy tests that attempt to set `app.config['TESTING']`.

### Technical Fixes
- **Validation Errors:** Overrode the default FastAPI `RequestValidationError` handler to return `{"error": "Invalid data provided"}` with a 400 status code, matching the Flask implementation's error format.
- **HTTP Exceptions:** Flattened the default FastAPI "detail" structure to match the expected `{"error": "..."}` format.
- **Deprecations:** Updated Pydantic usage to `ConfigDict` and switched from `utcnow()` to `now(UTC)` to avoid Python 3.12+ warnings.

## Step 2: Modernize Package Management with `uv`
**Status: Completed**

### Actions
- **Dependency Addition:** Used `uv add` to manage `fastapi`, `uvicorn`, and `httpx`.
- **Environment:** Created and managed the virtual environment using `uv sync`.
- **Documentation:** Updated `README.md` with comprehensive instructions for project setup, execution, and testing using `uv`.
- **Note:** The `pyproject.toml` and `uv.lock` are fully managed by `uv`.

## Step 3: Containerize with Docker
**Status: Completed**

### Docker Implementation
- **Multi-Stage Build:** Optimized the image using a `builder` stage for dependency installation and a slim `runtime` stage for the final image.
- **`uv` Integration:** Utilized `ghcr.io/astral-sh/uv` as the builder base to leverage fast dependency resolution and bytecode compilation (`UV_COMPILE_BYTECODE=1`).
- **Layer Caching:** Structured the `Dockerfile` to copy `pyproject.toml` and `uv.lock` first, allowing Docker to cache the virtual environment layer independently of source code changes.
- **Image Optimization:** Added a `.dockerignore` file to exclude unnecessary files (`.venv`, `tests/`, documentation), resulting in a significantly smaller production image.
- **Configuration:** Exposed port 5000 and configured the container to run the application via `python app.py` (which invokes uvicorn).

---
*Next Step: Setup GitHub Actions for CI and coverage.*
