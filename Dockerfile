FROM python:3.12.7-slim
WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir -r uv
COPY pyproject.toml uv.lock /app/
RUN uv pip install -r uv.lock

# Copy the rest of the code
COPY . /app

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]