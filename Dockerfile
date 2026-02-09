# Use official Python 3.11 image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy project files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Expose Streamlit default port
EXPOSE 8501

# Command to run Streamlit
CMD ["streamlit", "run", "scripts/dashboard.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.enableCORS=false"]
