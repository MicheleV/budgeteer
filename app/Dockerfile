###########
# BUILDER #
###########

FROM centos:8 as builder

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN dnf -y install python36 nc
RUN alternatives --set python /usr/bin/python3
RUN update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1

COPY ./requirements.txt .
RUN pip install wheel
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt

#########
# FINAL #
#########
FROM centos:8

MAINTAINER Michele Valsecchi
LABEL Vendor="budgeteer"
LABEL Version=0.0.1

RUN dnf -y module disable postgresql:10
RUN dnf -y module enable postgresql:12

RUN dnf -y install python36 nc postgresql
RUN alternatives --set python /usr/bin/python3
RUN update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1

RUN mkdir -p /home/app
RUN groupadd -r app && adduser -r app -g app

ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/static
WORKDIR $APP_HOME

COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install wheel & pip install --no-cache /wheels/*

COPY ./entrypoint.sh $APP_HOME
COPY . $APP_HOME


RUN chown -R app:app $APP_HOME
# Avoid permission issues on /static from nginx container
RUN chmod -R 755 $APP_HOME/static
# FIXME: We should have a shard uid:guid between containers instead of using 755
# example: https://github.com/rowdybeaver/sample-django-docker/blob/master/Dockerfile

USER app

ENTRYPOINT ["/home/app/web/entrypoint.sh"]