FROM library/python:3.10-alpine

EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# RUN apk update && apk add bind-tools curl

RUN apk --no-cache add coreutils

# Install requirements and libraries.
#   --no-cache allows users to install packages with an index that is updated and used on-the-fly and not cached locally
RUN apk --no-cache --quiet add gcc make g++ bash git openssh \
    postgresql-dev curl build-base libffi-dev python3-dev py-pip \
    jpeg-dev zlib-dev libsass-dev

# https://gist.github.com/deliro/509b663093ff0f49c1b71e1876597ccb
RUN apk add --update --no-cache --virtual .build-deps \
    libxml2 \
    libxml2-dev && \
    apk add libxslt-dev && \
    apk del .build-deps

RUN apk add --no-cache tzdata
ENV TZ=America/Lima

# RUN mkdir /app
WORKDIR /app
COPY . ./app/

# Install pip requirements
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
# RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
# USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "project.wsgi"]
