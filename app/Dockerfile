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

COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY ./entrypoint.sh .
COPY . .

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
