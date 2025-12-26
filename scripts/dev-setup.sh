#!/bin/bash

# Development setup script for Todo Full-Stack Application

echo "Setting up development environment for Todo Full-Stack Application..."

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "Git is not installed. Please install git first."
    exit 1
fi

# Check if Python 3.11+ is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3.11 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
MAJOR_VERSION=$(echo $PYTHON_VERSION | cut -d'.' -f1)
MINOR_VERSION=$(echo $PYTHON_VERSION | cut -d'.' -f2)

if [ $MAJOR_VERSION -lt 3 ] || ([ $MAJOR_VERSION -eq 3 ] && [ $MINOR_VERSION -lt 11 ]); then
    echo "Python 3.11 or higher is required. Current version: $PYTHON_VERSION"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "Node.js is not installed. Please install Node.js 18 or higher."
    exit 1
fi

NODE_VERSION=$(node --version | sed 's/v//')
NODE_MAJOR=$(echo $NODE_VERSION | cut -d'.' -f1)

if [ $NODE_MAJOR -lt 18 ]; then
    echo "Node.js 18 or higher is required. Current version: $NODE_VERSION"
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "npm is not installed. Please install npm."
    exit 1
fi

echo "All prerequisites are installed."

# Create .env files if they don't exist
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo ".env file created from .env.example"
fi

if [ ! -f "backend/.env" ]; then
    cp .env.example backend/.env
    echo "backend/.env file created from .env.example"
fi

if [ ! -f "frontend/.env.local" ]; then
    cp .env.example frontend/.env.local
    echo "frontend/.env.local file created from .env.example"
fi

echo "Development environment setup complete!"
echo ""
echo "To start development:"
echo "1. For backend: cd backend && source venv/bin/activate && uvicorn src.main:app --reload --port 8000"
echo "2. For frontend: cd frontend && npm run dev"