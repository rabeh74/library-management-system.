FROM python:3.9-alpine3.13
LABEL maintainer="rabehrabie"
# to make output from python directly to console
ENV PYTHONUNBUFFERED 1
# to copy reqs from local machine to container
COPY ./requirements.txt /tmp/requirements.txt
COPY /requirements.dev.txt /tmp/requirements.dev.txt
# to copy code from local machine to container
COPY ./app /app
# where we run commands to docker and where django project is located
# when running command in django i didnot need o write full path
WORKDIR /app
# to exxpose 800 from conatiner to our local machine
EXPOSE 8000
ARG DEV=false
# env to provide any conflict between my project dependencies and image
RUN python3 -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client jpeg-dev &&\
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev zlib zlib-dev &&\
    /py/bin/pip install -r /tmp/requirements.txt && \
    # to install this package just in devlopment stage 
    if [ $DEV = "true" ];then /py/bin/pip install -r /tmp/requirements.dev.txt;fi && \
    rm -rf /tmp && \
    apk del .tmp-build-deps &&\
    # to prevent using root user
    adduser \
        --disabled-password \
        --no-create-home \
        django-user &&\
    mkdir -p /vol/web/media && \
    mkdir -p /vol/web/static &&\
    chown -R django-user:django-user /vol &&\
    chmod -R 755 /vol
# when run any command we need not specify the full path
ENV PATH="/py/bin:$PATH"
USER django-user