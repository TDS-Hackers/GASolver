from fastapi import FastAPI, Query, Request, HTTPException, UploadFile, Form, File
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse, RedirectResponse
import uvicorn

from request_parser import extract_info

import os, datetime

from GA_registry import GARegistry

app = FastAPI()
# Mount the static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI! at " + str(datetime.datetime.now())}

@app.post("/api")
async def process_request(
        question: str = Form(...),
        file: Optional[UploadFile] = File(None)
    ):
    try:
        #data = question
        #print(data)
        use_case = extract_info(question)
        if use_case:
            return GARegistry[use_case["GA_No"]](question, use_case["parameters"])
            #return {"use_case": use_case}
        
        return {"error": "No use case found."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/api/parse")
async def process_request(
        question: str = Form(...),
        file: Optional[UploadFile] = File(None)
    ):
    try:
        return extract_info(question)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Serve the favicon.ico
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("static/favicon.ico")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)