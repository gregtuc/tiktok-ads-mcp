FROM python:3.12-slim

WORKDIR /app

# Copy all necessary files for installation
COPY requirements.txt pyproject.toml README.md LICENSE ./
COPY tiktok_ads_mcp/ ./tiktok_ads_mcp/

# Install dependencies
RUN pip install --no-cache-dir -e .

# Run the MCP server
CMD ["python", "-m", "tiktok_ads_mcp"]
