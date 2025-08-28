FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose port 5001 as specified in requirements
EXPOSE 5001

# Run the Flask application
CMD ["python", "app.py"]