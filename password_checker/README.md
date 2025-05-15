##  Project Overview

This project contains:

* A **FastAPI** application under the `password_checker/` directory.
* A **Jenkinsfile** written in **Groovy** that defines all pipeline stages.
* A **Dockerfile** to build a Jenkins image with Python support.
* Jenkins produces a **ZIP artifact** with the final app executable.

---


---

##  Why Build a Custom Jenkins Image?

The **official Jenkins Docker image does not include Python** or pip by default. This project needs Python to install dependencies and run `pyinstaller`. So, we:

* Create a Dockerfile that extends Jenkins and adds Python, pip, and zip.
* This allows Jenkins to perform all Python-related tasks during the pipeline.

---

##  Dockerfile Explained

```dockerfile
FROM jenkins/jenkins:lts

USER root

RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv zip && \
    apt-get clean

USER jenkins
```

**Explanation:**

* `FROM jenkins/jenkins:lts`: Base Jenkins image.
* `apt-get install`: Installs Python3, pip, venv, and zip tool.
* `USER jenkins`: Ensures Jenkins runs with non-root user.

---

## Build and Run Jenkins Container

###  Build Jenkins with Python

```bash
docker build -t jenkins-python .
```

###  Run Jenkins Container

```bash
docker run -d \
  -p 8091:8080 \	# Jenkins UI (http://localhost:8091)
  -p 50000:50000 \	# Jenkins inbound agent port
  -p 8092:8081 \	# Expose FastAPI server on host (http://localhost:8092)
  --name jenkins-app \
  jenkins-python
```

---

##  Access Jenkins Admin Panel

```bash
docker exec -it jenkins-app cat /var/jenkins_home/secrets/initialAdminPassword
```

Use the password to log in at: [http://localhost:8091](http://localhost:8091)

---

##  Why Use `venv`?

`venv` creates a **virtual environment**, which is an isolated Python environment inside Jenkins. It ensures:

* Clean and isolated dependencies.
* No interference with system-level Python packages.
* Environment consistency across stages.

---

##  FastAPI App Overview

App is started in `main.py` using:

```python
uvicorn.run(app, host="0.0.0.0", port=8081)
```

So, when deployed inside Docker, and with port 8081 mapped to host port 8092:

* 📍 Access it via: [http://localhost:8092/verify-password](http://localhost:8092/verify-password)

---

## Jenkinsfile (Groovy Script)

```groovy
pipeline {
    agent any

    environment {
        VENV_PATH = "${WORKSPACE}/venv/bin"
        PATH = "${VENV_PATH}:${env.PATH}"
        DEST_PATH = "${WORKSPACE}/artifact_output"
    }

    stages {
        stage('Setup Virtualenv & Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install pyinstaller fastapi uvicorn pydantic
                '''
            }
        }

        stage('Build Package') {
            steps {
                sh '''
                    . venv/bin/activate
                    pyinstaller -y password_checker/main.py \
                        --distpath bin \
                        --name password_checker \
                        --paths password_checker/app
                '''
            }
        }

        stage('Zip Build') {
            steps {
                sh '''
                    mkdir -p ${DEST_PATH}
                    cd bin/password_checker
                    zip -r ${DEST_PATH}/password_checker.zip .
                '''
            }
        }

        stage('Archive') {
            steps {
                archiveArtifacts artifacts: 'artifact_output/password_checker.zip', allowEmptyArchive: false
            }
        }
    }
}
```

---

## 🔍 Jenkinsfile Explained for Beginners

| Stage                | What it Does                                                                    |
| -------------------- | ------------------------------------------------------------------------------- |
| **Setup Virtualenv** | Creates an isolated Python environment & installs FastAPI, PyInstaller, etc.    |
| **Build Package**    | Converts the app into a standalone binary using `pyinstaller`                   |
| **Zip Build**        | Compresses the generated binary and files into a `.zip` archive                 |
| **Archive**          | Jenkins stores the zip file as an artifact you can download from the Jenkins UI |

---

## Final Output

After the pipeline runs:

* A file named `password_checker.zip` will be saved in: `artifact_output/`
* Download it from Jenkins UI under "Build Artifacts"

---

##  Run the Final Zipped Output

```bash
unzip password_checker.zip
./password_checker
```

* This launches the FastAPI app on **port 8081**
* 📍 Access via: [http://localhost:8081/verify-password](http://localhost:8081/verify-password)

---


## ✅ Summary

* Jenkins + Docker CI/CD pipeline
* Custom Jenkins Docker image with Python tools
* FastAPI app converted to binary with PyInstaller
* Final zipped build archived and downloadable
* Clean explanation for beginners
