# Sales Training Voice Simulator

A voice-based sales training application built with Vue.js and FastAPI, powered by the OmniDimension Voice API. Sales professionals practice realistic customer conversations — the AI calls your phone, acts as a prospect or patient, raises objections, and generates post-call feedback based on the real transcript.

## Features

- **Live Voice Calls**: OmniDimension calls your phone number — no browser mic, no simulation
- **Industry Support**: Real estate and healthcare scenarios (extensible to other industries)
- **Realistic AI Customer**: GPT-4.1-mini plays the customer/patient and responds dynamically with ElevenLabs TTS
- **Objection Handling**: AI raises 1, 2, or 3+ objections depending on difficulty level
- **Performance Feedback**: Post-call scores (1–10), strengths, improvements, and side-by-side objection review
- **Difficulty Levels**: Easy, Medium, and Hard modes for progressive training

## Project Structure

```
OmniDimensionTrainer/
├── backend/                    # FastAPI server
│   ├── app.py                 # Main FastAPI application and routes
│   ├── database.py            # SQLAlchemy models and DB setup
│   ├── scenarios.py           # Scenario seed data
│   ├── feedback.py            # Heuristic feedback scoring (7 criteria)
│   ├── omnidim_service.py     # OmniDimension SDK wrapper
│   ├── requirements.txt       # Python dependencies
│   ├── .env                   # API key (not committed)
│   └── data/
│       └── scenarios.db       # SQLite database
│
├── frontend/                   # Vue.js SPA
│   ├── index.html
│   ├── src/
│   │   ├── main.js
│   │   ├── App.vue            # 3-step progress navbar
│   │   ├── style.css
│   │   ├── components/
│   │   │   ├── ScenarioSelector.vue   # Industry cards, scenario grid, phone input
│   │   │   ├── CallInterface.vue      # Call status UI with live polling
│   │   │   └── FeedbackReport.vue     # Score circle, objection review
│   │   └── services/
│   │       └── api.js
│   ├── package.json
│   └── vite.config.js
│
└── README.md
```

## Quick Start

### Prerequisites

- Python 3.9+
- Node.js 16+ and npm
- An OmniDimension API key (set in `backend/.env`)

### Backend Setup

1. Create and activate a Python virtual environment:
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `backend/.env` with your OmniDimension API key:
```
OMNIDIM_API_KEY=your_key_here
```

4. Start the backend server:
```bash
python -m uvicorn app:app --reload
```

The backend will:
- Initialize the SQLite database at `backend/data/scenarios.db`
- Seed it with 4 real estate and 4 healthcare scenarios
- Pre-load the OmniDimension agent cache from your account
- Run on `http://localhost:8000`

API documentation available at `http://localhost:8000/docs`

### Frontend Setup

1. Install Node.js dependencies:
```bash
cd frontend
npm install
```

2. Start the development server:
```bash
npm run dev
```

The frontend runs on `http://localhost:5173` (or `5174` if the port is taken).

## Usage

1. Open `http://localhost:5173` in your browser
2. Select an industry (Real Estate or Healthcare)
3. Choose a scenario and difficulty level
4. Enter your phone number and click **Start Practice**
5. OmniDimension will call your phone within ~1–2 minutes
6. Have the conversation — the AI acts as the customer and raises objections
7. Hang up when the call ends — the UI detects completion automatically
8. Review post-call feedback: scores, strengths, improvements, and your actual responses vs. the ideal

## API Endpoints

### Industries
- `GET /api/industries` — List all industries

### Scenarios
- `GET /api/industries/{id}/scenarios?difficulty=medium` — Get scenarios by industry
- `GET /api/scenarios/{id}` — Get full scenario details

### Calls
- `POST /api/calls/start` — Dispatch an OmniDim outbound call to the user's phone
- `GET /api/calls/{call_id}/status` — Poll call status (ringing / in-progress / completed)
- `POST /api/calls/{call_id}/end` — Fetch transcript and generate feedback

### Health
- `GET /health` — Health check

## Seed Scenarios

### Real Estate (4 scenarios)
1. **First-time Buyer Worried About Price** — Medium
2. **Buyer Comparing Builders** — Hard
3. **Investor Asking About Returns** — Medium
4. **Buyer Requesting Site Visit** — Easy

### Healthcare (4 scenarios)
1. **Patient Asking About Cost** — Medium
2. **Patient Concerned About Safety** — Hard
3. **Patient Booking First Appointment** — Easy
4. **Patient Comparing Doctors** — Medium

## Feedback Scoring

Post-call feedback scores each of 7 criteria on a 1–10 scale:

| Criterion | What It Measures |
|---|---|
| Clarity | How clearly you communicate |
| Confidence | Delivery and assertiveness |
| Product Knowledge | Understanding of what you're selling |
| Empathy | Listening and acknowledging the customer |
| Objection Handling | How well you address concerns |
| Call Control | Managing the conversation flow |
| Move to Next Step | Advancing the sale or booking |

The objection review shows each AI objection alongside your actual response and the ideal response, pulled directly from the call transcript.

## OmniDimension Integration

- **SDK**: `omnidimension` Python package
- **LLM**: GPT-4.1-mini
- **TTS**: ElevenLabs
- **Call type**: Outgoing (bot calls the user)
- **Agent strategy**: One agent per scenario+difficulty combination; agents are always updated on dispatch so prompt changes take effect immediately
- **Status matching**: Calls are matched by `call_request_id` (returned from dispatch) to avoid picking up stale logs from previous sessions
- **Concurrent call limit**: 1 active call at a time on standard account tier

## Extending to New Industries

1. Edit `backend/scenarios.py`
2. Add a new scenario list (e.g., `INSURANCE_SCENARIOS`)
3. Include it in `seed_database()`

Each scenario requires:
```python
{
    "name": "Scenario Title",
    "description": "Brief description",
    "deal_stage": "initial_call|pricing_discussion|booking|etc",
    "difficulty": "easy|medium|hard",
    "customer_profile": "Who the AI plays",
    "objective": "Goal of the call",
    "common_questions": ["Q1", "Q2", ...],
    "common_objections": ["Objection 1", ...],
    "ideal_responses": {
        "Objection 1": "Better response...",
    }
}
```

## Technology Stack

- **Frontend**: Vue.js 3, Vite, Axios
- **Backend**: FastAPI, SQLAlchemy, Pydantic
- **Database**: SQLite
- **Voice AI**: OmniDimension SDK, GPT-4.1-mini, ElevenLabs TTS

## Troubleshooting

**OmniDim call never arrives**
- Confirm `OMNIDIM_API_KEY` is set in `backend/.env`
- Check the backend logs — the dispatch response and `requestId` are logged
- OmniDim can take 1–3 minutes to connect; the UI polls every 6 seconds

**Frontend won't connect to backend**
- Ensure backend is running on `http://localhost:8000`
- Check Vite proxy config in `frontend/vite.config.js`

**Database not seeding**
- Delete `backend/data/scenarios.db` if it exists, then restart the backend

**npm not found**
- Install Node.js from https://nodejs.org/

## Future Enhancements

- User authentication and progress tracking
- Custom scenario builder
- Advanced analytics and team leaderboards
- CRM integration
- Machine learning-based feedback scoring
