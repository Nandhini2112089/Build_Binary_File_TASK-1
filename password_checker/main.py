import uvicorn
from app.core import app 

if __name__ == "__main__":
    uvicorn.run("app.core:app", host="0.0.0.0", port=8081, reload=True)
