# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies for pytesseract and other packages
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-eng \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    wget \
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

# Install conda packages
RUN conda run -n chatbot_env conda install -c conda-forge -y \
    fastapi \
    uvicorn \
    langchain \
    langchain-ollama \
    langchain-community \
    chromadb \
    pydantic

# Copy requirements and install remaining pip dependencies
COPY requirements.txt .
RUN conda run -n chatbot_env pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Create directory for FAISS database
RUN mkdir -p faiss_db

# Expose port
EXPOSE 8000

# Command to run the application
CMD ["conda", "run", "-n", "chatbot_env", "python", "main.py"]