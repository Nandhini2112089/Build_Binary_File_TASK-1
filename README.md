---
---
This document shows how to:

- Build a **custom Jenkins Docker image** `jenkins-python-docker` with Python & Docker CLI
- Use Jenkins pipeline to build Docker image from a **pre-built binary folder**
- Push the image to **Docker Hub** (`sivanandhini23/password-checker`)
- Pull and run the image from Docker Hub on any system

---

##  Step 1: Create Custom Jenkins Image

### Why a custom Jenkins image?

The base Jenkins image lacks:

- Python
- Docker CLI

Hence, we create a custom Jenkins image with both tools pre-installed.

###  Dockerfile (`CustomJenkins.Dockerfile`)

```dockerfile
FROM jenkins/jenkins:lts

USER root

RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv zip curl gnupg lsb-release && \
    apt-get clean

RUN python3 -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install pyinstaller fastapi pydantic uvicorn

RUN curl -fsSL https://download.docker.com/linux/debian/gpg | \
    gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] \
    https://download.docker.com/linux/debian $(lsb_release -cs) stable" > /etc/apt/sources.list.d/docker.list && \
    apt-get update && \
    apt-get install -y docker-ce-cli

RUN groupadd docker && usermod -aG docker jenkins

USER jenkins
````

###  Build the Image

```bash
docker build -t jenkins-python-docker .
```

### ▶️ Run Jenkins Container

```bash
docker run -d \
  -p 8091:8080 \
  -p 50000:50000 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v jenkins_home:/var/jenkins_home \
  --name jenkins-app \
  jenkins-python-docker
```

### 🌐 Access Jenkins

* URL: [http://localhost:8091](http://localhost:8091)
* Get admin password:

```bash
docker exec -it jenkins-app cat /var/jenkins_home/secrets/initialAdminPassword
```

---

## Step 2: Dockerfile for Pre-Built Binary

We already have a pre built binary folder `password_checker`.

###  Dockerfile (`Dockerfile-app`)

```dockerfile
FROM python:3.11

WORKDIR /app

COPY binary/password_checker /app/password_checker

EXPOSE 8081

RUN chmod +x /app/password_checker/password_checker

ENTRYPOINT ["/app/password_checker/password_checker"]
```

---

## Step 3: Jenkins Pipeline - Build & Push Docker Image

###  `Jenkinsfile`

```groovy
pipeline {
    agent any

    environment {
        DOCKERHUB_USER = 'sivanandhini23'
        IMAGE_NAME = "${DOCKERHUB_USER}/password-checker"
    }

    stages {
        stage('Check Docker Access') {
            steps {
                sh 'docker --version'
                sh 'docker ps'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME .'
            }
        }

        stage('Login to Docker Hub') {
            steps {
                sh 'docker login -u $DOCKERHUB_USER -p <dokcer-hub password>'
            }
        }

        stage('Push Docker Image') {
            steps {
                sh 'docker push $IMAGE_NAME'
            }
        }
    }
}
```
---

## Step 4: Pull & Run Anywhere

Once pushed, pull and run it anywhere:

```bash
docker pull sivanandhini23/password-checker
docker run -d -p 8092:8081 sivanandhini23/password-checker
```

### App URL

[http://localhost:8092/verify-password/](http://localhost:8092/verify-password/)

---
