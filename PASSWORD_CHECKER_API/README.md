## **FAST API**

### **Step 1: Create Project Structure**
```bash
cd C:\Users\sbalam387\Documents
mkdir project1
cd project1
mkdir bin lib src
```

### **Step 2: Write Python file (password_checker.py)**
```python
from fastapi import FastAPI
from pydantic import BaseModel
import re

app = FastAPI()

class PasswordRequest(BaseModel):
    password: str

@app.post("/verify-password/")
def verify_password(data: PasswordRequest):
    password = data.password
    if len(password) < 8 or len(password) > 20:
        return {"status": "failed", "reason": "Password must be 8-20 characters."}
    if not re.search(r"[A-Z]", password):
        return {"status": "failed", "reason": "Password must contain at least one uppercase letter."}
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return {"status": "failed", "reason": "Password must contain at least one special character."}
    return {"status": "success", "message": "Password is valid."}

def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8081) 

if __name__ == "__main__":
    main()
```

### **Step 3: Create build.sh**
```bash
#!/bin/bash

echo "Cleaning old builds..."
rm -rf build dist
rm -f bin/password_checker

echo "Building FastAPI app into binary..."
pyinstaller --onefile src/password_checker.py --distpath bin --name password_checker

echo "Build complete! Binary saved in bin/password_checker"
```

### **Step 4: Launch build container**
```bash
docker run -it -v C:\Users\sbalam387\Documents\project1:/project rockylinux:9 bash
```
(Inside Container)
```bash
cd /project
dnf update -y
dnf install python3 python3-pip gcc make zip unzip -y
pip3 install pyinstaller fastapi uvicorn pydantic
chmod +x build.sh
./build.sh
Open browser and can test:http://localhost:8081/verify-password/

```

### **Step 5: Zip the binary file**

### **Step 6 : Create a fresh container**
```bash
docker run -it --name apitest -p 8082:8081 rockylinux:9 bash
```

### **Step 7 :Copy ZIP to Container**

```bash
docker cp C:\Users\sbalam387\Documents\project1\bin\password_checker.zip apitest:/root/
docker exec -it apitest bash
```

### **Step 8 : Inside the Container – Unzip and Run**
```bash
cd /root
dnf install unzip -y
unzip password_checker.zip
chmod +x password_checker
./password_checker
```


### **Step 9: Test**
Open browser and go to:
```
http://localhost:8082/verify-password/
```
