# Imagem base
FROM python:3.10-slim

# Evita gerar arquivos .pyc
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Diretório dentro do container
WORKDIR /app

# Copia dependências primeiro (cache de build)
COPY requirements.txt .

# Instala dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o projeto
COPY . .

# Porta da API
EXPOSE 9000

# Comando para rodar a aplicação
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9000"]
