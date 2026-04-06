FROM python:3.12-slim

WORKDIR /app

# install dependency system
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libpq-dev \
    curl \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# upgrade pip
RUN pip install --upgrade pip setuptools wheel

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