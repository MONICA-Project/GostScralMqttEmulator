FROM python:3.8

# Update base container install
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get -y update
RUN apt-get install -y dialog apt-utils
RUN apt-get upgrade -y

# Add unstable repo to allow us to access latest GDAL builds
RUN echo deb http://ftp.uk.debian.org/debian unstable main contrib non-free >> /etc/apt/sources.list
RUN apt-get update

# Existing binutils causes a dependency conflict, correct version will be installed when GDAL gets intalled
RUN apt-get remove -y binutils

# Install GDAL dependencies
RUN apt-get -t unstable install -y libgdal-dev g++

# Update C env vars so compiler can find gdal
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

# This will install GDAL 2.2.4
#RUN pip install GDAL==2.2.4

# Install dependencies
# Update base container install
#RUN apt-get update
#RUN apt-get upgrade -y

# create a folder and set is as working directory
RUN mkdir /code/
WORKDIR /code/

# add requirements.txt to the image
ADD images/web/requirements.txt /code/

# install python depends
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# create unprivileged user
RUN adduser --disabled-password --gecos '' myuser