# Sales Training Voice Simulator

A voice-based sales training application built with Vue.js and FastAPI. Sales professionals practice realistic customer conversations with an AI agent that acts as a prospect or patient, raises objections, and provides post-call feedback.

## Features

- **Industry Support**: Real estate and healthcare scenarios (extensible to other industries)
- **Realistic Conversations**: AI acts as a customer/patient and responds dynamically
- **Objection Handling**: AI raises realistic objections based on difficulty level
- **Performance Feedback**: Post-call scores, strengths, improvements, and suggested responses
- **Difficulty Levels**: Easy, Medium, and Hard modes for progressive training
- **Extensible Design**: Add new industries and scenarios without code changes

## Project Structure

```
OmniDimensionTrainer/
├── backend/                    # FastAPI server
│   ├── app.py                 # Main FastAPI application
│   ├── database.py            # SQLAlchemy models and DB setup
│   ├── scenarios.py           # Scenario seed data
│   ├── feedback.py            # Feedback generation logic
│   ├── requirements.txt        # Python dependencies
│   ├── venv/                  # Python virtual environment
│   └── data/
│       └── scenarios.db       # SQLite database
│
├── frontend/                   # Vue.js SPA
│   ├── index.html             # Entry point
│   ├── src/
│   │   ├── main.js
│   │   ├── App.vue
│   │   ├── style.css
│   │   ├── components/
│   │   │   ├── ScenarioSelector.vue
│   │   │   ├── CallInterface.vue
│   │   │   └── FeedbackReport.vue
│   │   └── services/
│   │       └── api.js         # API service
│   ├── package.json
│   ├── vite.config.js
│   └── node_modules/          # (generated)
│
└── README.md
```

## Quick Start

### Prerequisites

- Python 3.9+
- Node.js 16+ and npm
- SQLite3

### Backend Setup

1. Create and activate Python virtual environment:
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Start the backend server:
```bash
python -m uvicorn app:app --reload
```

The backend will:
- Initialize the SQLite database at `backend/data/scenarios.db`
- Seed it with 4 real estate and 4 healthcare scenarios
- Run on `http://localhost:8000`

API documentation available at: `http://localhost:8000/docs`

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

The frontend will run on `http://localhost:5173`

## Usage

1. Open `http://localhost:5173` in your browser
2. Select an industry (Real Estate or Healthcare)
3. Choose a scenario and difficulty level
4. Click "Start Practice" to begin
5. Respond to the AI customer/patient
6. Review post-call feedback with scores and suggestions
7. Try another scenario or return home

## API Endpoints

### Industries
- `GET /api/industries` - List all industries

### Scenarios
- `GET /api/industries/{id}/scenarios?difficulty=medium` - Get scenarios by industry
- `GET /api/scenarios/{id}` - Get full scenario details

### Calls
- `POST /api/calls/start` - Start a new call
- `POST /api/calls/{call_id}/respond` - Send user response during call
- `POST /api/calls/{call_id}/end` - End call and get feedback

### Health
- `GET /health` - Health check

## Seed Scenarios

### Real Estate (4 scenarios)
1. **First-time Buyer Worried About Price** - Medium difficulty
2. **Buyer Comparing Builders** - Hard difficulty
3. **Investor Asking About Returns** - Medium difficulty
4. **Buyer Requesting Site Visit** - Easy difficulty

### Healthcare (4 scenarios)
1. **Patient Asking About Cost** - Medium difficulty
2. **Patient Concerned About Safety** - Hard difficulty
3. **Patient Booking First Appointment** - Easy difficulty
4. **Patient Comparing Doctors** - Medium difficulty

## Feedback Scoring

Users receive scores (1-5) on:
- **Clarity** - How clearly you communicate
- **Confidence** - Your delivery confidence
- **Product Knowledge** - Understanding of what you're selling
- **Empathy** - Listening and understanding the customer
- **Objection Handling** - How well you address concerns
- **Call Control** - Managing conversation flow
- **Move to Next Step** - Ability to advance the sale/booking

Post-call feedback includes:
- Overall average score
- Key strengths
- Areas for improvement
- Objection handling suggestions with better response examples

## Extending to New Industries

### Adding a New Industry

1. Edit `backend/scenarios.py`
2. Add industry-specific scenarios to a new list (e.g., `INSURANCE_SCENARIOS`)
3. Include in `seed_database()` function
4. Database schema automatically handles new data

### Scenario Structure

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
        ...
    }
}
```

## Architecture Notes

### Phase 1 (Current)
- Mock AI responses and objections
- Randomized feedback scores
- Full UI and frontend-backend integration
- No OmniDimension API integration

### Phase 2 (Planned)
- Real OmniDimension Voice API integration
- Audio recording and transcription
- Text-to-speech for AI responses
- Real feedback analysis
- Call recording storage and replay

## Technology Stack

- **Frontend**: Vue.js 3, Vite, Axios
- **Backend**: FastAPI, SQLAlchemy, Pydantic
- **Database**: SQLite
- **Styling**: Custom CSS with responsive design

## Development

### Backend Development
```bash
cd backend
source venv/bin/activate
python -m uvicorn app:app --reload
```

### Frontend Development
```bash
cd frontend
npm run dev
```

### Building for Production
```bash
# Frontend
cd frontend
npm run build
# Output in frontend/dist/

# Backend
# Deploy using uvicorn with gunicorn or similar
```

## Testing

Manual end-to-end flow:
1. Select a scenario and difficulty
2. Complete a mock call (3-5 exchanges)
3. Verify feedback scores display
4. Check objection handling suggestions
5. Return home and try different scenario
6. Test both industries

## Troubleshooting

**Frontend won't connect to backend**
- Ensure backend is running on `http://localhost:8000`
- Check Vite proxy config in `frontend/vite.config.js`

**Database not seeding**
- Delete `backend/data/scenarios.db` if it exists
- Restart backend - database will auto-seed on startup

**npm not found**
- Install Node.js from https://nodejs.org/
- Verify: `node --version && npm --version`

## Future Enhancements

- User authentication and progress tracking
- Custom scenario builder
- Advanced analytics and reporting
- Team leaderboards
- CRM integration
- Mobile app support
- Real voice integration with OmniDimension APIs
- Machine learning-based feedback scoring

## License

[To be determined]

## Support

For issues or questions, please contact the development team.
