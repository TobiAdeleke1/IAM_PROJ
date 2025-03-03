FROM python:3.11-slim

WORKDIR /full-app

RUN pip install --upgrade pip

COPY requirements.txt /full-app

RUN pip install -r requirements.txt

COPY . /full-app

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "backend.wsgi:application"]