# 1. Base Image: Start with a lightweight Python 3.10
FROM python:3.10-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy just the requirements first (for caching speed)
COPY requirements.txt .

# 4. Install dependencies
# We add --no-cache-dir to keep the image small
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of the application code
COPY . .

# 6. Expose the port Flask runs on
EXPOSE 5000

# 7. The command to run when the container starts
# We use 'gunicorn' (a production server) instead of 'python run.py'
# But for now, let's stick to python run.py to keep it simple
CMD ["python", "run.py"]