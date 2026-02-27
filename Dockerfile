# Base image - official Python runtime
FROM python:3.12-slim

# Set working directory inside the container
WORKDIR /app

# Copy dependencies file first (layer caching optimization)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the port Flask runs on
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]