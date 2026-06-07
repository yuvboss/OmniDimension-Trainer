from database import SessionLocal, Industry, Scenario
import json

REAL_ESTATE_SCENARIOS = [
    {
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
            "The price feels high compared to other properties": "This property offers unique features and location benefits that justify the price. Let me show you the comparable sales data.",
            "I need to talk to my family first": "That's a great idea! I can prepare all the documentation for your family review. When would be a good time to follow up?",
            "I want to compare other options": "Absolutely, comparing is smart. This property stands out because of X, Y, and Z. Would you like me to highlight our competitive advantages?",
            "The maintenance costs seem high": "Our homes are built with premium materials. Plus, we offer a 10-year warranty that covers major repairs."
        }
    },
    {
        "name": "Buyer Comparing Builders",
        "description": "A skeptical buyer is comparing multiple builders and asking tough questions.",
        "deal_stage": "initial_call",
        "difficulty": "hard",
        "customer_profile": "Skeptical buyer, comparing builders",
        "objective": "Differentiate from competitors and build trust",
        "common_questions": [
            "What makes your builder different?",
            "How long have you been in business?",
            "Do you have customer references?",
            "What's your warranty coverage?"
        ],
        "common_objections": [
            "Competitor A is cheaper",
            "I've heard negative reviews about your company",
            "Your timelines seem unrealistic",
            "I'm not sure I can trust your quality"
        ],
        "ideal_responses": {
            "Competitor A is cheaper": "Lower price often means lower quality. Our homes have industry-leading features and come with a comprehensive warranty.",
            "I've heard negative reviews about your company": "We take every review seriously. Would you like to speak with our recent clients? I can connect you with 5 satisfied homeowners.",
            "Your timelines seem unrealistic": "Our timelines are based on proven project management. Here's our track record of on-time deliveries.",
            "I'm not sure I can trust your quality": "We're certified and have won multiple quality awards. Every home undergoes a rigorous inspection process."
        }
    },
    {
        "name": "Investor Asking About Returns",
        "description": "An investor is interested in rental income and ROI.",
        "deal_stage": "final_decision",
        "difficulty": "medium",
        "customer_profile": "Property investor, ROI-focused",
        "objective": "Demonstrate investment value and rental potential",
        "common_questions": [
            "What's the expected rental income?",
            "What's the appreciation potential?",
            "What are the hidden costs?",
            "How tenantable is this location?"
        ],
        "common_objections": [
            "The ROI is lower than other markets",
            "I'm concerned about tenant vacancy",
            "The location might not appreciate",
            "I need more time to analyze numbers"
        ],
        "ideal_responses": {
            "The ROI is lower than other markets": "While ROI is important, this location has strong fundamentals: stable economy, growing population, and consistent demand.",
            "I'm concerned about tenant vacancy": "This area has a 95% occupancy rate. We can connect you with property managers who have a track record here.",
            "The location might not appreciate": "Historical data shows 4% annual appreciation in this neighborhood. Economic development plans support future growth.",
            "I need more time to analyze numbers": "Absolutely, take your time. I've prepared a detailed financial analysis. When would you like to review it together?"
        }
    },
    {
        "name": "Buyer Requesting Site Visit",
        "description": "A buyer is interested and ready to visit the property.",
        "deal_stage": "initial_call",
        "difficulty": "easy",
        "customer_profile": "Engaged buyer, ready to view",
        "objective": "Secure a site visit appointment",
        "common_questions": [
            "Can I visit the property this weekend?",
            "What should I look for during the visit?",
            "How long does the tour take?",
            "Can I bring my family?"
        ],
        "common_objections": [
            "I'm busy this weekend",
            "Can you come down on the price if I view today?",
            "I want to bring my inspector",
            "I need to check my schedule"
        ],
        "ideal_responses": {
            "I'm busy this weekend": "No problem! What about next week? I can work around your schedule.",
            "Can you come down on the price if I view today?": "Let's focus on finding the right property first. The price reflects the market value. I can discuss financing options.",
            "I want to bring my inspector": "Great idea! Professional inspection is always recommended. I can coordinate with the owner.",
            "I need to check my schedule": "Take your time. Here are a few time slots available. Feel free to reach out when you're ready."
        }
    }
]

HEALTHCARE_SCENARIOS = [
    {
        "name": "Patient Asking About Cost",
        "description": "A patient is interested in treatment but concerned about the cost.",
        "deal_stage": "consultation",
        "difficulty": "medium",
        "customer_profile": "Cost-conscious patient",
        "objective": "Address cost concerns and explain value",
        "common_questions": [
            "What's the total cost of treatment?",
            "Does insurance cover this?",
            "What are payment options?",
            "Why is this procedure so expensive?"
        ],
        "common_objections": [
            "The treatment is too expensive",
            "I can't afford this right now",
            "Another clinic quoted a lower price",
            "I need to think about it"
        ],
        "ideal_responses": {
            "The treatment is too expensive": "I understand cost is important. This treatment uses advanced technology and our success rate is 95%. We offer flexible payment plans.",
            "I can't afford this right now": "We have multiple payment options, including installment plans with no interest. Let's find a solution that works for you.",
            "Another clinic quoted a lower price": "Lower price might mean different technology or less experienced practitioners. Our clinic uses cutting-edge equipment and board-certified doctors.",
            "I need to think about it": "That's completely reasonable. Delaying treatment can increase complications and costs later. Can we schedule a follow-up call?"
        }
    },
    {
        "name": "Patient Concerned About Safety",
        "description": "A skeptical patient is worried about procedure safety and risks.",
        "deal_stage": "consultation",
        "difficulty": "hard",
        "customer_profile": "Safety-conscious, anxious patient",
        "objective": "Build confidence and address safety concerns",
        "common_questions": [
            "How safe is this procedure?",
            "What are the risks?",
            "What's the recovery time?",
            "Have you done this many times?"
        ],
        "common_objections": [
            "I'm scared of the procedure",
            "I've heard horror stories online",
            "What if something goes wrong?",
            "I want a second opinion"
        ],
        "ideal_responses": {
            "I'm scared of the procedure": "That's completely normal. I've had thousands of patients with similar concerns. Our team is experienced and we prioritize your comfort.",
            "I've heard horror stories online": "Online stories are usually outliers. Our hospital has a 99.2% safety record. We can connect you with patients who had successful procedures.",
            "What if something goes wrong?": "We follow strict safety protocols. Our surgical team has 15+ years of experience. We have emergency procedures in place if needed.",
            "I want a second opinion": "I encourage that! A second opinion confirms you're making the right decision. We can provide all your medical records."
        }
    },
    {
        "name": "Patient Booking First Appointment",
        "description": "A new patient wants to schedule their first consultation.",
        "deal_stage": "booking",
        "difficulty": "easy",
        "customer_profile": "New patient, ready to schedule",
        "objective": "Secure appointment and gather patient information",
        "common_questions": [
            "When can I schedule an appointment?",
            "Do I need a referral?",
            "What should I bring?",
            "How long is the first visit?"
        ],
        "common_objections": [
            "I'm not available during your hours",
            "Can I schedule a virtual consultation first?",
            "I need to confirm my insurance first",
            "I want to think about it more"
        ],
        "ideal_responses": {
            "I'm not available during your hours": "We have evening and weekend appointments available. What time works best for you?",
            "Can I schedule a virtual consultation first?": "Absolutely! We can start with a 15-minute virtual consultation. It helps me understand your concerns before the in-person visit.",
            "I need to confirm my insurance first": "That's smart. We accept most major insurance plans. I can verify your coverage while we schedule.",
            "I want to think about it more": "No problem! Take your time. Here's my contact info. Feel free to call when you're ready to book."
        }
    },
    {
        "name": "Patient Comparing Doctors",
        "description": "A patient is deciding between multiple doctors/clinics.",
        "deal_stage": "follow_up",
        "difficulty": "medium",
        "customer_profile": "Comparison-shopping patient",
        "objective": "Differentiate the practice and build trust",
        "common_questions": [
            "How experienced are you?",
            "What's your success rate?",
            "Do you have patient testimonials?",
            "What's your treatment philosophy?"
        ],
        "common_objections": [
            "Another doctor has more experience",
            "I'm not sure about the treatment plan",
            "The other clinic seems more convenient",
            "I need time to decide"
        ],
        "ideal_responses": {
            "Another doctor has more experience": "While experience matters, I've successfully treated 500+ patients in this specialty. Quality of care matters more than years in practice.",
            "I'm not sure about the treatment plan": "Great question! Let me explain the rationale. We follow evidence-based protocols that have the highest success rates.",
            "The other clinic seems more convenient": "Convenience is secondary to quality care. We're located near public transport and offer flexible scheduling to make it work.",
            "I need time to decide": "Absolutely. Consider the pros/cons of each doctor. I'm confident you'll find our approach personalized and professional."
        }
    }
]


def seed_database():
    """Seed the database with initial scenario data"""
    db = SessionLocal()

    try:
        # Check if data already exists
        if db.query(Industry).count() > 0:
            print("Database already seeded. Skipping...")
            return

        # Create industries
        real_estate = Industry(name="real_estate", description="Real estate sales training")
        healthcare = Industry(name="healthcare", description="Healthcare clinic sales training")

        db.add(real_estate)
        db.add(healthcare)
        db.commit()

        # Create real estate scenarios
        for scenario_data in REAL_ESTATE_SCENARIOS:
            scenario = Scenario(
                industry_id=real_estate.id,
                name=scenario_data["name"],
                description=scenario_data["description"],
                deal_stage=scenario_data["deal_stage"],
                difficulty=scenario_data["difficulty"],
                customer_profile=scenario_data["customer_profile"],
                objective=scenario_data["objective"],
                common_questions=json.dumps(scenario_data["common_questions"]),
                common_objections=json.dumps(scenario_data["common_objections"]),
                ideal_responses=json.dumps(scenario_data["ideal_responses"]),
                initial_prompt=""
            )
            db.add(scenario)

        # Create healthcare scenarios
        for scenario_data in HEALTHCARE_SCENARIOS:
            scenario = Scenario(
                industry_id=healthcare.id,
                name=scenario_data["name"],
                description=scenario_data["description"],
                deal_stage=scenario_data["deal_stage"],
                difficulty=scenario_data["difficulty"],
                customer_profile=scenario_data["customer_profile"],
                objective=scenario_data["objective"],
                common_questions=json.dumps(scenario_data["common_questions"]),
                common_objections=json.dumps(scenario_data["common_objections"]),
                ideal_responses=json.dumps(scenario_data["ideal_responses"]),
                initial_prompt=""
            )
            db.add(scenario)

        db.commit()
        print("Database seeded successfully!")
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
