# Use Python base image
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy all files
COPY . .

# Install dependencies
RUN pip install pydantic

# Run your project
CMD ["python", "inference.py"]