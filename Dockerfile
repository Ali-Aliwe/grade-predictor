# Multi-stage build for both backend and frontend

# Stage 1: Build Frontend
FROM node:18-alpine as frontend-build
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Stage 2: Backend with Python
FROM python:3.11-slim
WORKDIR /app

# Copy backend files
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/app.py ./
COPY backend/model/ ./model/

# Copy frontend build
COPY --from=frontend-build /app/frontend/build ./static

# Install nginx to serve frontend
RUN apt-get update && apt-get install -y nginx && rm -rf /var/lib/apt/lists/*
COPY nginx.conf /etc/nginx/nginx.conf

# Expose ports
EXPOSE 80 5000

# Start both services
COPY start.sh ./
RUN chmod +x start.sh
CMD ["./start.sh"]