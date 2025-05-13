FROM jenkins/jenkins:lts

USER root


RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv && \
    apt-get clean


RUN python3 -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install pyinstaller fastapi uvicorn pydantic

ENV PATH="/opt/venv/bin:$PATH"

USER jenkins
