FROM python:3.12-slim

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    ffmpeg \
    wget \
    gnupg \
    unzip \
    curl \
    xvfb \
    # Chrome/Chromium para Selenium
    chromium \
    chromium-driver \
    # Dependências para processamento de imagem/vídeo
    libgl1 \
    libglib2.0-0 \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Define diretório de trabalho
WORKDIR /app

# Copia arquivos de dependências
COPY requirements.txt .

# Instala dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação
COPY . .

# Define variáveis de ambiente
ENV PYTHONUNBUFFERED=1
ENV DISPLAY=:99
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver

# Pasta para output e logs
RUN mkdir -p /app/output /app/logs

# Comando padrão
CMD ["python3", "main.py"]

