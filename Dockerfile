# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies for pytesseract and PyTorch
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-eng \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libgthread-2.0-0 \
    libglib2.0-0 \
    wget \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Miniconda
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh && \
    /opt/conda/bin/conda clean --all --yes && \
    ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate base" >> ~/.bashrc

# Set PATH for conda
ENV PATH=/opt/conda/bin:$PATH

# Accept conda ToS
RUN conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main && \
    conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r

# Create conda environment
RUN conda create -n chatbot_env python=3.11 -y

# Copy requirements and install all dependencies via pip
COPY requirements.txt .
RUN conda run -n chatbot_env pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Create directories for FAISS database and model cache
RUN mkdir -p faiss_db models

# Set Hugging Face cache directory
ENV HF_HOME=/app/models
ENV TRANSFORMERS_CACHE=/app/models

# Expose port
EXPOSE 8000

# Command to run the application
CMD ["conda", "run", "-n", "chatbot_env", "python", "main.py"]