import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

const COURSES = {
  'Semester 1': ['I1100', 'M1100', 'M1101', 'P1100', 'P1101', 'S1101', 'PHYS100', 'PHYS101'],
  'Semester 2': ['I1101', 'M1102', 'M1103', 'M1104', 'M1105', 'M1106', 'M1107'],
  'Semester 3': ['I2201', 'I2202', 'I2203', 'I2204', 'I2205', 'S2250', 'M2250', 'M2251'],
  'Semester 4': ['I2206', 'I2207', 'I2208', 'I2209', 'I2210', 'I2211', 'I2234']
};

function App() {
  const [grades, setGrades] = useState({});
  const [predictions, setPredictions] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Initialize with default grades
  const initializeGrades = (value = 70) => {
    const allGrades = {};
    Object.values(COURSES).flat().forEach(course => {
      allGrades[course] = value;
    });
    setGrades(allGrades);
  };

  // Handle input change
  const handleChange = (course, value) => {
    const numValue = Math.max(0, Math.min(100, parseFloat(value) || 0));
    setGrades(prev => ({ ...prev, [course]: numValue }));
  };

  // Predict grades
  const handlePredict = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.post(`${API_URL}/predict`, { grades });
      setPredictions(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Prediction failed');
    }
    setLoading(false);
  };

  // Fill all with average
  const fillWithAverage = () => {
    const avg = Object.values(grades).reduce((a, b) => a + b, 0) / Object.values(grades).length || 70;
    initializeGrades(Math.round(avg));
  };

  // Initialize on mount
  React.useEffect(() => {
    initializeGrades();
  }, []);

  return (
    <div className="app">
      <header className="header">
        <h1>🎓 Student Grade Predictor</h1>
        <p>Predict third-year performance based on first two years</p>
      </header>

      <div className="container">
        <div className="input-section">
          <div className="controls">
            <button onClick={() => initializeGrades(70)} className="btn btn-secondary">
              Reset to 70
            </button>
            <button onClick={fillWithAverage} className="btn btn-secondary">
              Fill with Average
            </button>
          </div>

          {Object.entries(COURSES).map(([semester, courses]) => (
            <div key={semester} className="semester-group">
              <h3>{semester}</h3>
              <div className="course-grid">
                {courses.map(course => (
                  <div key={course} className="course-input">
                    <label>{course}</label>
                    <input
                      type="number"
                      min="0"
                      max="100"
                      value={grades[course] || 0}
                      onChange={(e) => handleChange(course, e.target.value)}
                    />
                  </div>
                ))}
              </div>
            </div>
          ))}

          <button 
            onClick={handlePredict} 
            disabled={loading}
            className="btn btn-primary btn-large"
          >
            {loading ? 'Predicting...' : 'Predict Third Year Grades'}
          </button>

          {error && (
            <div className="error">
              ⚠️ {error}
            </div>
          )}
        </div>

        {predictions && (
          <div className="results-section">
            <h2>📊 Predicted Results</h2>
            
            <div className="summary-cards">
              <div className="card">
                <h3>Average Grade</h3>
                <div className="value">{predictions.average.toFixed(1)}</div>
              </div>
              <div className="card">
                <h3>Pass Rate</h3>
                <div className="value">{predictions.pass_rate.toFixed(0)}%</div>
              </div>
              <div className="card">
                <h3>Total Courses</h3>
                <div className="value">{Object.keys(predictions.predictions).length}</div>
              </div>
            </div>

            <h3>Course-by-Course Predictions</h3>
            <div className="predictions-grid">
              {Object.entries(predictions.predictions)
                .sort((a, b) => b[1] - a[1])
                .map(([course, grade]) => (
                  <div 
                    key={course} 
                    className={`prediction-item ${grade >= 70 ? 'good' : grade >= 50 ? 'pass' : 'fail'}`}
                  >
                    <span className="course-name">{course}</span>
                    <span className="grade">{grade.toFixed(1)}</span>
                    <span className="status">
                      {grade >= 70 ? '✓ Excellent' : grade >= 50 ? '✓ Pass' : '✗ Risk'}
                    </span>
                  </div>
                ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;