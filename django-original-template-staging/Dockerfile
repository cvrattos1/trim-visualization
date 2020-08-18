FROM python:3.6
RUN DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install nano
RUN apt-get update && apt-get install curl

RUN  apt-get update && apt-get --assume-yes install gfortran

WORKDIR /usr/src/app/

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
