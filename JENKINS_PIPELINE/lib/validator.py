import re

def validate_password(password: str):
    if len(password) < 8 or len(password) > 20:
        return {"status": "failed", "reason": "Password must be 8-20 characters."}
    if not re.search(r"[A-Z]", password):
        return {"status": "failed", "reason": "Must contain at least one uppercase letter."}
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return {"status": "failed", "reason": "Must contain at least one special character."}
    return {"status": "success", "message": "Password is valid."}
