FROM python:3
MAINTAINER "Janik Luechinger janik.luechinger@uzh.ch"

COPY . /pga
WORKDIR /pga

RUN apt-get -y update && apt-get -y upgrade
RUN pip install -U pip && pip install -r requirements.txt

ENTRYPOINT [ "python", "-m", "initializer" ]

# Manual image building
# docker build -t pga-cloud-initializer .
# docker tag pga-cloud-initializer jluech/pga-cloud-initializer
# docker push jluech/pga-cloud-initializer
