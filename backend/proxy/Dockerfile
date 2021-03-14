FROM ubuntu:20.04

RUN apt update
RUN apt -y install ca-certificates python3 libssl-dev
RUN apt -y install python3-pip
RUN pip3 install mitmproxy redis

RUN mkdir /app/
ADD service.py /app/
ADD *.sh /tmp/ 
RUN chmod +x /tmp/*.sh

ENTRYPOINT ["/bin/sh", "/tmp/proxy_run.sh"]
