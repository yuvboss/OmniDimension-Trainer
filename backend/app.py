from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
import uuid
import json
import random

from database import init_db, get_db, Industry, Scenario, CallRecording
import omnidim_service

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
    # Pre-load existing OmniDim agents into cache
    try:
        from database import SessionLocal
        db = SessionLocal()
        scenarios = db.query(Scenario).all()
        scenario_list = [{"id": s.id, "name": s.name, "difficulty": s.difficulty} for s in scenarios]
        db.close()
        name_map = omnidim_service.make_scenario_name_map(scenario_list)
        omnidim_service.preload_agent_cache(name_map)
    except Exception as e:
        print(f"[Startup] Agent cache preload failed: {e}")


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
    phone_number: str


class CallStartResponse(BaseModel):
    call_id: str
    status: str
    message: str


class CallEndRequest(BaseModel):
    call_duration: Optional[int] = 0


class FeedbackResponse(BaseModel):
    feedback: dict
    strengths: List[str]
    improvements: List[str]
    objection_responses: List[dict]
    average_score: float


# In-memory storage for active calls
active_calls = {}


# API Routes
@app.get("/api/industries", response_model=List[IndustryResponse])
def get_industries(db: Session = Depends(get_db)):
    return db.query(Industry).all()


@app.get("/api/industries/{industry_id}/scenarios", response_model=List[ScenarioResponse])
def get_scenarios_by_industry(
    industry_id: int,
    difficulty: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Scenario).filter(Scenario.industry_id == industry_id)
    if difficulty:
        query = query.filter(Scenario.difficulty == difficulty)
    scenarios = query.all()
    if not scenarios:
        raise HTTPException(status_code=404, detail="No scenarios found")
    return scenarios


@app.get("/api/scenarios/{scenario_id}", response_model=ScenarioDetailResponse)
def get_scenario_detail(scenario_id: int, db: Session = Depends(get_db)):
    scenario = db.query(Scenario).filter(Scenario.id == scenario_id).first()
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")
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
        "ideal_responses": json.loads(scenario.ideal_responses) if isinstance(scenario.ideal_responses, str) else scenario.ideal_responses,
    }


@app.post("/api/calls/start", response_model=CallStartResponse)
def start_call(request: CallStartRequest, db: Session = Depends(get_db)):
    scenario = db.query(Scenario).filter(Scenario.id == request.scenario_id).first()
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")

    scenario_dict = {
        "name": scenario.name,
        "description": scenario.description,
        "customer_profile": scenario.customer_profile,
        "objective": scenario.objective,
        "common_objections": json.loads(scenario.common_objections) if isinstance(scenario.common_objections, str) else scenario.common_objections,
        "common_questions": json.loads(scenario.common_questions) if isinstance(scenario.common_questions, str) else scenario.common_questions,
    }

    try:
        agent_id = omnidim_service.get_or_create_agent(request.scenario_id, scenario_dict, scenario.difficulty)
        dispatch_result = omnidim_service.dispatch_call(agent_id, request.phone_number)
        request_id = (
            dispatch_result.get("json", {}).get("requestId")
            or dispatch_result.get("json", {}).get("request_id")
            or dispatch_result.get("requestId")
        )
        print(f"[Call] Dispatched agent={agent_id} request_id={request_id} to={request.phone_number}")
    except Exception as e:
        print(f"[Call] OmniDim dispatch failed: {e}")
        raise HTTPException(status_code=502, detail=f"Failed to dispatch call: {str(e)}")

    call_id = str(uuid.uuid4())
    active_calls[call_id] = {
        "scenario_id": request.scenario_id,
        "agent_id": agent_id,
        "request_id": request_id,
        "scenario_name": scenario.name,
        "difficulty": scenario.difficulty,
        "user_responses": [],
        "ai_responses": [],
        "objections_raised": [],
        "common_objections": json.loads(scenario.common_objections) if isinstance(scenario.common_objections, str) else scenario.common_objections,
        "ideal_responses": json.loads(scenario.ideal_responses) if isinstance(scenario.ideal_responses, str) else scenario.ideal_responses,
        "last_call_log": None,
    }

    return {"call_id": call_id, "status": "calling", "message": "Call dispatched. Your phone will ring shortly."}


@app.get("/api/calls/{call_id}/status")
def get_call_status(call_id: str):
    if call_id not in active_calls:
        raise HTTPException(status_code=404, detail="Call not found")

    call = active_calls[call_id]
    agent_id = call.get("agent_id")

    if not agent_id:
        return {"status": "calling"}

    try:
        logs = omnidim_service.get_recent_calls_for_agent(agent_id, page_size=10)
        if not logs:
            return {"status": "calling"}

        # Match by call_request_id so we never pick up old completed calls
        request_id = call.get("request_id")
        log = None
        if request_id:
            for entry in logs:
                if str(entry.get("call_request_id", "")) == str(request_id):
                    log = entry
                    break

        if not log:
            return {"status": "calling"}

        raw_status = (log.get("call_status") or log.get("status") or "").lower().replace("-", "_").replace(" ", "_")

        if raw_status in ("completed", "ended", "finished"):
            call["last_call_log"] = log
            return {"status": "completed"}
        elif raw_status in ("in_progress", "ongoing", "active", "answered", "in_progress"):
            return {"status": "in_progress"}
        elif raw_status in ("failed", "no_answer", "busy", "cancelled"):
            return {"status": "failed"}
        else:
            return {"status": "calling", "raw_status": raw_status}
    except Exception as e:
        print(f"[Status] OmniDim poll error: {e}")
        return {"status": "calling"}


@app.post("/api/calls/{call_id}/end", response_model=FeedbackResponse)
def end_call(call_id: str, request: CallEndRequest, db: Session = Depends(get_db)):
    if call_id not in active_calls:
        raise HTTPException(status_code=404, detail="Call not found")

    call = active_calls[call_id]
    scenario = db.query(Scenario).filter(Scenario.id == call["scenario_id"]).first()
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")

    # Try to get real transcript from OmniDim
    user_responses = call["user_responses"]
    ai_responses = call["ai_responses"]
    conversation_turns = []
    try:
        call_log = call.get("last_call_log")
        if not call_log and call.get("agent_id"):
            logs = omnidim_service.get_recent_calls_for_agent(call["agent_id"], page_size=3)
            call_log = logs[0] if logs else None
        if call_log:
            user_responses, ai_responses = omnidim_service.parse_transcript(call_log)
            conversation_turns = omnidim_service.parse_conversation_turns(call_log)
    except Exception as e:
        print(f"[End] Could not fetch transcript: {e}")

    feedback_data = generate_feedback(
        scenario_data={"name": scenario.name, "objective": scenario.objective},
        difficulty=call["difficulty"],
        call_responses=user_responses,
        common_objections=call["common_objections"],
        ideal_responses=call["ideal_responses"],
        conversation_turns=conversation_turns,
    )

    call_recording = CallRecording(
        scenario_id=call["scenario_id"],
        user_transcript=" | ".join(user_responses),
        ai_transcript=" | ".join(ai_responses),
        call_duration=request.call_duration or 0,
        feedback_score=json.dumps(feedback_data["feedback"]),
        feedback_suggestions=json.dumps({
            "strengths": feedback_data["strengths"],
            "improvements": feedback_data["improvements"],
            "objection_responses": feedback_data["objection_responses"],
        }),
    )
    db.add(call_recording)
    db.commit()

    del active_calls[call_id]
    return feedback_data


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
