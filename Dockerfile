FROM python:3.10

ENV PYTHONPATH "${PYTHONPATH}:/"
ENV PORT=8000
ENV DOCKER_BUILDKIT=0
ENV COMPOSE_DOCKER_CLI_BUILD=0

RUN pip install --upgrade pip
RUN pip install "poetry==1.4.2"

WORKDIR /app

COPY ./app /app
COPY poetry.lock pyproject.toml /app/
COPY ./main.py /app

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--lifespan=on", "--use-colors", "--reload" ]
