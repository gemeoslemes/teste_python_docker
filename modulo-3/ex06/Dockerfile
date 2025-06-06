# Usando a imagem oficial do Python como base
FROM python:3.12.10-bullseye

# Definir o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copiar os arquivos do projeto para dentro do contêiner
COPY . /app/

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expor a porta 8080 para acesso externo
EXPOSE 8080

# Definir o ponto de entrada e comando para rodar FastAPI
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8080"]

