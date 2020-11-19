FROM ubuntu:20.04

RUN apt-get update
RUN apt-get install -y python3 python3-pip

COPY ./ ./code
WORKDIR ./code

RUN pip3 install -r requirements.txt

ENTRYPOINT python3 processing_unit.py