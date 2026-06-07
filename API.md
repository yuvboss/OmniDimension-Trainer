# API Documentation

Base URL: `http://localhost:8000`  
Interactive Docs: `http://localhost:8000/docs`

## Endpoints

### Health Check

#### GET /health
Check if the server is running.

**Response:**
```json
{
  "status": "ok"
}
```

---

### Industries

#### GET /api/industries
Get list of all available industries.

**Response:**
```json
[
  {
    "id": 1,
    "name": "real_estate",
    "description": "Real estate sales training"
  },
  {
    "id": 2,
    "name": "healthcare",
    "description": "Healthcare clinic sales training"
  }
]
```

---

### Scenarios

#### GET /api/industries/{industry_id}/scenarios
Get scenarios for a specific industry.

**Parameters:**
- `industry_id` (path): Industry ID (1 or 2)
- `difficulty` (query, optional): Filter by difficulty (easy, medium, hard)

**Example:**
```
GET /api/industries/1/scenarios?difficulty=medium
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "First-time Buyer Worried About Price",
    "description": "A first-time buyer is interested but concerned about the price.",
    "deal_stage": "pricing_discussion",
    "difficulty": "medium",
    "customer_profile": "First-time buyer, budget-conscious"
  }
]
```

#### GET /api/scenarios/{scenario_id}
Get full details of a specific scenario.

**Parameters:**
- `scenario_id` (path): Scenario ID

**Response:**
```json
{
  "id": 1,
  "name": "First-time Buyer Worried About Price",
  "description": "A first-time buyer is interested but concerned about the price.",
  "deal_stage": "pricing_discussion",
  "difficulty": "medium",
  "customer_profile": "First-time buyer, budget-conscious",
  "objective": "Address price concerns and highlight value",
  "common_questions": [
    "Is this property overpriced?",
    "What's included in the price?",
    "Can we negotiate?",
    "What are the financing options?"
  ],
  "common_objections": [
    "The price feels high compared to other properties",
    "I need to talk to my family first",
    "I want to compare other options",
    "The maintenance costs seem high"
  ],
  "ideal_responses": {
    "The price feels high compared to other properties": "This property offers unique features...",
    "I need to talk to my family first": "That's a great idea! I can prepare..."
  }
}
```

---

### Calls

#### POST /api/calls/start
Start a new voice call session.

**Request Body:**
```json
{
  "scenario_id": 1
}
```

**Response:**
```json
{
  "call_id": "550e8400-e29b-41d4-a716-446655440000",
  "ai_greeting": "Hi, I'm interested in learning more about your properties in this area...",
  "scenario_name": "First-time Buyer Worried About Price",
  "status": "active"
}
```

#### POST /api/calls/{call_id}/respond
Send a user response during an active call.

**Parameters:**
- `call_id` (path): Call ID from start response

**Request Body:**
```json
{
  "user_response": "Our properties are competitively priced for the area."
}
```

**Response:**
```json
{
  "ai_response": "I understand, but the price feels high compared to other properties. What do you think about that?",
  "objection_raised": true,
  "status": "active",
  "message": "Response recorded. Continue the conversation."
}
```

#### POST /api/calls/{call_id}/end
End the call and receive feedback.

**Parameters:**
- `call_id` (path): Call ID from start response

**Request Body:**
```json
{
  "call_duration": 120
}
```

**Response:**
```json
{
  "feedback": {
    "clarity": 4,
    "confidence": 3,
    "product_knowledge": 5,
    "empathy": 4,
    "objection_handling": 3,
    "call_control": 4,
    "move_to_next_step": 3
  },
  "strengths": [
    "Good product knowledge",
    "Professional tone"
  ],
  "improvements": [
    "Address objections more directly",
    "Build more confidence in your responses"
  ],
  "objection_responses": [
    {
      "objection": "The price feels high compared to other properties",
      "user_said": "Our homes are priced competitively",
      "better_response": "I understand price is important. Let me show you the value..."
    }
  ],
  "average_score": 3.6
}
```

---

## Error Responses

All errors return appropriate HTTP status codes:

### 404 Not Found
```json
{
  "detail": "Scenario not found"
}
```

### 400 Bad Request
```json
{
  "detail": "Invalid request body"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

---

## Testing with cURL

### Start a call
```bash
curl -X POST http://localhost:8000/api/calls/start \
  -H "Content-Type: application/json" \
  -d '{"scenario_id": 1}'
```

### Respond to a call
```bash
curl -X POST http://localhost:8000/api/calls/{call_id}/respond \
  -H "Content-Type: application/json" \
  -d '{"user_response": "Your response here"}'
```

### End a call
```bash
curl -X POST http://localhost:8000/api/calls/{call_id}/end \
  -H "Content-Type: application/json" \
  -d '{"call_duration": 120}'
```

### Get industries
```bash
curl http://localhost:8000/api/industries
```

### Get scenarios for an industry
```bash
curl http://localhost:8000/api/industries/1/scenarios
```

### Get scenario details
```bash
curl http://localhost:8000/api/scenarios/1
```

---

## Database Schema

### industries
- `id` (INTEGER, PRIMARY KEY)
- `name` (TEXT, UNIQUE)
- `description` (TEXT)
- `created_at` (TIMESTAMP)

### scenarios
- `id` (INTEGER, PRIMARY KEY)
- `industry_id` (INTEGER, FOREIGN KEY)
- `name` (TEXT)
- `description` (TEXT)
- `deal_stage` (TEXT)
- `difficulty` (TEXT)
- `customer_profile` (TEXT)
- `objective` (TEXT)
- `common_questions` (JSON)
- `common_objections` (JSON)
- `ideal_responses` (JSON)
- `initial_prompt` (TEXT)
- `created_at` (TIMESTAMP)

### call_recordings
- `id` (INTEGER, PRIMARY KEY)
- `scenario_id` (INTEGER, FOREIGN KEY)
- `user_transcript` (TEXT)
- `ai_transcript` (TEXT)
- `call_duration` (INTEGER)
- `feedback_score` (JSON)
- `feedback_suggestions` (JSON)
- `created_at` (TIMESTAMP)

---

## Version

API Version: 1.0.0  
Last Updated: 2026-05-12
