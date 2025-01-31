FROM python:3.8-alpine
COPY  . /application
WORKDIR /application
RUN pip install -r requirements.txt
CMD python application.py