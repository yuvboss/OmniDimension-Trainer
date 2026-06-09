import random


# Keywords that signal quality responses
_CONFIDENCE_WORDS = {"absolutely", "definitely", "certainly", "confident", "guarantee", "ensure", "proven", "proven"}
_EMPATHY_WORDS = {"understand", "appreciate", "hear you", "makes sense", "valid concern", "i see", "that's fair", "completely normal"}
_CLARITY_WORDS = {"specifically", "exactly", "let me explain", "what i mean", "in other words", "to clarify", "the reason"}
_NEXT_STEP_WORDS = {"schedule", "book", "appointment", "next step", "follow up", "when can", "shall we", "move forward", "sign", "visit"}
_WEAK_WORDS = {"um", "uh", "maybe", "i think", "i guess", "not sure", "probably", "sort of", "kind of"}


def _score_from_transcript(user_responses: list, common_objections: list, ideal_responses: dict) -> dict:
    """Score based on actual transcript content."""
    if not user_responses:
        return None  # Fall back to random

    full_text = " ".join(user_responses).lower()
    word_count = len(full_text.split())

    def keyword_score(keywords: set, base: int, bonus: int = 2) -> int:
        hits = sum(1 for kw in keywords if kw in full_text)
        return min(10, base + hits * bonus)

    def penalty(keywords: set, score: int, penalty_per: int = 1) -> int:
        hits = sum(1 for kw in keywords if kw in full_text)
        return max(1, score - hits * penalty_per)

    # Clarity: longer, specific responses score better
    clarity = 4 if word_count < 20 else 5 if word_count < 50 else 6
    clarity = keyword_score(_CLARITY_WORDS, clarity)
    clarity = penalty(_WEAK_WORDS, clarity)

    # Confidence: confident language, no hedging
    confidence = keyword_score(_CONFIDENCE_WORDS, 4)
    confidence = penalty(_WEAK_WORDS, confidence, 2)

    # Empathy: acknowledgment of concerns
    empathy = keyword_score(_EMPATHY_WORDS, 4)

    # Objection handling: check if user addressed each objection
    objection_score = 4
    for objection in common_objections[:3]:
        key_words = set(objection.lower().split())
        if any(w in full_text for w in key_words if len(w) > 4):
            objection_score = min(10, objection_score + 2)

    # Call control: response length and structure signals
    call_control = 5 if word_count > 30 else 3

    # Move to next step
    move_score = keyword_score(_NEXT_STEP_WORDS, 3, 3)

    # Product knowledge: addressed ideal response topics
    product_score = 4
    for resp in ideal_responses.values():
        overlap = set(resp.lower().split()) & set(full_text.split())
        if len(overlap) > 5:
            product_score = min(10, product_score + 1)

    # Clamp all scores to 1-10
    def clamp(v): return max(1, min(10, v))

    return {
        "clarity": clamp(clarity),
        "confidence": clamp(confidence),
        "product_knowledge": clamp(product_score),
        "empathy": clamp(empathy),
        "objection_handling": clamp(objection_score),
        "call_control": clamp(call_control),
        "move_to_next_step": clamp(move_score),
    }


def _random_scores(difficulty: str) -> dict:
    """Fallback random scores when no transcript is available."""
    ranges = {
        "easy":   (5, 8),
        "medium": (3, 6),
        "hard":   (1, 5),
    }
    lo, hi = ranges.get(difficulty, (3, 6))
    return {
        "clarity": random.randint(lo, hi),
        "confidence": random.randint(lo, hi),
        "product_knowledge": random.randint(lo, hi),
        "empathy": random.randint(lo, hi),
        "objection_handling": random.randint(lo, max(lo, hi - 1)),
        "call_control": random.randint(lo, hi),
        "move_to_next_step": random.randint(lo, max(lo, hi - 1)),
    }


def _find_response_for_objection(objection: str, conversation_turns: list):
    """Find the user turn immediately after the AI turn that raised the objection."""
    if not conversation_turns:
        return None
    objection_words = {w.lower() for w in objection.split() if len(w) > 3}
    for i, (speaker, text) in enumerate(conversation_turns):
        if speaker == "ai":
            text_words = {w.lower() for w in text.split()}
            if len(objection_words & text_words) >= 2:
                for j in range(i + 1, len(conversation_turns)):
                    if conversation_turns[j][0] == "user":
                        return conversation_turns[j][1]
    return None


def generate_feedback(
    scenario_data: dict,
    difficulty: str,
    call_responses: list,
    common_objections: list,
    ideal_responses: dict,
    conversation_turns: list = None,
) -> dict:
    # Use real transcript scoring if we have content, else fall back to random
    scores = _score_from_transcript(call_responses, common_objections, ideal_responses)
    if scores is None:
        scores = _random_scores(difficulty)

    strengths = []
    if scores["clarity"] >= 7:
        strengths.append("Clear and structured communication")
    if scores["confidence"] >= 7:
        strengths.append("Confident and assertive delivery")
    if scores["product_knowledge"] >= 7:
        strengths.append("Strong product knowledge")
    if scores["empathy"] >= 7:
        strengths.append("Good empathy and active listening")
    if scores["call_control"] >= 7:
        strengths.append("Strong call control and pacing")
    if scores["move_to_next_step"] >= 7:
        strengths.append("Effective at advancing the sale")
    if scores["objection_handling"] >= 7:
        strengths.append("Handled objections confidently")
    if not strengths:
        strengths = ["Professional approach maintained throughout"]

    improvements = []
    if scores["objection_handling"] <= 5:
        improvements.append("Address objections more directly — acknowledge the concern first, then counter")
    if scores["confidence"] <= 5:
        improvements.append("Build more confidence — avoid hedging words like 'maybe' or 'I think'")
    if scores["call_control"] <= 5:
        improvements.append("Take more control of the conversation flow")
    if scores["move_to_next_step"] <= 5:
        improvements.append("Push for a concrete next step — always end with a clear ask")
    if scores["product_knowledge"] <= 5:
        improvements.append("Deepen your product knowledge to answer questions without hesitation")
    if scores["clarity"] <= 5:
        improvements.append("Be more concise — lead with the key point, then add detail")
    if scores["empathy"] <= 5:
        improvements.append("Acknowledge the prospect's concerns before countering them")
    if not improvements:
        improvements = ["Keep building on your strong foundation"]

    # Match objections with the actual user response from the conversation
    objection_responses = []
    for objection in common_objections[:3]:
        user_said = None
        if conversation_turns:
            user_said = _find_response_for_objection(objection, conversation_turns)
        if not user_said:
            # Fall back: keyword search across all user responses
            objection_words = {w.lower() for w in objection.split() if len(w) > 3}
            best, best_score = None, 0
            for r in call_responses:
                score = len(objection_words & {w.lower() for w in r.split()})
                if score > best_score:
                    best_score, best = score, r
            user_said = best if best_score >= 1 else "This objection was not directly addressed"
        better_response = ideal_responses.get(
            objection,
            "Acknowledge the concern, provide specific evidence, then redirect to the next step."
        )
        objection_responses.append({
            "objection": objection,
            "user_said": user_said,
            "better_response": better_response,
        })

    return {
        "feedback": scores,
        "strengths": strengths,
        "improvements": improvements,
        "objection_responses": objection_responses,
        "average_score": round(sum(scores.values()) / len(scores), 1),
    }
