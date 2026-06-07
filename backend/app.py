from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
import uuid
import json
import random

from database import init_db, get_db, Industry, Scenario, CallRecording
from scenarios import seed_database
from feedback import generate_feedback

app = FastAPI(title="Sales Training Voice Simulator")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
async def startup():
    init_db()
    seed_database()


# Pydantic Models
class IndustryResponse(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        from_attributes = True


class ScenarioResponse(BaseModel):
    id: int
    name: str
    description: str
    deal_stage: str
    difficulty: str
    customer_profile: str

    class Config:
        from_attributes = True


class ScenarioDetailResponse(BaseModel):
    id: int
    name: str
    description: str
    deal_stage: str
    difficulty: str
    customer_profile: str
    objective: str
    common_questions: List[str]
    common_objections: List[str]
    ideal_responses: dict

    class Config:
        from_attributes = True


class CallStartRequest(BaseModel):
    scenario_id: int


class CallStartResponse(BaseModel):
    call_id: str
    ai_greeting: str
    scenario_name: str
    status: str


class CallRespondRequest(BaseModel):
    user_response: str


class CallRespondResponse(BaseModel):
    ai_response: str
    objection_raised: bool
    status: str
    message: str


class CallEndRequest(BaseModel):
    call_duration: int


class FeedbackResponse(BaseModel):
    feedback: dict
    strengths: List[str]
    improvements: List[str]
    objection_responses: List[dict]
    average_score: float


# In-memory storage for active calls (for demo purposes)
active_calls = {}


# API Routes
@app.get("/api/industries", response_model=List[IndustryResponse])
def get_industries(db: Session = Depends(get_db)):
    """Get all industries"""
    industries = db.query(Industry).all()
    return industries


@app.get("/api/industries/{industry_id}/scenarios", response_model=List[ScenarioResponse])
def get_scenarios_by_industry(
    industry_id: int,
    difficulty: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get scenarios for a specific industry"""
    query = db.query(Scenario).filter(Scenario.industry_id == industry_id)

    if difficulty:
        query = query.filter(Scenario.difficulty == difficulty)

    scenarios = query.all()

    if not scenarios:
        raise HTTPException(status_code=404, detail="No scenarios found")

    return scenarios


@app.get("/api/scenarios/{scenario_id}", response_model=ScenarioDetailResponse)
def get_scenario_detail(scenario_id: int, db: Session = Depends(get_db)):
    """Get full scenario details"""
    scenario = db.query(Scenario).filter(Scenario.id == scenario_id).first()

    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")

    # Convert JSON strings back to lists/dicts
    return {
        "id": scenario.id,
        "name": scenario.name,
        "description": scenario.description,
        "deal_stage": scenario.deal_stage,
        "difficulty": scenario.difficulty,
        "customer_profile": scenario.customer_profile,
        "objective": scenario.objective,
        "common_questions": json.loads(scenario.common_questions) if isinstance(scenario.common_questions, str) else scenario.common_questions,
        "common_objections": json.loads(scenario.common_objections) if isinstance(scenario.common_objections, str) else scenario.common_objections,
        "ideal_responses": json.loads(scenario.ideal_responses) if isinstance(scenario.ideal_responses, str) else scenario.ideal_responses
    }


@app.post("/api/calls/start", response_model=CallStartResponse)
def start_call(request: CallStartRequest, db: Session = Depends(get_db)):
    """Start a voice call with the AI agent"""
    scenario = db.query(Scenario).filter(Scenario.id == request.scenario_id).first()

    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")

    call_id = str(uuid.uuid4())

    # Generate initial AI greeting based on scenario
    common_questions = json.loads(scenario.common_questions) if isinstance(scenario.common_questions, str) else scenario.common_questions

    if "real_estate" in scenario.customer_profile.lower() or "buyer" in scenario.customer_profile.lower():
        greetings = [
            f"Hi! I'm interested in learning more about your properties in this area. I'm currently looking for something that fits my budget and needs.",
            f"Hello! I found your listing online and I'm very interested. Before I schedule a viewing, I have a few questions about the property.",
            f"Hi there! I've been looking at properties here for a while now. Tell me more about what makes your listings special."
        ]
    else:  # healthcare
        greetings = [
            f"Hello! I was referred here by a friend. I'm interested in learning about your treatment options for my condition.",
            f"Hi! I've done some research about your clinic and I'd like to know more about the services you offer and your experience.",
            f"Hi there! I'm considering this procedure and I'd like to understand more about the process, costs, and what to expect."
        ]

    ai_greeting = random.choice(greetings)

    # Store call in active calls
    active_calls[call_id] = {
        "scenario_id": request.scenario_id,
        "scenario_name": scenario.name,
        "difficulty": scenario.difficulty,
        "user_responses": [],
        "ai_responses": [ai_greeting],
        "objections_raised": [],
        "common_objections": json.loads(scenario.common_objections) if isinstance(scenario.common_objections, str) else scenario.common_objections,
        "ideal_responses": json.loads(scenario.ideal_responses) if isinstance(scenario.ideal_responses, str) else scenario.ideal_responses
    }

    return {
        "call_id": call_id,
        "ai_greeting": ai_greeting,
        "scenario_name": scenario.name,
        "status": "active"
    }


@app.post("/api/calls/{call_id}/respond", response_model=CallRespondResponse)
def respond_to_call(call_id: str, request: CallRespondRequest):
    """User responds to AI during the call"""
    if call_id not in active_calls:
        raise HTTPException(status_code=404, detail="Call not found")

    call = active_calls[call_id]
    call["user_responses"].append(request.user_response)

    # Decide if we raise an objection
    objection_raised = False
    ai_response = ""

    difficulty = call["difficulty"]
    common_objections = call["common_objections"]

    # Objection probability based on difficulty
    if difficulty == "easy":
        objection_chance = 0.2  # 20% chance
    elif difficulty == "medium":
        objection_chance = 0.5  # 50% chance
    else:  # hard
        objection_chance = 0.8  # 80% chance

    if random.random() < objection_chance and len(call["objections_raised"]) < 2:
        # Raise an objection
        available_objections = [o for o in common_objections if o not in call["objections_raised"]]
        if available_objections:
            objection = random.choice(available_objections)
            call["objections_raised"].append(objection)
            objection_raised = True
            ai_response = f"I understand, but {objection.lower()} What do you think about that?"
        else:
            ai_response = "That makes sense. Let's continue. Do you have any other questions?"
    else:
        # Continue conversation naturally
        responses = [
            "That's a good point. Let me think about that for a moment.",
            "I appreciate your perspective. How does that align with your needs?",
            "Interesting. Can you tell me more about why that's important to you?",
            "I see. That's definitely something we should consider."
        ]
        ai_response = random.choice(responses)

    call["ai_responses"].append(ai_response)

    return {
        "ai_response": ai_response,
        "objection_raised": objection_raised,
        "status": "active",
        "message": "Response recorded. Continue the conversation."
    }


@app.post("/api/calls/{call_id}/end", response_model=FeedbackResponse)
def end_call(call_id: str, request: CallEndRequest, db: Session = Depends(get_db)):
    """End the call and generate feedback"""
    if call_id not in active_calls:
        raise HTTPException(status_code=404, detail="Call not found")

    call = active_calls[call_id]

    # Get scenario details
    scenario = db.query(Scenario).filter(Scenario.id == call["scenario_id"]).first()

    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")

    # Generate feedback
    ideal_responses = call["ideal_responses"]
    feedback_data = generate_feedback(
        scenario_data={
            "name": scenario.name,
            "objective": scenario.objective
        },
        difficulty=call["difficulty"],
        call_responses=call["user_responses"],
        common_objections=call["objections_raised"],
        ideal_responses=ideal_responses
    )

    # Save call recording to database
    call_recording = CallRecording(
        scenario_id=call["scenario_id"],
        user_transcript=" | ".join(call["user_responses"]),
        ai_transcript=" | ".join(call["ai_responses"]),
        call_duration=request.call_duration,
        feedback_score=json.dumps(feedback_data["feedback"]),
        feedback_suggestions=json.dumps({
            "strengths": feedback_data["strengths"],
            "improvements": feedback_data["improvements"],
            "objection_responses": feedback_data["objection_responses"]
        })
    )
    db.add(call_recording)
    db.commit()

    # Remove from active calls
    del active_calls[call_id]

    return feedback_data


@app.get("/health")
def health():
    """Health check endpoint"""
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
