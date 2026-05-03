from fastapi import FastAPI, Request, HTTPException as FastAPIHTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from api.routes import router
from fastapi.testclient import TestClient
import json

app = FastAPI()

# Register the router
app.include_router(router)

# Custom exception handler for validation errors to match Flask response format
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={"error": "Invalid data provided"},
    )

# Custom exception handler for FastAPI HTTPExceptions to flatten the "detail" key
@app.exception_handler(FastAPIHTTPException)
async def http_exception_handler(request: Request, exc: FastAPIHTTPException):
    if isinstance(exc.detail, dict) and "error" in exc.detail:
        return JSONResponse(
            status_code=exc.status_code,
            content=exc.detail,
        )
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": str(exc.detail)},
    )

# Compatibility layer for Flask unit tests
class FlaskCompatibleResponse:
    def __init__(self, response):
        self._response = response
        self.status_code = response.status_code
        self.data = response.content
    
    @property
    def json(self):
        return self._response.json()

class FlaskCompatibleClient(TestClient):
    def _filter_kwargs(self, kwargs):
        # Remove Flask-specific kwargs that TestClient doesn't like
        kwargs.pop('content_type', None)
        return kwargs

    def get(self, *args, **kwargs):
        return FlaskCompatibleResponse(super().get(*args, **self._filter_kwargs(kwargs)))
    
    def post(self, *args, **kwargs):
        return FlaskCompatibleResponse(super().post(*args, **self._filter_kwargs(kwargs)))
    
    def put(self, *args, **kwargs):
        return FlaskCompatibleResponse(super().put(*args, **self._filter_kwargs(kwargs)))
    
    def delete(self, *args, **kwargs):
        return FlaskCompatibleResponse(super().delete(*args, **self._filter_kwargs(kwargs)))

    def __enter__(self):
        # Flask's test_client context manager returns the client itself
        super().__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        super().__exit__(exc_type, exc_val, exc_tb)

class MockConfig(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    def __setitem__(self, key, value):
        super().__setitem__(key, value)
    def __getitem__(self, key):
        return super().get(key, None)

app.config = MockConfig()
app.test_client = lambda: FlaskCompatibleClient(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
