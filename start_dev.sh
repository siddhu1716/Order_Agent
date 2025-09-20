#!/bin/bash

# QuickPick Development Startup Script
# This script starts both the backend API and frontend development servers

echo "🚀 Starting QuickPick Development Environment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check if a port is in use
port_in_use() {
    lsof -i :$1 >/dev/null 2>&1
}

# Check prerequisites
echo -e "${BLUE}📋 Checking prerequisites...${NC}"

# Check Python
if ! command_exists python3; then
    echo -e "${RED}❌ Python 3 is not installed${NC}"
    exit 1
fi

# Check Node.js or Bun
if command_exists bun; then
    PACKAGE_MANAGER="bun"
    echo -e "${GREEN}✅ Bun found${NC}"
elif command_exists node; then
    PACKAGE_MANAGER="npm"
    echo -e "${GREEN}✅ Node.js found${NC}"
else
    echo -e "${RED}❌ Neither Node.js nor Bun is installed${NC}"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "myenv" ]; then
    echo -e "${YELLOW}⚠️  Virtual environment not found. Creating one...${NC}"
    python3 -m venv myenv
fi

# Activate virtual environment
echo -e "${BLUE}🐍 Activating Python virtual environment...${NC}"
source myenv/bin/activate

# Install Python dependencies
echo -e "${BLUE}📦 Installing Python dependencies...${NC}"
pip install -r requirements.txt 2>/dev/null || pip install -e .

# Check if frontend dependencies are installed
if [ ! -d "quickpick_frontend/node_modules" ]; then
    echo -e "${YELLOW}⚠️  Frontend dependencies not found. Installing...${NC}"
    cd quickpick_frontend
    if [ "$PACKAGE_MANAGER" = "bun" ]; then
        bun install
    else
        npm install
    fi
    cd ..
fi

# Check if ports are available
echo -e "${BLUE}🔍 Checking port availability...${NC}"

if port_in_use 8000; then
    echo -e "${YELLOW}⚠️  Port 8000 is already in use. Backend might already be running.${NC}"
fi

if port_in_use 5173; then
    echo -e "${YELLOW}⚠️  Port 5173 is already in use. Frontend might already be running.${NC}"
fi

# Create log directory
mkdir -p logs

# Function to start backend
start_backend() {
    echo -e "${GREEN}🚀 Starting Backend API on http://localhost:8000${NC}"
    python main.py > logs/backend.log 2>&1 &
    BACKEND_PID=$!
    echo $BACKEND_PID > logs/backend.pid
}

# Function to start frontend
start_frontend() {
    echo -e "${GREEN}🎨 Starting Frontend on http://localhost:5173${NC}"
    cd quickpick_frontend
    if [ "$PACKAGE_MANAGER" = "bun" ]; then
        bun dev > ../logs/frontend.log 2>&1 &
    else
        npm run dev > ../logs/frontend.log 2>&1 &
    fi
    FRONTEND_PID=$!
    echo $FRONTEND_PID > ../logs/frontend.pid
    cd ..
}

# Function to cleanup on exit
cleanup() {
    echo -e "\n${YELLOW}🛑 Shutting down servers...${NC}"
    
    if [ -f logs/backend.pid ]; then
        BACKEND_PID=$(cat logs/backend.pid)
        kill $BACKEND_PID 2>/dev/null
        rm logs/backend.pid
        echo -e "${GREEN}✅ Backend stopped${NC}"
    fi
    
    if [ -f logs/frontend.pid ]; then
        FRONTEND_PID=$(cat logs/frontend.pid)
        kill $FRONTEND_PID 2>/dev/null
        rm logs/frontend.pid
        echo -e "${GREEN}✅ Frontend stopped${NC}"
    fi
    
    deactivate
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Start servers
echo -e "${BLUE}🚀 Starting servers...${NC}"

# Start backend
start_backend

# Wait a moment for backend to start
sleep 3

# Start frontend
start_frontend

# Wait a moment for frontend to start
sleep 3

# Display status
echo -e "\n${GREEN}🎉 QuickPick Development Environment Started!${NC}"
echo -e "${BLUE}📊 Status:${NC}"
echo -e "  Backend API:  ${GREEN}http://localhost:8000${NC}"
echo -e "  Frontend:     ${GREEN}http://localhost:5173${NC}"
echo -e "  API Docs:     ${GREEN}http://localhost:8000/docs${NC}"
echo -e "\n${YELLOW}📝 Logs:${NC}"
echo -e "  Backend:  ${BLUE}logs/backend.log${NC}"
echo -e "  Frontend: ${BLUE}logs/frontend.log${NC}"
echo -e "\n${YELLOW}💡 Tips:${NC}"
echo -e "  - Press Ctrl+C to stop all servers"
echo -e "  - Check logs for debugging information"
echo -e "  - Backend API will be available at /docs for testing"
echo -e "\n${GREEN}🚀 Happy coding!${NC}"

# Keep script running
wait
