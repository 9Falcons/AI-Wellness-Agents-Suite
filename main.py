import base64
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import agents

app = FastAPI(title="Standalone AI Agents API", version="1.0.0")


class CosmeticRequest(BaseModel):
    product_data: Dict[str, Any]


class SkinRequest(BaseModel):
    user_description: str
    image_base64: str


class WorkoutRequest(BaseModel):
    user_profile: Dict[str, Any]
    preferences: Dict[str, Any]


class MealRequest(BaseModel):
    context: Dict[str, Any]


@app.get("/")
def read_root():
    return {"message": "Welcome to the Standalone AI Agents API"}


@app.post("/analyze-cosmetic")
def analyze_cosmetic(request: CosmeticRequest):
    try:
        result = agents.analyze_cosmetic_product(request.product_data)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/analyze-skin")
def analyze_skin_endpoint(request: SkinRequest):
    try:
        result = agents.analyze_skin(request.image_base64, request.user_description)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/analyze-skin-upload")
async def analyze_skin_upload(
    user_description: str = Form(...),
    file: UploadFile = File(...)
):
    try:
        content = await file.read()
        image_base64 = base64.b64encode(content).decode('utf-8')
        result = agents.analyze_skin(image_base64, user_description)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate-workout")
def generate_workout(request: WorkoutRequest):
    try:
        result = agents.generate_workout_plan(request.user_profile, request.preferences)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate-meal")
def generate_meal(request: MealRequest):
    try:
        result = agents.generate_meal_plan(request.context)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
