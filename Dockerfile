FROM selenium/standalone-firefox
USER root
ADD ./* /src/

RUN apt update && apt update -y && apt install -y python3 python3-pip
RUN python3 -m pip install -r /src/requirements.txt
