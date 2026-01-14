# Firewall and Offline Deployment Guide

This guide describes how to build and deploy Open Notebook in environments with restricted internet access, such as behind corporate firewalls or in air-gapped systems.

## Docker Build Configuration

We provide several build arguments to configure custom package registries and download URLs.

### Python Package Registry (PyPI)

If you use a private PyPI mirror (e.g., Artifactory, Nexus), you can configure `uv` (the python package manager we use) with the following build arguments:

- `UV_INDEX_URL`: The URL of the primary package index.
- `UV_EXTRA_INDEX_URL`: URL for an extra package index.

**Example:**
```bash
docker build \
  --build-arg UV_INDEX_URL=https://pypi.your-company.com/simple \
  -t open-notebook .
```

### Node.js Package Registry (npm)

To use a custom npm registry:

- `NPM_CONFIG_REGISTRY`: The URL of the npm registry.

**Example:**
```bash
docker build \
  --build-arg NPM_CONFIG_REGISTRY=https://npm.your-company.com/ \
  -t open-notebook .
```

### System Dependencies URLs

Some system dependencies are installed via `curl`. You can override the URLs if you host these scripts internally:

- `NODE_SETUP_URL`: URL for the Node.js setup script (default: `https://deb.nodesource.com/setup_20.x`).
- `SURREALDB_INSTALL_URL`: URL for the SurrealDB install script (only used in `Dockerfile.single`, default: `https://install.surrealdb.com`).

**Example:**
```bash
docker build \
  --build-arg NODE_SETUP_URL=http://internal-mirror/setup_20.x \
  -f Dockerfile.single .
```

### HTTP Proxies

Docker supports `http_proxy` and `https_proxy` build arguments natively.

**Example:**
```bash
docker build \
  --build-arg http_proxy=http://proxy.company.com:8080 \
  --build-arg https_proxy=http://proxy.company.com:8080 \
  -t open-notebook .
```

## Runtime Configuration

### Offline Token Counting (tiktoken)

Open Notebook uses `tiktoken` to count tokens for LLM usage tracking. By default, `tiktoken` attempts to download encoding files (specifically `o200k_base` for GPT-4o compatibility) from the internet.

If the application is running offline:
1.  **Automatic Fallback**: The system detects if the encoding cannot be loaded (e.g., due to no internet) and falls back to a simple word-count based approximation. A warning will be logged.
2.  **Cached Mode**: If you require exact token counting, you can pre-populate the tiktoken cache directory.

The cache directory is located at `./data/tiktoken-cache` inside the container (mapped to `data/tiktoken-cache` on host if using standard volumes).

**To pre-populate the cache:**
Run the following Python script on a machine with internet access:

```python
import tiktoken
import os

# Set cache dir to a local folder
os.environ["TIKTOKEN_CACHE_DIR"] = "./tiktoken-cache"

# Download the encoding
tiktoken.get_encoding("o200k_base")

print("Encoding downloaded to ./tiktoken-cache")
```

Then copy the contents of `./tiktoken-cache` to the `data/tiktoken-cache` directory on your offline server.
