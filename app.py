from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import joblib
import numpy as np
from mangum import Mangum
import os

app = FastAPI(root_path="/default")

# --- PATH CONFIGURATION ---
# This calculates the exact location of the file inside the Docker container
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_PATH = os.path.join(BASE_DIR, "frontend", "index.html")
MODEL_PATH = os.path.join(BASE_DIR, "model", "linear_model.pkl")

# Load Model
if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
    model_loaded = True
else:
    model_loaded = False

class SalaryInput(BaseModel):
    years_experience: float

def predict_salary(years):
    if not model_loaded:
        return {"error": "Model file not found inside container"}
    features = np.array([[years]])
    prediction = model.predict(features)
    return round(prediction[0], 2)

# --- HELPER: Read HTML File Safely ---
def get_html_content():
    if not os.path.exists(FRONTEND_PATH):
        return f"<h1>Error: Could not find HTML file at {FRONTEND_PATH}</h1>"
    with open(FRONTEND_PATH, "r") as f:
        return f.read()

# --- ROUTES ---
@app.get("/{full_path:path}", response_class=HTMLResponse)
async def serve_ui(full_path: str):
    return HTMLResponse(content=get_html_content(), status_code=200)

@app.get("/", response_class=HTMLResponse)
async def serve_root_ui():
    return HTMLResponse(content=get_html_content(), status_code=200)

@app.post("/{full_path:path}")
async def catch_all_predict(request: Request, full_path: str):
    data = await request.json()
    years = data.get("years_experience")
    salary = predict_salary(years)
    return {"predicted_salary": salary}

handler = Mangum(app)