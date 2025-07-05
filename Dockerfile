FROM python:3.13.5-slim

# Install system dependencies (including mkvmerge)
RUN apt-get update && apt-get install -y \
    mkvtoolnix \
    && rm -rf /var/lib/apt/lists/*
# Set the working directory
WORKDIR /app
# Copy the requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "src/main.py"]

