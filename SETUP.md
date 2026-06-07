# Setup Instructions

## Prerequisites

- **Python** 3.9 or higher
- **Node.js** 16+ (includes npm)
- **npm** (comes with Node.js)

## Installation

### 1. Install Node.js (if not already installed)

Download from https://nodejs.org/ and install the LTS version.

Verify installation:
```bash
node --version
npm --version
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment (if not already created)
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
```

## Running the Application

### Terminal 1 - Start Backend Server

```bash
cd backend

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Start the server
python -m uvicorn app:app --reload
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

Backend is ready at: **http://localhost:8000**  
API docs: **http://localhost:8000/docs**

### Terminal 2 - Start Frontend Dev Server

```bash
cd frontend

# Start Vite dev server
npm run dev
```

You should see:
```
VITE v... dev server running at:
➜  Local:   http://localhost:5173/
```

Frontend is ready at: **http://localhost:5173**

## First Run

1. Open **http://localhost:5173** in your browser
2. Select an industry (Real Estate or Healthcare)
3. Choose a scenario
4. Select difficulty level (Easy, Medium, Hard)
5. Click "Start Practice"
6. Have a conversation with the AI
7. Click "End Call" to see feedback

## Troubleshooting

### Backend Issues

**Error: `ModuleNotFoundError: No module named 'fastapi'`**
- Make sure virtual environment is activated
- Run: `pip install -r requirements.txt`

**Error: `Address already in use`**
- Change port: `python -m uvicorn app:app --reload --port 8001`
- Update frontend proxy in `frontend/vite.config.js`

**Error: Database not found**
- Backend automatically creates database on startup
- If issues persist, delete `backend/data/scenarios.db` and restart

### Frontend Issues

**Error: `npm: command not found`**
- Install Node.js from https://nodejs.org/
- Then run: `npm install` in frontend directory

**Error: `Cannot GET /`**
- Make sure Vite dev server is running: `npm run dev`
- Check you're accessing http://localhost:5173 (not 8000)

**Error: API calls failing (502/503 errors)**
- Ensure backend is running on http://localhost:8000
- Check Vite proxy config: `frontend/vite.config.js`

**Error: `node_modules` issues**
- Delete `node_modules` folder
- Run: `npm install` again

### Database Reset

To reset the database and reseed scenarios:

```bash
cd backend
rm -f data/scenarios.db  # Delete existing database
# Restart the server - database will auto-create and seed
python -m uvicorn app:app --reload
```

## Development Workflow

1. Keep both servers running (backend + frontend)
2. Edit Vue components in `frontend/src/components/`
3. Frontend auto-reloads on changes
4. Edit backend routes in `backend/app.py`
5. Backend auto-reloads on changes (thanks to `--reload` flag)

## Building for Production

### Frontend Build
```bash
cd frontend
npm run build
# Output in frontend/dist/
```

### Backend Deployment
Use a production ASGI server like Gunicorn:
```bash
cd backend
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app:app
```

## Next Steps

- Read `README.md` for full project documentation
- Check `backend/app.py` for API implementation
- Review Vue components in `frontend/src/components/`
- Test all 8 seed scenarios

## Support

For issues or questions, refer to the main README.md or contact the development team.
