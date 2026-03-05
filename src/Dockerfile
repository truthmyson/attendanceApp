# Use official Python slim image
FROM python:3.13.7-slim

# Set working directory
WORKDIR /app

# Install dependencies first (cache layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Expose port
EXPOSE 3636

# Run with Gunicorn (production WSGI server)
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:3636", "app:create_app()"]
