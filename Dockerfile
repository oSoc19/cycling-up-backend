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
RUN echo "0 3 1-7 * 1 root python /backend/process_data/fetch_convert.py >> /var/log/api_fetch.out 2>/var/log/api_fetch.err" \
        >> /etc/crontab

RUN python process_data/fetch_convert.py

# CMD ["python", "app.py"]
CMD ["gunicorn", "--workers=6", "--bind=0.0.0.0:5000", " --log-level=warning", "--name=backend", "app:api"]
