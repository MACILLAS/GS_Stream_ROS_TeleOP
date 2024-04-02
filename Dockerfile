FROM ros:noetic-ros-core
LABEL maintaner="Joaquin Gimenez <jg@joaquingimenez.com>"

LABEL org.opencontainers.image.title: "noetic-rosbridge"
LABEL org.opencontainers.image.description: "Docker image with ros:noetic-ros-core and ros-bridge-suite running rosbridge server on launch"
LABEL org.opencontainers.image.url: "https://hub.docker.com/repository/docker/joaquingimenez1/noetic-rosbridge"
LABEL org.opencontainers.image.source: "https://github.com/JoaquinGimenez1/docker-noetic-rosbridge"
LABEL org.opencontainers.image.version: "1.1.4"

WORKDIR /

RUN sudo apt update && apt install -y ros-noetic-rosbridge-suite
RUN sudo apt-get update
RUN sudo apt-get install -y python3
RUN sudo apt-get install -y pip
RUN pip install roslibpy
RUN pip install "python-socketio[client]"
RUN pip install numpy

COPY init-rosbridge.sh .
COPY app.py .
COPY debug_listener.py .

RUN chmod +x init-rosbridge.sh



CMD ["/init-rosbridge.sh"]