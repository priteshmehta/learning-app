FROM python:3.13-slim

# Install required packages
RUN pip install --upgrade pip

# Create app directory
WORKDIR /app

# Copy all files
COPY . .

RUN pip install -r requirements.txt

# Expose both ports
EXPOSE 8000 8501

# Start supervisord
CMD ["/usr/local/bin/supervisord", "-c", "/app/supervisord.conf"]