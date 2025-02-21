FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Set the PYTHONPATH environment variable
ENV PYTHONPATH=/app

# Copy the requirements file first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN apt-get update && apt-get install -y postgresql-client
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Make the script executable
RUN chmod +x wait-for-db.sh

# Command to run the application
CMD ["./wait-for-db.sh", "uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "8000"]