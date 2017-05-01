FROM python:3.6

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.* /usr/src/app/
RUN pip install --no-cache-dir -r requirements.dev.txt

ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh /
RUN chmod +xr /wait-for-it.sh
