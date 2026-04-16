# Use Python slim image for smaller size
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY azure_devops_mcp_server.py .
COPY .env.example .env.example

# Create non-root user for security
RUN useradd -m -u 1000 mcpuser && \
    chown -R mcpuser:mcpuser /app

USER mcpuser

# Environment variables (can be overridden)
ENV AZURE_DEVOPS_PAT="" \
    AZURE_DEVOPS_ORG_URL="" \
    AZURE_DEVOPS_USERNAME="" \
    AZURE_DEVOPS_PROJECT=""

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"

# Run the MCP server
CMD ["python", "azure_devops_mcp_server.py"]
