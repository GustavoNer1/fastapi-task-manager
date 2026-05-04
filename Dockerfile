FROM python:3.14-slim
ENV POETRY_VIRTUALENVS_CREATE=false
WORKDIR app/
COPY . .
COPY entrypoint.sh /entrypoint.sh

RUN pip install poetry
RUN chmod +x /entrypoint.sh



RUN poetry config installer.max-workers 10
RUN poetry install --no-interaction --no-ansi --without dev --no-root

EXPOSE 8000
# CMD poetry run uvicorn --host 0.0.0.0 fast_api.app:app
ENTRYPOINT ["/entrypoint.sh"]