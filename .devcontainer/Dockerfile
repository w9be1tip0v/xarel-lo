# Use base image of Python 3.9
FROM python:3.9-slim

# Set working directory
WORKDIR /workspace

# Install necessary packages
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Run as non-root user
RUN useradd -m vscode
USER vscode