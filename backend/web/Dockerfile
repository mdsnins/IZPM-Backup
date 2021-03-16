FROM ubuntu:20.04

RUN apt update
RUN apt -y install ca-certificates python3 tar
RUN apt -y install python3-pip
RUN pip3 install redis flask requests

RUN mkdir /app/
ADD *.py /app/
ADD page /app/page

ENTRYPOINT ["python3", "/app/index.py"]
