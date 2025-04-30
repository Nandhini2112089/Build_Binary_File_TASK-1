
```markdown
# How I Built My FastAPI App into a Binary and Used It in Another Container

This document explains **how I built my FastAPI application into a binary** file using PyInstaller, and how that binary is used to run the application in a completely different container **without needing Python, pip, or the source code**.

---

## What Is a Binary File?

A binary file in this context is an **executable** that contains:
- The **Python interpreter**
- All **required libraries**
- My own **Python source code**

This means I can run the app anywhere, even inside containers that **don’t have Python installed**, as long as I copy this binary along with its internal files.

---

##  Why I Built a Binary

I converted my FastAPI project into a binary for the following reasons:

- **Portability** – Works on any container, even without Python
- **No source code needed** – I can hide the original `.py` files
- **No dependency installation** – FastAPI, Pydantic, etc., are included in the binary
- **Clean runtime** – The destination container stays lightweight and neat
- **Faster startup** – No time wasted on pip installs or environment setup

---

##  Build Steps

###  Shell Script to Build the Binary

I created a `build.sh` file to automate the binary generation using PyInstaller:

```bash
#!/bin/bash

echo "Cleaning old builds..."
rm -rf build dist
rm -f bin/password_checker

echo "Building FastAPI app into binary..."
pyinstaller src/main.py --distpath bin --name password_checker --paths=lib

echo "Build complete! Binary saved in bin/password_checker"
```

### Project Structure Before Building

```
project1/
├── lib/
│   ├── __init__.py
│   ├── app.py
│   ├── routes.py
│   ├── models.py
│   └── validator.py
│
├── src/
│   └── main.py
│
├── build.sh
```

---

## What Happens During the Build

When I run:

```bash
./build.sh
```

PyInstaller does the following:

- Packs everything (Python + all imports) into a folder named `password_checker` under `bin/`
- Detects and includes modules from `lib/` using `--paths=lib`
- Embeds a Python interpreter
- Bundles all my `.py` files, third-party libraries, and dependencies

###  Output Structure After Build

```
bin/
└── password_checker/
    ├── password_checker     ← Executable binary (small stub)
    └── _internal/           ← All runtime files, Python interpreter, app code
```



---

##  How the Binary Works

To run the app:

```bash
cd bin/password_checker
./password_checker
```

Behind the scenes:

- The binary runs a **bootloader**
- It uses the bundled Python interpreter to execute the FastAPI code
- **Uvicorn starts** the FastAPI server

### Output Example

```
INFO:     Started server process [PID]
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8081
```

---

##  Running in Another Container

To run the app in another Docker container (or host):

1. Copy the entire `bin/password_checker/` folder to the container
2. Inside the container, execute:

```bash
cd password_checker
./password_checker
```


###  What’s Special:

- No need to install Python or pip
- No FastAPI or Uvicorn setup
- No `.py` files needed
- Just one folder contains everything to run the app

---

##  Why the Binary Size Reduced

Initially, I kept the whole code in one file and used `--onefile`, which produced a large binary (~11MB). Later, when I structured the app into multiple files and **didn’t use `--onefile`**, PyInstaller created a small launcher binary (~4 KB) and an internal folder containing all other files.

---
