FROM python:3.13-slim

WORKDIR /app

# Installer uv (pour uvx)
RUN apt-get update && apt-get install -y curl \
    && curl -LsSf https://astral.sh/uv/install.sh | sh \
    && apt-get clean

COPY . /app

RUN if [ -f requirements.txt ]; then \
        pip install --no-cache-dir --root-user-action=ignore -r requirements.txt; \
    fi

EXPOSE 8777

CMD ["python", "-m", "src.upu.app"]
