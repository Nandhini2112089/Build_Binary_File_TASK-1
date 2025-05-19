---
This document shows how to:

* Build a **custom Jenkins Docker image** named `jenkins-python-docker` that includes Python and Docker CLI.
* Use Jenkins pipelines to build a **Docker image from a pre-built binary folder**.
* Push the built Docker image to **Docker Hub** under the name `sivanandhini23/password-checker`.
* Pull and run the Docker image from Docker Hub on any machine.

---

# Step 1: Build the Custom Jenkins Image (`jenkins-python-docker`)

### Why build a custom Jenkins image?

The official Jenkins image **does not come with Python or Docker CLI installed**, which are required to:

* Run Python-based builds inside Jenkins (if needed).
* Use Docker commands inside Jenkins pipelines to build and push Docker images.

### Dockerfile (`CustomJenkins.Dockerfile`)

```dockerfile
FROM jenkins/jenkins:lts

USER root

# Update OS and install Python3, pip, venv, zip, curl, gnupg, and lsb-release
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv zip curl gnupg lsb-release && \
    apt-get clean

# Create Python virtual environment and install essential Python packages
RUN python3 -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install pyinstaller fastapi pydantic uvicorn

# Add Docker repository keys and install Docker CLI
RUN curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" > /etc/apt/sources.list.d/docker.list && \
    apt-get update && \
    apt-get install -y docker-ce-cli

# Create Docker group and add Jenkins user to it so Jenkins can run Docker commands
RUN groupadd docker && usermod -aG docker jenkins

USER jenkins
```

---

### Build the Jenkins Image

From the directory containing `CustomJenkins.Dockerfile`:

```bash
docker build -t jenkins-python-docker .
```

---

### Run the Jenkins Container

Run the container with Docker socket mounted (required for Jenkins to use Docker on host):

```bash
docker run -d \
  -p 8091:8080 \       # Jenkins UI port
  -p 50000:50000 \     # Jenkins agent port
  -v /var/run/docker.sock:/var/run/docker.sock \  # Allow Docker commands inside Jenkins
  -v jenkins_home:/var/jenkins_home \             # Persistent Jenkins data
  --name jenkins-app \
  jenkins-python-docker
```

---

### Access Jenkins UI

* Open browser and go to: [http://localhost:8091](http://localhost:8091)
* Get initial admin password:

```bash
docker exec -it myjenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

* Use this password to unlock Jenkins and install recommended plugins.
* Create admin user when prompted.

---

# Step 2: Prepare Dockerfile for Binary Image

Already have a pre-built binary folder: `password_checker`

### Dockerfile (`Dockerfile-app`)

```dockerfile
FROM python:3.11

WORKDIR /app

# Copy your binary folder into container
COPY binary/password_checker /app/password_checker

# Expose port your app listens on
EXPOSE 8081

# Make binary executable
RUN chmod +x /app/password_checker/password_checker

# Run the binary when container starts
ENTRYPOINT ["/app/password_checker/password_checker"]
```

---

# Step 3: Jenkins Pipeline to Build and Push Docker Image

The `Jenkinsfile` for building and pushing the docker image.

```groovy
pipeline {
    agent any

   environment {
    DOCKERHUB_USER = "sivanandhini23"
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
        sh 'docker login -u sivanandhini23 -p Nandhini@23'
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

# Step 4: Manual Docker Pull & Run (Outside Jenkins)

Once pipeline pushes the image to Docker Hub, we can pull and run it anywhere with Docker:

```bash
docker pull sivanandhini23/password-checker
docker run -d -p 8092:8081 sivanandhini23/password-checker
```

* App will be available at: [http://localhost:8092/verify-password/](http://localhost:8092/verify-password)

---


