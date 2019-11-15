FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/
WORKDIR /code
# to use queue with the server uncomment this
# ADD prestart.sh /code/prestart.sh
# RUN prestart.sh
