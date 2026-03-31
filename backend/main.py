from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np

app = FastAPI()

# allow frontend call
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

data_store = {}

@app.post("/upload")
async def upload(file: UploadFile):
    df = pd.read_csv(file.file)
    data_store["data"] = df
    return {"columns": list(df.columns)}

@app.get("/summary")
def summary():
    df = data_store.get("data")
    if df is None:
        return {"error": "No data uploaded"}
    return df.describe().to_dict()

@app.post("/ppk")
def ppk(usl: float, lsl: float, column: str):
    df = data_store.get("data")
    if df is None:
        return {"error": "No data uploaded"}

    data = df[column]

    mean = np.mean(data)
    std = np.std(data)

    cpu = (usl - mean) / (3 * std)
    cpl = (mean - lsl) / (3 * std)
    ppk = min(cpu, cpl)

    return {
        "mean": float(mean),
        "std": float(std),
        "Ppk": float(ppk)
    }
