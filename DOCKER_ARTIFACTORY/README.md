## Project Structure

```
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
└── build.sh            # Builds a binary using PyInstaller

````

---

##  How to Run

### 1. Build & Run Using Docker Compose

```bash
docker build -t <image_name> .
docker run -it -p 8089:8081 <image_name>
````

* This builds the Docker image
* Runs `build.sh` to generate a binary using PyInstaller
* Executes the binary inside the container

App will be available at: [http://localhost:8089/verify-password](http://localhost:8089/verify-password)

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
docker build -t <image_name> .
```
This ensures the image and binary are rebuilt.

---

