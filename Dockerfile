FROM python:3.11-slim
WORKDIR /app
RUN pip install poetry==1.8.3
COPY pyproject.toml README.md ./
COPY printclaw ./printclaw
COPY tests ./tests
RUN poetry config virtualenvs.create false && poetry install --without dev --no-interaction --no-ansi
EXPOSE 8080
CMD ["uvicorn", "printclaw.web.app:app", "--host", "0.0.0.0", "--port", "8080"]
