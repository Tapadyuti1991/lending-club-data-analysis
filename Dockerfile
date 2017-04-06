#FROM khozzy/selenium-python-chrome

#WORKDIR /src

#COPY . /

#RUN pip install bs4 pandas  


#CMD ["python", "/src/Autologin.py"]





FROM python:latest

MAINTAINER  Pranjal_Jain

ARG user=app
ARG group=app
ARG uid=2101
ARG gid=2101

# The luigi app is run with user `app`, uid = 2101
# If you bind mount a volume from the host or a data container,
# ensure you use the same uid
RUN groupadd -g ${gid} ${group} \
    && useradd -u ${uid} -g ${group} -m -s /bin/bash ${user}

RUN mkdir /etc/luigi
ADD ./etc/luigi/logging.cfg /etc/luigi/
ADD ./etc/luigi/client.cfg /etc/luigi/
VOLUME /etc/luigi

RUN mkdir -p /luigi/tasks
RUN mkdir -p /luigi/work
RUN mkdir -p /luigi/outputs
ADD ./Data /Data
ADD ./luigi/tasks/ /luigi/tasks

RUN chown -R ${user}:${group} /luigi

VOLUME /luigi/work
VOLUME /luigi/tasks
VOLUME /luigi/outputs

RUN apt-get update && apt-get install -y \
    libpq-dev \
    freetds-dev \
    build-essential



USER ${user}

RUN bash -c "pyvenv /luigi/.pyenv \
    && source /luigi/.pyenv/bin/activate \
    && pip install cython \
    && pip install sqlalchemy luigi pymssql psycopg2 alembic numpy pandas sklearn scipy"

ADD ./luigi/taskrunner.sh /luigi/

ENTRYPOINT ["bash", "/luigi/taskrunner.sh"]
