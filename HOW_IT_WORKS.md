# HOW_IT_WORKS.md

## How I Built My FastAPI App into a Binary and Used It in Another Container

This document explains **how** I built my FastAPI application into a binary.

---

### What Is a Binary File?

A binary file is an executable file that includes:
- Python interpreter
- All required libraries
- My own Python source code

This means I can run it **anywhere**, without needing to install Python or any packages.

---

### Why I Built a Binary

1. **Portability** – Works even in containers that don’t have Python installed  
2. **No need for source code** – Just copy the binary  
3. **No dependency installation** – FastAPI, Pydantic, etc. are already included  
4. **Clean runtime** – Target container stays lightweight  
5. **Faster startup** – No pip install or setup needed

---

### Build Steps

#### 1. Shell Script to Build the Binary

I created a `build.sh` script:
---

#### 2. Project Structure

```
project1/
│
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

### What Happens During Build

When I run:

```bash
./build.sh
```

PyInstaller:
- Packs everything into a `password_checker` binary under `bin/`
- Includes hidden imports (modules inside `lib`)
- Embeds a Python interpreter

Generated output:
```
bin/
└── password_checker/
    ├── password_checker  ← executable binary
    └── _internal/         ← runtime files
```

---

###  How the Binary Works

To run:

```bash
./bin/password_checker/password_checker
```

- Python runs inside the binary
- Uvicorn starts the FastAPI server
- API is live at `http://0.0.0.0:8081`

Output example:

```
INFO:     Started server process [PID]
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8081
```

---

###Running in Another Container

On the target container:
1. Copy `password_checker/password_checker`
2. Run it directly:
   ```bash
   ./password_checker
   ```

- No need to install Python  
- No source code required  
- Just one file runs the whole app

---

