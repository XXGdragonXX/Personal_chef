# Use official Python image
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy dependencies and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Set environment variable to ensure frontend connects to backend inside the container
ENV BACKEND_URL="http://localhost:8000/submit"

# Expose ports for FastAPI (8000) and Streamlit (8501)
EXPOSE 8000 8501

# Run FastAPI in the background & Streamlit in the foreground
CMD uvicorn api:app --host 0.0.0.0 --port 8000 & streamlit run UI.py --server.port=8501 --server.address=0.0.0.0
