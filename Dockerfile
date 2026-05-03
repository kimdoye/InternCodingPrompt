# Use a specific Python version for reproducibility
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

# Set the working directory
WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy only requirements to cache them in a separate layer
COPY pyproject.toml uv.lock ./

# Install dependencies without the project itself to cache them
# This ensures that changes to source code don't trigger a full re-install
RUN uv sync --frozen --no-install-project --no-dev

# Copy the rest of the application source code
COPY . .

# Install the project (this will be fast since dependencies are already cached)
RUN uv sync --frozen --no-dev

# Final runtime image: use a slim version for production
FROM python:3.12-slim-bookworm

WORKDIR /app

# Copy the virtual environment from the builder stage
COPY --from=builder /app/.venv /app/.venv

# Copy the application source code
COPY . .

# Set environment variables to use the virtual environment
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Expose the port the app runs on
EXPOSE 5000

# Run the application using the entry point in app.py
CMD ["python", "app.py"]
