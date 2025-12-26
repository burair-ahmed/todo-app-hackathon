#!/bin/bash

# Setup script for Todo Full-Stack Application

echo "Setting up Todo Full-Stack Application..."

# Create virtual environment for backend
echo "Setting up backend environment..."
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd ..

# Setup frontend
echo "Setting up frontend..."
cd frontend
npm install
cd ..

echo "Setup complete! To run the application:"
echo "1. Start backend: cd backend && source venv/bin/activate && uvicorn src.main:app --reload"
echo "2. In another terminal, start frontend: cd frontend && npm run dev"