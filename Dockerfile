FROM python:3.14-slim-bookworm

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY ../src ./src
COPY ../pyproject.toml ./pyproject.toml
RUN pip install --no-cache-dir -e .

COPY ./app .

EXPOSE 8501

CMD ["streamlit", "run", "main.py", "--server.address=0.0.0.0", "--server.enableCORS=false", "--server.enableXsrfProtection=false"]