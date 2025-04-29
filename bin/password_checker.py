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
