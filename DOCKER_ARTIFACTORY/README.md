## Project Structure


DOCKER_ARTIFACTORY/
├── lib/
│   ├── __init__.py
│   ├── app.py          # App initialization (FastAPI instance)
│   ├── models.py       # Pydantic models for request/response
│   ├── routes.py       # API endpoints
│   └── validator.py    # Password validation logic
│
├── src/
│   └── main.py         # Entry point calling FastAPI app
│
├── Dockerfile          # Builds the container image
├── build.sh            # Builds a binary using PyInstaller
└── docker-compose.yml  # Defines how to build/run containerized app

````

---

##  How to Run

### 1. Build & Run Using Docker Compose

```bash
docker-compose up --build
````

* This builds the Docker image
* Runs `build.sh` to generate a binary using PyInstaller
* Executes the binary inside the container

App will be available at: [http://localhost:8089/verify-password](http://localhost:8089/verify-password)

---

### 2. Manual Docker Build & Run

```bash
docker build -t docker_artifactory-app .
docker run -p 8089:8081 docker_artifactory-app
```

---

##  Output Binary

After build, PyInstaller places the binary in:

```
bin/password_checker/password_checker
```
---

##  Rebuilding

If you make changes to source files, re-run:

```bash
docker-compose up --build
```
This ensures the image and binary are rebuilt.

---

