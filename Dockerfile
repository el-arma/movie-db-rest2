# Use an official Python image as the base
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy only the necessary files
COPY main.py database.py schemas.py /app/
COPY movies.db /app/
COPY requirements.txt /app/


# Install dependencies
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Expose the FastAPI port
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
