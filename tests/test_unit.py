import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../backend'))
os.chdir(os.path.join(os.path.dirname(__file__), '../backend'))
from app import app
from fastapi.testclient import TestClient

client = TestClient(app)

# Unit Test 1: Home endpoint returns correct status
def test_home_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "running"

# Unit Test 2: Health endpoint is healthy
def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

# Unit Test 3: Prediction returns correct structure
def test_prediction_structure():
    grades = {f"M110{i}": 70 for i in range(7)}
    grades.update({f"I110{i}": 70 for i in range(2)})
    # Add all 30 required courses with grade 70
    all_courses = ['M1100', 'M1101', 'M1102', 'PHYS100', 'PHYS101', 'I1100', 
                   'P1101', 'S1101', 'P1100', 'M1103', 'M1104', 'M1105', 
                   'M1106', 'M1107', 'I1101', 'I2202', 'I2204', 'I2205', 
                   'M2251', 'M2250', 'I2201', 'I2203', 'S2250', 'I2206', 
                   'I2207', 'I2208', 'I2209', 'I2210', 'I2211', 'I2234']
    grades = {course: 70.0 for course in all_courses}
    
    response = client.post("/predict", json={"grades": grades})
    assert response.status_code == 200
    data = response.json()
    assert "predictions" in data
    assert "average" in data
    assert "pass_rate" in data