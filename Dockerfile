FROM python:2.7.8
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY ./requirements.txt /usr/src/app/
COPY . /usr/src/app
EXPOSE 80
CMD ["python","influxdb_test.py"]

