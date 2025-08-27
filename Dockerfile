# Use a Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS uv

# Install the project into `/app`
WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1
# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

# Copy dependency files first for better caching
COPY uv.lock pyproject.toml ./

# Install the project's dependencies WITHOUT cache mounts (Railway safe)
RUN uv sync --frozen --no-install-project --no-dev --no-editable

# Then, add the rest of the project source code and install it
COPY . /app

# Install the project itself WITHOUT cache mounts
RUN uv sync --frozen --no-dev --no-editable

# Runtime stage
FROM python:3.12-slim-bookworm

# Create app user for security
RUN groupadd --gid 1000 app && \
    useradd --uid 1000 --gid app --shell /bin/bash --create-home app

# Set working directory
WORKDIR /app

# Copy virtual environment from builder stage
COPY --from=uv --chown=app:app /app/.venv /app/.venv

# Make sure we use venv
ENV PATH="/app/.venv/bin:$PATH"

# Switch to non-root user
USER app

# Health check (optional)
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import sys; sys.exit(0)" || exit 1

# Default command - can be overridden with environment variables
ENTRYPOINT ["mcp-server-rabbitmq"]

# Default arguments - these will be used if no other args are provided
CMD ["--help"]
