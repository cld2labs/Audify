FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Create non-root runtime user
RUN addgroup --system app && adduser --system --ingroup app app

# Copy the requirements file first to leverage Docker layer caching
COPY requirements.txt .

RUN pip install -r requirements.txt

# Copy the rest of the application files into the container
COPY simple_backend.py .
RUN chown -R app:app /app

USER app

# Expose the port the service runs on
EXPOSE 8000

# Command to run the application
CMD ["python", "-m", "uvicorn", "simple_backend:app", "--host", "0.0.0.0", "--port", "8000"]
