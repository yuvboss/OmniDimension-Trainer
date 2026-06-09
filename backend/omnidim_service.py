import os
import re
from dotenv import load_dotenv
from omnidimension import Client

load_dotenv()

_client = None
_agent_cache = {}  # (scenario_id, difficulty) -> agent_id

# Pattern to match agents we created: "Trainer-<name>-<difficulty>"
_AGENT_NAME_RE = re.compile(r"^Trainer-.+-(?P<difficulty>easy|medium|hard)$")


def get_client():
    global _client
    if _client is None:
        api_key = os.environ.get("OMNIDIM_API_KEY")
        if not api_key:
            raise ValueError("OMNIDIM_API_KEY not set in environment")
        _client = Client(api_key)
    return _client


def preload_agent_cache(scenario_map: dict):
    """
    Fetch all agents from OmniDim and populate the in-memory cache.
    scenario_map: {agent_name: (scenario_id, difficulty)}  — built from DB at startup.
    """
    try:
        client = get_client()
        response = client.agent.list(page_size=100)
        bots = response.get("json", {}).get("bots", [])
        loaded = 0
        for bot in bots:
            name = bot.get("name", "")
            agent_id = bot.get("id")
            if name in scenario_map and agent_id:
                key = scenario_map[name]
                _agent_cache[key] = int(agent_id)
                loaded += 1
        print(f"[OmniDim] Pre-loaded {loaded} agents from OmniDimension into cache.")
    except Exception as e:
        print(f"[OmniDim] Warning: could not pre-load agent cache: {e}")


def _build_context_breakdown(scenario: dict, difficulty: str) -> list:
    common_objections = scenario.get("common_objections", [])
    common_questions = scenario.get("common_questions", [])
    questions_text = "\n".join(f"- {q}" for q in common_questions[:4])

    if difficulty == "easy":
        tone = (
            "You are friendly, warm, and genuinely interested. You are mostly ready to proceed but have one hesitation. "
            "If the rep gives a good answer to your concern, you happily agree to move forward."
        )
        objection_instruction = (
            f"At a natural point in the conversation, raise this one concern: \"{common_objections[0] if common_objections else 'I just need a little more time to think about it'}\". "
            "Be open to a reasonable answer and move forward if they address it well."
        )
    elif difficulty == "medium":
        objections_text = "\n".join(f"- {o}" for o in common_objections[:2])
        tone = (
            "You are moderately skeptical. You are comparing a couple of options and need your concerns properly addressed before committing. "
            "You won't agree to anything without a clear, specific answer."
        )
        objection_instruction = (
            "At natural points in the conversation, raise these 2 concerns one at a time:\n"
            f"{objections_text}\n"
            "Require specific, convincing responses before you warm up."
        )
    else:  # hard
        objections_text = "\n".join(f"- {o}" for o in common_objections[:4])
        tone = (
            "You are very skeptical, have done your research, and are comparing multiple options. "
            "You are not impressed by vague or generic answers. Push back when the rep is unclear. "
            "Only commit if the rep gives compelling, specific, factual responses to every concern."
        )
        objection_instruction = (
            "Raise at least 3 of these concerns throughout the conversation, one at a time. Push back hard on weak answers:\n"
            f"{objections_text}"
        )

    return [
        {
            "title": "YOUR ROLE — READ THIS CAREFULLY",
            "body": (
                f"You are a {scenario['customer_profile']}. You have called a sales representative to ask about their product or service. "
                "YOU are the CUSTOMER. The person who answers is the SALESPERSON. "
                "Your job is to ask questions and raise concerns FROM A CUSTOMER'S POINT OF VIEW — not to sell anything. "
                "NEVER ask questions like 'What are you looking for?' or 'What is your budget?' or 'How can I help you today?' — those are things a salesperson says. "
                "You are the one calling with questions. They are the one who should be answering and convincing you. "
                "Stay in character at all times. Do not reveal you are an AI."
            ),
        },
        {
            "title": "The Situation",
            "body": (
                f"{scenario['description']} "
                f"You called because you want to know more. The salesperson's job is to: {scenario['objective']}. "
                "You are evaluating whether to move forward based on how well they answer your questions and address your concerns."
            ),
        },
        {
            "title": "Your Personality",
            "body": tone,
        },
        {
            "title": "Questions You Want to Ask",
            "body": (
                "Ask these questions naturally as the conversation flows — don't ask them all at once:\n"
                f"{questions_text}"
            ),
        },
        {
            "title": "Concerns to Raise",
            "body": objection_instruction,
        },
        {
            "title": "How to Speak",
            "body": (
                "Speak like a real person on the phone — short, natural sentences (2-3 per turn). "
                "React to what the salesperson says. If their answer is vague, ask them to be more specific. "
                "If they address everything well, agree to the next step. "
                "Keep the total call under 5 minutes."
            ),
        },
    ]


def _make_agent_name(scenario_name: str, difficulty: str) -> str:
    return f"Trainer-{scenario_name[:25].strip()}-{difficulty}"


def _build_welcome_message(scenario: dict) -> str:
    profile = scenario.get("customer_profile", "").lower()
    name = scenario.get("name", "")
    if any(w in profile for w in ["buyer", "investor"]):
        return f"Hi, I was looking at some properties and I had a few questions. Do you have a minute to talk?"
    elif any(w in profile for w in ["patient"]):
        return f"Hi, I was looking at your clinic online and had a few questions before I book anything. Is now a good time?"
    else:
        return "Hi, I came across your service and had a few questions. Do you have a moment?"


def get_or_create_agent(scenario_id: int, scenario: dict, difficulty: str) -> int:
    cache_key = (scenario_id, difficulty)
    client = get_client()
    context_breakdown = _build_context_breakdown(scenario, difficulty)
    welcome_message = _build_welcome_message(scenario)
    agent_name = _make_agent_name(scenario["name"], difficulty)

    if cache_key in _agent_cache:
        # Always update so prompt changes take effect immediately
        agent_id = _agent_cache[cache_key]
        try:
            client.agent.update(agent_id, {
                "context_breakdown": context_breakdown,
                "welcome_message": welcome_message,
            })
            print(f"[OmniDim] Updated agent {agent_id} ({agent_name})")
        except Exception as e:
            print(f"[OmniDim] Warning: could not update agent {agent_id}: {e}")
        return agent_id

    response = client.agent.create(
        name=agent_name,
        context_breakdown=context_breakdown,
        welcome_message=welcome_message,
        bot_call_type="Outgoing",
    )

    agent_id = response["json"].get("id") or response["json"].get("bot_id")
    if not agent_id:
        raise ValueError(f"Agent creation failed — unexpected response: {response}")

    _agent_cache[cache_key] = int(agent_id)
    print(f"[OmniDim] Created agent {agent_id} ({agent_name})")
    return int(agent_id)


def dispatch_call(agent_id: int, phone_number: str, call_context: dict = None) -> dict:
    client = get_client()
    response = client.call.dispatch_call(
        agent_id=agent_id,
        to_number=phone_number,
        from_number_id=4224,
        call_context=call_context or {},
    )
    return response


def get_call_log(call_log_id) -> dict:
    client = get_client()
    response = client.call.get_call_log(call_log_id)
    logs = response.get("json", {}).get("call_log_data", [])
    return logs[0] if logs else {}


def get_recent_calls_for_agent(agent_id: int, page_size: int = 5) -> list:
    client = get_client()
    response = client.call.get_call_logs(agent_id=agent_id, page_size=page_size)
    return response.get("json", {}).get("call_log_data", [])


def parse_transcript(call_log: dict) -> tuple[list, list]:
    """Returns (user_lines, ai_lines) from any OmniDim transcript format."""
    turns = parse_conversation_turns(call_log)
    if turns:
        user_lines = [t for s, t in turns if s == "user"]
        ai_lines = [t for s, t in turns if s == "ai"]
        return user_lines, ai_lines

    raw = call_log.get("transcript") or call_log.get("transcription") or []
    user_lines, ai_lines = [], []

    if isinstance(raw, str):
        lines = [l.strip() for l in raw.split("\n") if l.strip()]
        for i, line in enumerate(lines):
            (ai_lines if i % 2 == 0 else user_lines).append(line)
        return user_lines, ai_lines

    if isinstance(raw, list):
        for entry in raw:
            role = (entry.get("role") or entry.get("speaker") or "").lower()
            text = entry.get("content") or entry.get("text") or entry.get("message") or ""
            if not text:
                continue
            if role in ("user", "human", "caller"):
                user_lines.append(text)
            else:
                ai_lines.append(text)

    return user_lines, ai_lines


def parse_conversation_turns(call_log: dict) -> list:
    """Returns [(speaker, text), ...] from call_conversation field. speaker is 'ai' or 'user'."""
    raw = call_log.get("call_conversation", "")
    if not raw or not isinstance(raw, str):
        return []
    turns = []
    for part in raw.split("<br/>"):
        part = part.strip()
        if part.startswith("LLM:"):
            turns.append(("ai", part[4:].strip()))
        elif part.startswith("User:"):
            turns.append(("user", part[5:].strip()))
    return turns


def make_scenario_name_map(scenarios: list) -> dict:
    """
    Build a name -> (scenario_id, difficulty) map for all scenarios,
    so preload_agent_cache can match existing OmniDim agents.
    """
    result = {}
    for s in scenarios:
        name = _make_agent_name(s["name"], s["difficulty"])
        result[name] = (s["id"], s["difficulty"])
    return result
