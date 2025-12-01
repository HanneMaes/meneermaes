# - "slim" variant is smaller (~120MB vs ~800MB for full Python image). Python 3.11 is stable and widely supported
FROM python:3.11-slim

# Environment variables that will be available inside the container
# PYTHONUNBUFFERED=1 ensures Python output appears immediately in logs
# (without this, output might be delayed/buffered)
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 PIP_NO_CACHE_DIR=1

# Creates /app directory and makes it the current directory
# All subsequent commands run from this directory
# Similar to 'cd /app' in bash
WORKDIR /app

# First, copy requirements.txt separately (Docker layer caching optimization)
# If requirements.txt doesn't change, Docker reuses this layer and doesn't
# reinstall packages on every build
COPY requirements.txt .

# Install Python dependencies
# --no-cache-dir: don't cache downloaded packages (saves space)
RUN pip install --upgrade pip && \
  pip install --no-cache-dir -r requirements.txt

# Now copy all project files
# The '.' at the end means "current directory in container" (/app)
COPY . .

# VOLUME ["/app/scripts"]
# This would create a mount point for external data
# We'll handle this in docker-compose.yml instead for flexibility

# This runs every time you start a container from this image
# /bin/bash starts an interactive bash shell
# You can override this when running: docker run -it myimage python script.py
CMD ["/bin/bash"]
