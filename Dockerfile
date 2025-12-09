FROM python:3.12.2

ARG ENTRYPOINT_NAME
ENV ENTRYPOINT_NAME ${ENTRYPOINT_NAME}

ENV PYTHONUNBURRERED 1

RUN mkdir /apps/
WORKDIR /apps/


RUN pip install pip==24.2
RUN pip install --no-cache-dir poetry==1.8.4

COPY poetry.lock /apps/poetry.lock
COPY pyproject.toml /apps/pyproject.toml

RUN poetry export --without-hashes -f requirements.txt --output requirements.txt

RUN pip install -r requirements.txt

COPY ./. /apps/
COPY ./.env /apps/.env

RUN echo "Container name is ${ENTRYPOINT_NAME}"

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]