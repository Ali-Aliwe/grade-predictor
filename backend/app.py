from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import numpy as np
import pandas as pd
from typing import Dict

app = FastAPI(title="Grade Predictor API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model
model = joblib.load('model/best_xgboost_model.pkl')
input_courses = joblib.load('model/feature_columns.pkl')
output_courses = joblib.load('model/target_columns.pkl')

class GradeInput(BaseModel):
    grades: Dict[str, float]

class PredictionResponse(BaseModel):
    predictions: Dict[str, float]
    average: float
    pass_rate: float

@app.get("/")
def home():
    return {"status": "running", "model": "XGBoost Grade Predictor"}

@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/predict", response_model=PredictionResponse)
def predict(data: GradeInput):
    try:
        print("\n" + "="*70)
        print("PREDICTION REQUEST RECEIVED")
        print("="*70)
        
        grades_dict = data.grades
        print(f"\n1. Received grades dictionary:")
        print(f"   Total courses received: {len(grades_dict)}")
        print(f"   Courses: {list(grades_dict.keys())}")
        
        print(f"\n2. Expected input courses (from model):")
        print(f"   Total expected: {len(input_courses)}")
        print(f"   Courses: {input_courses}")
        
        # Create a list with grades in the exact order of input_courses
        grades_list = []
        missing_courses = []
        for course in input_courses:
            if course in grades_dict:
                grades_list.append(grades_dict[course])
            else:
                grades_list.append(70)  # Default value for missing courses
                missing_courses.append(course)
        
        if missing_courses:
            print(f"\n3. Missing courses (filled with 70): {missing_courses}")
        else:
            print(f"\n3. All courses provided ✓")
        
        print(f"\n4. Creating DataFrame:")
        print(f"   Shape: (1, {len(grades_list)})")
        
        # Create DataFrame with proper structure
        student_input = pd.DataFrame([grades_list], columns=input_courses)
        
        print(f"   DataFrame columns: {list(student_input.columns)}")
        print(f"   DataFrame shape: {student_input.shape}")
        print(f"\n5. Sample values:")
        print(student_input.head())
        
        print(f"\n6. Making prediction...")
        # Predict
        # Replace line 86:
        prediction = model.predict(student_input.values)[0]        
        print(f"   Prediction successful ✓")
        print(f"   Number of predictions: {len(prediction)}")
        
        # Format response
        results = {course: float(pred) for course, pred in zip(output_courses, prediction)}
        avg = float(np.mean(prediction))
        pass_rate = float((prediction >= 50).sum() / len(prediction) * 100)
        
        print(f"\n7. Results:")
        print(f"   Average grade: {avg:.1f}")
        print(f"   Pass rate: {pass_rate:.0f}%")
        print(f"   Output courses: {len(results)}")
        
        print("\n" + "="*70)
        print("PREDICTION COMPLETED SUCCESSFULLY")
        print("="*70 + "\n")
        
        return {
            "predictions": results,
            "average": avg,
            "pass_rate": pass_rate
        }
    except Exception as e:
        print("\n" + "="*70)
        print("ERROR OCCURRED")
        print("="*70)
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        import traceback
        print("\nFull traceback:")
        traceback.print_exc()
        print("="*70 + "\n")
        raise HTTPException(status_code=400, detail=str(e))
    
if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
