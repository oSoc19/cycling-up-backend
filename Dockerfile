FROM python:3.7

COPY . /backend
WORKDIR /backend

RUN pip install pipenv

RUN pipenv install --system --deploy

RUN chmod +x app.py

CMD ["python", "app.py"]