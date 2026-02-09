import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../backend'))
os.chdir(os.path.join(os.path.dirname(__file__), '../backend'))
from app import app
from fastapi.testclient import TestClient

client = TestClient(app)

# Integration Test 1: Full prediction flow with valid data
def test_full_prediction_flow():
    all_courses = ['M1100', 'M1101', 'M1102', 'PHYS100', 'PHYS101', 'I1100', 
                   'P1101', 'S1101', 'P1100', 'M1103', 'M1104', 'M1105', 
                   'M1106', 'M1107', 'I1101', 'I2202', 'I2204', 'I2205', 
                   'M2251', 'M2250', 'I2201', 'I2203', 'S2250', 'I2206', 
                   'I2207', 'I2208', 'I2209', 'I2210', 'I2211', 'I2234']
    grades = {course: 85.0 for course in all_courses}
    
    response = client.post("/predict", json={"grades": grades})
    assert response.status_code == 200
    data = response.json()
    assert data["average"] > 0
    assert data["pass_rate"] >= 0

# Integration Test 2: Prediction with low grades
def test_prediction_low_grades():
    all_courses = ['M1100', 'M1101', 'M1102', 'PHYS100', 'PHYS101', 'I1100', 
                   'P1101', 'S1101', 'P1100', 'M1103', 'M1104', 'M1105', 
                   'M1106', 'M1107', 'I1101', 'I2202', 'I2204', 'I2205', 
                   'M2251', 'M2250', 'I2201', 'I2203', 'S2250', 'I2206', 
                   'I2207', 'I2208', 'I2209', 'I2210', 'I2211', 'I2234']
    grades = {course: 45.0 for course in all_courses}
    
    response = client.post("/predict", json={"grades": grades})
    assert response.status_code == 200

# Integration Test 3: Empty grades gets filled with defaults (200 OK)
def test_empty_grades_uses_defaults():
    response = client.post("/predict", json={"grades": {}})
    assert response.status_code == 200  # Should succeed with default values
    data = response.json()
    assert data["average"] > 0