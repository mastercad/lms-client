FROM ubuntu

ENV DEBIAN_FRONTEND noninteractive
ENV TERM linux
ENV DISPLAY :0

RUN apt update && \
  apt install -y \
#  rpi-update rpi-update \
  pyflakes \
  pylint \
  python \
  python3 \
  python3-all \
  python3-all-dev \
  python3-dev \
  python3-pip \
  python3-setuptools \
  python-all \
  python-all-dev \
  python-dev \
  python-pip \
  python-setuptools \
  alsa-utils

RUN python -m pip install pylms mfrc522 python-vlc simple_queue configparser psutil

RUN echo "dtparam=spi=on" | tee -a "/boot/config.txt" >> /dev/null && \
  echo "device_tree_param=spi=on" | tee -a "/boot/config.txt" >> /dev/null && \
  echo "dtoverlay=hifiberry-dac" | tee -a "/boot/config.txt" >> /dev/null

COPY config/asound.conf /etc/asound.conf
