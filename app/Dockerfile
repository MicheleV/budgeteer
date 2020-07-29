FROM centos:8

MAINTAINER Michele Valsecchi
LABEL Vendor="CentOS8-python36"
LABEL Version=0.0.1

#RUN mkdir -p /app/
#WORKDIR /app/
WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# RUN dnf -y update
RUN dnf -y install python36
RUN alternatives --set python /usr/bin/python3
RUN update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1

COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY ./entrypoint.sh .
COPY . .

# EXPOSE 8000

# CMD ["python","manage.py","runserver", "0.0.0.0:8000"]