from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from ai_modules.gastric.model_inference import gastric_model_instance
import json

router = APIRouter()

@router.post("/analyze")
async def analyze_gastric(
    symptoms: str = Form(...), # JSON string containing symptom triggers
    student_prescription: str = Form(None), # Optional medical student prescription
    image: UploadFile = File(...)
):
    try:
        # 1. Parse symptoms
        symptoms_data = json.loads(symptoms)

        # 2. Process image with EfficientNet-B4
        image_bytes = await image.read()
        ai_result = gastric_model_instance.predict(image_bytes)

        # 3. Validation Logic (Step 7)
        # Compare student_prescription vs ai_result
        validation_feedback = "N/A"
        if student_prescription:
            # Add your NLP/Keyword comparison logic here later
            student_rx = json.loads(student_prescription)
            if ai_result["prediction"] == "Inflammation" and "omeprazole" in str(student_rx).lower():
                validation_feedback = "Correct treatment plan for inflammation."
            else:
                validation_feedback = "Consider proton pump inhibitors for confirmed inflammation."

        return {
            "status": "success",
            "symptom_data": symptoms_data,
            "ai_diagnosis": {
                "condition": ai_result["prediction"],
                "confidence": ai_result["confidence"],
                "severity": ai_result["severity"],
                "gradcam_image": ai_result["gradcam_base64"] # <--- Added this line
            },
            "educational_feedback": validation_feedback
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))