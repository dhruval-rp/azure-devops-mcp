# Docker Setup Guide

## Quick Start with Docker

### Option 1: Pull from Docker Hub (Easiest)

```bash
# Pull the latest image
docker pull YOUR_DOCKERHUB_USERNAME/azure-devops-mcp:latest

# Run with environment variables
docker run -i --rm \
  -e AZURE_DEVOPS_PAT="your_pat_token" \
  -e AZURE_DEVOPS_ORG_URL="https://dev.azure.com/YourOrg" \
  -e AZURE_DEVOPS_USERNAME="your_username" \
  -e AZURE_DEVOPS_PROJECT="YourProject" \
  YOUR_DOCKERHUB_USERNAME/azure-devops-mcp:latest
```

### Option 2: Build Locally

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/azure-devops-mcp-server.git
cd azure-devops-mcp-server

# Build the image
docker build -t azure-devops-mcp .

# Run the container
docker run -i --rm \
  -e AZURE_DEVOPS_PAT="your_pat_token" \
  -e AZURE_DEVOPS_ORG_URL="https://dev.azure.com/YourOrg" \
  azure-devops-mcp
```

### Option 3: Docker Compose (Recommended for Development)

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your credentials
nano .env

# Update docker-compose.yml to use .env file (uncomment env_file section)

# Start the service
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the service
docker-compose down
```

## VS Code Configuration with Docker

Add to `~/.config/Code/User/mcp.json`:

```json
{
  "servers": {
    "azure-devops": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "-e", "AZURE_DEVOPS_PAT=your_pat_token",
        "-e", "AZURE_DEVOPS_ORG_URL=https://dev.azure.com/YourOrg",
        "-e", "AZURE_DEVOPS_USERNAME=your_username",
        "-e", "AZURE_DEVOPS_PROJECT=YourProject",
        "YOUR_DOCKERHUB_USERNAME/azure-devops-mcp:latest"
      ]
    }
  }
}
```

**Or use environment variables from host:**

```json
{
  "servers": {
    "azure-devops": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "--env-file", "/home/username/path/to/.env",
        "YOUR_DOCKERHUB_USERNAME/azure-devops-mcp:latest"
      ]
    }
  }
}
```

## Building and Publishing to Docker Hub

### First Time Setup

1. **Create Docker Hub account** at https://hub.docker.com

2. **Create access token**:
   - Go to Account Settings → Security → New Access Token
   - Name it "github-actions" or similar
   - Save the token securely

3. **Add secrets to GitHub**:
   - Go to your GitHub repo → Settings → Secrets and variables → Actions
   - Add `DOCKERHUB_USERNAME` (your Docker Hub username)
   - Add `DOCKERHUB_TOKEN` (the access token from step 2)

### Automated Builds

Once secrets are configured, the image builds automatically:

- **Push to `main` branch** → Builds and pushes `latest` tag
- **Create a tag** (e.g., `v1.0.0`) → Builds and pushes version tags
- **Pull request** → Builds but doesn't push (for testing)

### Manual Build and Push

```bash
# Login to Docker Hub
docker login

# Build for multiple platforms
docker buildx create --use
docker buildx build --platform linux/amd64,linux/arm64 \
  -t YOUR_DOCKERHUB_USERNAME/azure-devops-mcp:latest \
  --push .

# Or build for single platform
docker build -t YOUR_DOCKERHUB_USERNAME/azure-devops-mcp:latest .
docker push YOUR_DOCKERHUB_USERNAME/azure-devops-mcp:latest
```

## Image Tags

- `latest` - Latest stable build from main branch
- `v1.0.0` - Specific version release
- `main` - Latest commit to main branch

## Troubleshooting

### Container exits immediately
```bash
# Check logs
docker logs <container-id>

# Run in interactive mode to see errors
docker run -it YOUR_DOCKERHUB_USERNAME/azure-devops-mcp:latest
```

### Environment variables not working
```bash
# Verify variables are set
docker run --rm YOUR_DOCKERHUB_USERNAME/azure-devops-mcp:latest env

# Make sure you're using -e flag for each variable
docker run -i --rm \
  -e AZURE_DEVOPS_PAT="value" \
  -e AZURE_DEVOPS_ORG_URL="value" \
  YOUR_DOCKERHUB_USERNAME/azure-devops-mcp:latest
```

### Cannot pull from Docker Hub
```bash
# Make sure image name is correct
docker pull YOUR_DOCKERHUB_USERNAME/azure-devops-mcp:latest

# Check if image exists on Docker Hub
# Visit: https://hub.docker.com/r/YOUR_DOCKERHUB_USERNAME/azure-devops-mcp
```

## Image Details

- **Base Image**: Python 3.11 Slim
- **Size**: ~150MB (slim, optimized)
- **Platforms**: linux/amd64, linux/arm64
- **User**: Non-root user (mcpuser) for security
- **Working Directory**: /app

## Security Best Practices

1. **Never hardcode credentials** in Dockerfile or docker-compose.yml
2. **Use environment variables** or secrets management
3. **Don't commit .env file** to version control
4. **Rotate PAT tokens** regularly
5. **Use specific image tags** instead of `latest` in production

## Advanced Usage

### Using with Docker Secrets

```bash
# Create secrets
echo "your_pat_token" | docker secret create ado_pat -
echo "https://dev.azure.com/YourOrg" | docker secret create ado_url -

# Use in docker-compose.yml
services:
  azure-devops-mcp:
    secrets:
      - ado_pat
      - ado_url
    environment:
      - AZURE_DEVOPS_PAT_FILE=/run/secrets/ado_pat
```

### Custom Network

```bash
# Create custom network
docker network create mcp-network

# Run container on custom network
docker run -i --rm \
  --network mcp-network \
  --name azure-devops-mcp \
  -e AZURE_DEVOPS_PAT="token" \
  YOUR_DOCKERHUB_USERNAME/azure-devops-mcp:latest
```

## Resources

- [Docker Hub Repository](https://hub.docker.com/r/YOUR_DOCKERHUB_USERNAME/azure-devops-mcp)
- [GitHub Repository](https://github.com/YOUR_USERNAME/azure-devops-mcp-server)
- [Docker Documentation](https://docs.docker.com/)
