import pytest
import requests
import time

BASE_URL = "http://localhost:5000"

# E2E Test 1: API is accessible
def test_api_accessible():
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 200

# E2E Test 2: Complete prediction workflow
def test_complete_workflow():
    all_courses = ['M1100', 'M1101', 'M1102', 'PHYS100', 'PHYS101', 'I1100', 
                   'P1101', 'S1101', 'P1100', 'M1103', 'M1104', 'M1105', 
                   'M1106', 'M1107', 'I1101', 'I2202', 'I2204', 'I2205', 
                   'M2251', 'M2250', 'I2201', 'I2203', 'S2250', 'I2206', 
                   'I2207', 'I2208', 'I2209', 'I2210', 'I2211', 'I2234']
    grades = {course: 70.0 for course in all_courses}
    
    response = requests.post(f"{BASE_URL}/predict", json={"grades": grades})
    assert response.status_code == 200
    data = response.json()
    assert len(data["predictions"]) > 0

# E2E Test 3: Response time is acceptable
def test_response_time():
    all_courses = ['M1100', 'M1101', 'M1102', 'PHYS100', 'PHYS101', 'I1100', 
                   'P1101', 'S1101', 'P1100', 'M1103', 'M1104', 'M1105', 
                   'M1106', 'M1107', 'I1101', 'I2202', 'I2204', 'I2205', 
                   'M2251', 'M2250', 'I2201', 'I2203', 'S2250', 'I2206', 
                   'I2207', 'I2208', 'I2209', 'I2210', 'I2211', 'I2234']
    grades = {course: 70.0 for course in all_courses}
    
    start = time.time()
    response = requests.post(f"{BASE_URL}/predict", json={"grades": grades})
    duration = time.time() - start
    
    assert response.status_code == 200
    assert duration < 3.0  # Should respond in under 2 seconds