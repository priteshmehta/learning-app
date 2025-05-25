# to run backend server
import uvicorn
import  os
import sys

sys.path.append(os.getenv("PWD"))

if __name__ == "__main__":     
    uvicorn.run("src.main:app", host="127.0.0.1", port=8000, reload=True)
