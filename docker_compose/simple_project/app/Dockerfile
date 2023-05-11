FROM python:3.10

WORKDIR /opt/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV UWSGI_PROCESSES 1
ENV UWSGI_THREADS 16
ENV UWSGI_HARAKIRI 240
ENV DJANGO_SETTINGS_MODULE 'config.settings'

COPY run_uwsgi.sh /usr/local/bin/run_uwsgi.sh
COPY requirements.txt requirements.txt
COPY uwsgi/uwsgi.ini uwsgi.ini

RUN  mkdir -p /var/www/static/ \
     && mkdir -p /var/www/media/ \
     && mkdir -p /opt/app/static/ \
     && mkdir -p /opt/app/media/

RUN  pip install --upgrade pip \
     && pip install wheel --no-cache-dir \
     && pip install --upgrade setuptools \
     && pip install -r requirements.txt --no-cache-dir

COPY . .

#COPY $HOME/usr/local/lib/python3.10/site-packages/django/contrib/admin/static static

EXPOSE 8000

ENTRYPOINT ["bash", "run_uwsgi.sh"]
