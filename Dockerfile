FROM python:3.10-slim

WORKDIR /app

# install dependency system
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libpq-dev \
    curl \
    netcat-openbsd \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# upgrade pip and pin setuptools/wheel to fix compatibility with older catboost/xgboost
RUN pip install --upgrade pip
RUN pip install "setuptools<70.0.0" "wheel<0.44.0"

# copy requirements
COPY requirements.txt .

# install python dependency
RUN pip install --no-cache-dir -r requirements.txt

# copy project
COPY . .

# permission script
RUN chmod +x docker/wait-for-db.sh

EXPOSE 5000

CMD ["sh", "docker/wait-for-db.sh"]