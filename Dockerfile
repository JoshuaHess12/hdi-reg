FROM superelastix/elastix:5.0.1 AS elastix

COPY . /app/

RUN apt update && apt -y upgrade
RUN apt install python3.8 -y
RUN apt-get update && apt-get install -y python3-pip
RUN ln -s /usr/bin/pip3 /usr/bin/pip
RUN ln -s /usr/bin/python3.8 /usr/bin/python

RUN pip3 install numpy pandas nibabel opencv-python PyYAML