"""
Fixed set of quiz questions shown to the user, one at a time.

Each question has an id ("q1".."q10") and a list of options.
Each option has a numeric "value" (1-4) which is what the frontend sends
back to the backend inside POST /api/predict. The mood_engine module maps
these same ids/values to mood scores, so if you ever change the wording
here, make sure the values (1-4) stay the same, or update mood_engine.py
to match.

Q8 and Q9 are the fun/personal "mam" questions (Maggie + dance mood).
They're deliberately given a smaller weight in mood_engine.py so they
support the prediction without overpowering it.
"""

QUESTIONS = [
    {
        "id": "q1",
        "text": "How do you feel right now, mam?",
        "options": [
            {"value": 1, "label": "Happy"},
            {"value": 2, "label": "Okay"},
            {"value": 3, "label": "A little low"},
            {"value": 4, "label": "I don't know honestly"},
        ],
    },
    {
        "id": "q2",
        "text": "Was your day tiring, mam?",
        "options": [
            {"value": 1, "label": "Not at all"},
            {"value": 2, "label": "A little"},
            {"value": 3, "label": "Quite tiring"},
            {"value": 4, "label": "Completely exhausting"},
        ],
    },
    {
        "id": "q3",
        "text": "Did you smile/laugh today, mam?",
        "options": [
            {"value": 1, "label": "A lot"},
            {"value": 2, "label": "A few times"},
            {"value": 3, "label": "Barely"},
            {"value": 4, "label": "Honestly, not really"},
        ],
    },
    {
        "id": "q4",
        "text": "Do you feel well or not, mam?",
        "options": [
            {"value": 1, "label": "I'm feeling great"},
            {"value": 2, "label": "I'm okay"},
            {"value": 3, "label": "Not really"},
            {"value": 4, "label": "I feel pretty bad"},
        ],
    },
    {
        "id": "q5",
        "text": "If you had to describe today in one word, mam, what would it be?",
        "options": [
            {"value": 1, "label": "Good"},
            {"value": 2, "label": "Normal"},
            {"value": 3, "label": "Exhausting"},
            {"value": 4, "label": "Messy"},
        ],
    },
    {
        "id": "q6",
        "text": "Did you overthink today, mam?",
        "options": [
            {"value": 1, "label": "Not really"},
            {"value": 2, "label": "A little"},
            {"value": 3, "label": "Quite a lot"},
            {"value": 4, "label": "Way too much"},
        ],
    },
    {
        "id": "q7",
        "text": "Did you feel bored today, mam?",
        "options": [
            {"value": 1, "label": "Not at all"},
            {"value": 2, "label": "A little"},
            {"value": 3, "label": "Most of the day"},
            {"value": 4, "label": "Extremely bored"},
        ],
    },
    {
        "id": "q8",
        "text": "Maggie mili ya nahi, mam?",
        "options": [
            {"value": 1, "label": "Haan, mil gayi"},
            {"value": 2, "label": "Nahi mili, dukh hua"},
            {"value": 3, "label": "Try hi nahi kiya"},
            {"value": 4, "label": "Maggie ka mood hi nahi tha"},
        ],
    },
    {
        "id": "q9",
        "text": "Aaj dance karne ka mann hai ya nahi, mam?",
        "options": [
            {"value": 1, "label": "Haan, bilkul"},
            {"value": 2, "label": "Thoda sa"},
            {"value": 3, "label": "Mann nahi hai"},
            {"value": 4, "label": "Bilkul nahi, mood hi kharab hai"},
        ],
    },
    {
        "id": "q10",
        "text": "Do you feel like talking to someone right now, mam?",
        "options": [
            {"value": 1, "label": "Definitely"},
            {"value": 2, "label": "Maybe"},
            {"value": 3, "label": "Not really"},
            {"value": 4, "label": "I want to be left alone"},
        ],
    },
]

# Handy lookup: {"q1": {1: "Happy", 2: "Okay", ...}, ...}
# Used by the mood engine to build a small human-readable answer summary.
QUESTION_LABELS = {
    q["id"]: {opt["value"]: opt["label"] for opt in q["options"]} for q in QUESTIONS
}

QUESTION_TEXT = {q["id"]: q["text"] for q in QUESTIONS}
