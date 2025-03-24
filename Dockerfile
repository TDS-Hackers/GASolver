FROM python:3.12-slim-bookworm

# Set working directory
WORKDIR /code

# Copy and install dependencies
COPY requirements.txt .  
RUN pip install --no-cache-dir --upgrade -r requirements.txt && rm -rf /root/.cache/pip

# Copy the rest of the application
COPY . .

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
