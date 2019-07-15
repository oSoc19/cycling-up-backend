FROM python:3.7

COPY . /backend
WORKDIR /backend

RUN pip install pipenv gunicorn

RUN pipenv install --system --deploy

# RUN chmod +x app.py

RUN python process_data/fetch_convert.py

# CMD ["python", "app.py"]
CMD ["gunicorn", "--workers=16", "--bind=0.0.0.0:5000", "--name=backend", "app:api"]
