FROM python:3.10-bullseye

ENV DEBIAN_FRONTEND=noninteractive

# Install OS-level dependencies for audio + ffmpeg
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libsndfile1 \
    libavformat-dev \
    libavdevice-dev \
    libavfilter-dev \
    libavcodec-dev \
    libavutil-dev \
    libswscale-dev \
    libswresample-dev \
    build-essential \
    pkg-config \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy your app code
COPY . .

EXPOSE 8501

# Run Streamlit app
CMD ["streamlit", "run", "app_ui.py", "--server.port=8501", "--server.address=0.0.0.0"]
