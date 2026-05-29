from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import pandas as pd

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LRNRequest(BaseModel):
    lrn: str

students = {}
REQUIRED_COLUMNS = ["studentNumber", "firstName", "lastName"]

@app.post("/upload_excel")
async def upload_excel(file: UploadFile = File(...)):
    global students
    try:
        df = pd.read_excel(file.file)

        for col in REQUIRED_COLUMNS:
            if col not in df.columns:
                return {"error": f"Missing required column: {col}"}

        students = {}

        for _, row in df.iterrows():
            lrn = str(row["studentNumber"])
            name = f"{row['firstName']} {row['lastName']}"

            subjects = {}
            for col in df.columns:
                if col not in REQUIRED_COLUMNS:
                    subjects[col] = row[col]

            students[lrn] = {"name": name, "subjects": subjects}

        return {"message": "Uploaded", "total_students": len(students)}

    except:
        return {"error": "Invalid file"}

@app.post("/check_grade")
def check_grade(data: LRNRequest):
    if data.lrn in students:
        return students[data.lrn]
    return {"error": "LRN not found"}

@app.get("/download_sample")
def download_sample():
    file_name = "sample_students.xlsx"

    data = {
        "studentNumber": ["100001", "100002"],
        "firstName": ["Juan", "Maria"],
        "lastName": ["Dela Cruz", "Santos"],
        "Math": [90, 88],
        "English": [85, 91]
    }

    pd.DataFrame(data).to_excel(file_name, index=False)
    return FileResponse(file_name, filename=file_name)

@app.get("/")
def home():
    return FileResponse("system_index.html")