FROM python:3.12-slim

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    ffmpeg \
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

# Pasta para output
RUN mkdir -p /app/output

# Comando padrão
CMD ["python3", "create_lofi_video.py", "--help"]

