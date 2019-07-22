FROM python:3.7

ENV TZ="Europe/Brussels"

COPY . /backend
WORKDIR /backend

RUN apt-get update \
    && apt-get install -y cron \
    && apt-get autoremove -y

RUN pip install pipenv gunicorn

RUN pipenv install --system --deploy

# Set a cron to fetch job on each first Monday of month, at 3 a.m.
RUN echo "0 3 1-7 * 1 root python process/__init__.py  >> /var/log/api_process.out 2>/var/log/api_process.err" \
    >> /etc/crontab

RUN python process/__init__.py

# CMD ["python", "app.py"]
# CMD ["gunicorn", "--workers=6", "--bind=0.0.0.0:5000", "--name=backend", "'app:configure_api()'"]
CMD gunicorn --workers=6 --bind=0.0.0.0:5000 --name=backend 'app:configure_api()'
