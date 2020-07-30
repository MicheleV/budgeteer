FROM centos:8

MAINTAINER Michele Valsecchi
LABEL Vendor="CentOS8-python36"
LABEL Version=0.0.1

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN dnf -y install python36 nc
RUN alternatives --set python /usr/bin/python3
RUN update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1

RUN mkdir -p /home/app
RUN groupadd -r app && adduser -r app -g app

ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY ./entrypoint.sh $APP_HOME
COPY . $APP_HOME

# chown all the files to the app user
RUN chown -R app:app $APP_HOME

# change to the app user
USER app

ENTRYPOINT ["/home/app/web/entrypoint.sh"]