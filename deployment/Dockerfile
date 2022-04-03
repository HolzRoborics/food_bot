ARG PYTHON_VERSION
FROM python:${PYTHON_VERSION:-3.8}-slim-buster as prod

ENV POETRY_VERSION=1.1.13
RUN pip install "poetry==$POETRY_VERSION" "watchdog" && poetry config virtualenvs.create false

ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PIP_NO_CACHE_DIR=off
ENV PYTHONDONTWRITEBYTECODE=on
ENV PYTHONFAULTHANDLER=on
ENV PYTHONUNBUFFERED=on

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential nano telnet curl \
    && rm -rf /var/lib/apt/lists/*

# Dependencies
ARG RUN_LEVEL=production
ENV RUN_LEVEL=${RUN_LEVEL}
COPY pyproject.toml poetry.loc[k] /opt/app/
WORKDIR /opt/app
RUN poetry install $(if [ "${RUN_LEVEL}" = "production" ]; then echo "--no-dev"; fi ) --no-interaction --no-ansi -vvv

# Application
COPY python_project ./python_project

COPY deployment/pre_start.py ./
COPY deployment/run.sh ./
RUN chmod +x run.sh

CMD ["./run.sh"]


FROM prod as dev

# --- Development image ---

ARG USER_ID
ARG GROUP_ID

RUN addgroup --gid $GROUP_ID user
RUN adduser --disabled-password --gecos '' --uid $USER_ID --gid $GROUP_ID user
USER user

RUN poetry config virtualenvs.create false

RUN echo "export PATH=\$PATH:~/.local/bin" > /home/user/.bashrc

ENV PYTHONPATH=/opt/app/python_project

CMD ["watchmedo", "auto-restart", "--directory=./", "--pattern=*.py", "--", "python", "-m", "project"]
