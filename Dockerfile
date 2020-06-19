#FROM python:3.7.7-slim-buster
FROM web_app_base:latest

ADD . /WebApp
WORKDIR /WebApp

#RUN pip install --no-cache-dir --upgrade pip
#RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "app.py"]
