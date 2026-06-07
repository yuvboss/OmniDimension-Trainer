import random
import json


def generate_feedback(
    scenario_data: dict,
    difficulty: str,
    call_responses: list,
    common_objections: list,
    ideal_responses: dict
) -> dict:
    """Generate feedback based on call responses and scenario"""

    # Generate scores based on difficulty (out of 10, rigorous ranges)
    if difficulty == "easy":
        scores = {
            "clarity": random.randint(5, 8),
            "confidence": random.randint(5, 8),
            "product_knowledge": random.randint(4, 7),
            "empathy": random.randint(4, 7),
            "objection_handling": random.randint(4, 7),
            "call_control": random.randint(5, 8),
            "move_to_next_step": random.randint(4, 7)
        }
    elif difficulty == "medium":
        scores = {
            "clarity": random.randint(3, 6),
            "confidence": random.randint(3, 6),
            "product_knowledge": random.randint(3, 6),
            "empathy": random.randint(3, 6),
            "objection_handling": random.randint(2, 6),
            "call_control": random.randint(3, 6),
            "move_to_next_step": random.randint(2, 6)
        }
    else:  # hard
        scores = {
            "clarity": random.randint(1, 5),
            "confidence": random.randint(1, 5),
            "product_knowledge": random.randint(1, 4),
            "empathy": random.randint(1, 5),
            "objection_handling": random.randint(1, 4),
            "call_control": random.randint(1, 5),
            "move_to_next_step": random.randint(1, 4)
        }

    # Generate strengths
    strengths = []
    if scores["clarity"] >= 7:
        strengths.append("Clear communication")
    if scores["confidence"] >= 7:
        strengths.append("Confident delivery")
    if scores["product_knowledge"] >= 7:
        strengths.append("Strong product knowledge")
    if scores["empathy"] >= 7:
        strengths.append("Good empathy and listening")
    if scores["call_control"] >= 7:
        strengths.append("Strong call control")
    if scores["move_to_next_step"] >= 7:
        strengths.append("Effective at advancing the sale")

    if not strengths:
        strengths = ["Professional approach"]

    # Generate improvements
    improvements = []
    if scores["objection_handling"] <= 5:
        improvements.append("Address objections more directly and confidently")
    if scores["confidence"] <= 5:
        improvements.append("Build more confidence — avoid filler words and hesitation")
    if scores["call_control"] <= 5:
        improvements.append("Take more control of the conversation flow")
    if scores["move_to_next_step"] <= 5:
        improvements.append("Push harder to move the conversation to a concrete next step")
    if scores["product_knowledge"] <= 5:
        improvements.append("Deepen your product knowledge to answer questions without hesitation")
    if scores["clarity"] <= 5:
        improvements.append("Be more concise — avoid rambling or unclear explanations")
    if scores["empathy"] <= 5:
        improvements.append("Listen more actively and acknowledge the prospect's concerns")

    if not improvements:
        improvements = ["Continue building on your strengths"]

    # Match objections with user responses and suggest better answers
    objection_responses = []
    if len(call_responses) > 0 and len(common_objections) > 0:
        for i, objection in enumerate(common_objections[:2]):  # Show top 2
            better_response = ideal_responses.get(
                objection,
                "Let me address that concern. We can discuss this in more detail."
            )
            objection_responses.append({
                "objection": objection,
                "user_said": call_responses[i] if i < len(call_responses) else "Did not address this objection",
                "better_response": better_response
            })

    return {
        "feedback": scores,
        "strengths": strengths,
        "improvements": improvements,
        "objection_responses": objection_responses,
        "average_score": round(sum(scores.values()) / len(scores), 1)
    }
