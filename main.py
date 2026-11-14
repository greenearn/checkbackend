import os
import requests
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="CheckNumber Reseller Middle-Agent API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CHECKNUMBER_API_KEY = os.getenv("CHECKNUMBER_API_KEY", "YOUR_CHECKNUMBER_API_KEY")
CHECKNUMBER_BASE_URL = "https://api.checknumber.ai"

@app.post("/api/submit-task")
async def submit_task(
    user_id: str = Form(...),
    task_type: str = Form(...),
    file: UploadFile = File(...)
):
    file_bytes = await file.read()
    headers = {"X-API-Key": CHECKNUMBER_API_KEY}
    files = {"file": (file.filename, file_bytes, "text/plain")}
    data = {"task_type": task_type}
    
    try:
        response = requests.post(f"{CHECKNUMBER_BASE_URL}/v1/tasks", headers=headers, files=files, data=data)
        res_json = response.json()
        
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail=res_json.get("message", "Error submitting to CheckNumber API"))
            
        return {"status": "success", "data": res_json}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def home():
    return {"message": "CheckNumber Middle-Agent Backend is Running!"}