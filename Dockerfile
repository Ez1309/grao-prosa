# Imagem base oficial do Python (leve e estável)
FROM python:3.12-slim

# Evita criação de arquivos .pyc e garante saída imediata de logs no terminal
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Diretório de trabalho dentro do container
WORKDIR /app

# Instalação das dependências
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia o código da aplicação
COPY . .

# Porta exposta pelo servidor de desenvolvimento do Django
EXPOSE 8000

# Comando padrão de inicialização
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
