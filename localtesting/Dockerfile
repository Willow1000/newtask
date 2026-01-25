FROM ubuntu:latest
ARG DEBIAN_FRONTEND=noninteractive
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y build-essential
RUN apt-get install -y -f
RUN apt-get install -y apt-utils

RUN apt-get install -y wget
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN apt-get install -y git

RUN apt-get install -y xserver-xephyr
RUN apt-get install -y iputils-ping
RUN apt-get install -y python3-tk python3-dev
RUN apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6
RUN apt-get install -y gnome-screenshot
RUN apt-get install -y nano

RUN apt-get update -y

RUN apt install -y python3.12-venv
RUN python3 -m venv /code/venv_inside_docker

RUN apt-get install -y python3-pip
RUN /code/venv_inside_docker/bin/pip install --upgrade pip setuptools wheel
RUN /code/venv_inside_docker/bin/pip install python-xlib easyprocess pyvirtualdisplay pyautogui keyboard mouse opencv-python numpy pillow pynput
RUN /code/venv_inside_docker/bin/pip install discord
RUN /code/venv_inside_docker/bin/pip install fire

ENV VIRTUAL_ENV=/usr/src/app/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /workspace

# install java
RUN cd /opt/; wget https://github.com/AdoptOpenJDK/openjdk11-binaries/releases/download/jdk-11.0.6%2B10/OpenJDK11U-jdk_x64_linux_hotspot_11.0.6_10.tar.gz && \
      tar -xvzf OpenJDK11U-jdk_x64_linux_hotspot_11.0.6_10.tar.gz && \
      rm OpenJDK11U-jdk_x64_linux_hotspot_11.0.6_10.tar.gz; cd -
  
RUN apt-get install -y zip
 

# SHELL ["/bin/bash", "-c"]
# CMD /bin/bash -i "/opt/code/LocallyAvailableActionTooling/start_container.sh"

