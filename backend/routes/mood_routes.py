from flask import Blueprint, jsonify, request

from data.questions import QUESTIONS
from database import db
from models import MoodResult
from services.mood_engine import ANSWER_RULES, predict_mood

mood_bp = Blueprint("mood", __name__, url_prefix="/api")

REQUIRED_QUESTION_IDS = list(ANSWER_RULES.keys())  # ["q1", ..., "q7"]


@mood_bp.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "mahila-mitra-backend"})


@mood_bp.route("/questions", methods=["GET"])
def get_questions():
    return jsonify({"questions": QUESTIONS})


def _validate_answers(payload):
    """
    Returns (answers, error_message).
    answers is a clean dict of {"q1": 1, ..., "q7": 4} with ints, only if
    everything checks out. Otherwise answers is None and error_message
    explains what's wrong.
    """
    if not isinstance(payload, dict):
        return None, "Request body must be a JSON object."

    answers = payload.get("answers")
    if not isinstance(answers, dict):
        return None, "Missing or invalid 'answers' object."

    cleaned = {}
    for question_id in REQUIRED_QUESTION_IDS:
        if question_id not in answers:
            return None, f"Missing answer for '{question_id}'."

        raw_value = answers[question_id]
        try:
            value = int(raw_value)
        except (TypeError, ValueError):
            return None, f"Answer for '{question_id}' must be a number."

        if value not in ANSWER_RULES[question_id]:
            return None, f"Answer for '{question_id}' must be one of 1-4."

        cleaned[question_id] = value

    # Reject unexpected extra keys, just to keep things predictable.
    extra_keys = set(answers.keys()) - set(REQUIRED_QUESTION_IDS)
    if extra_keys:
        return None, f"Unexpected answer keys: {', '.join(sorted(extra_keys))}."

    return cleaned, None


@mood_bp.route("/predict", methods=["POST"])
def predict():
    payload = request.get_json(silent=True)
    answers, error = _validate_answers(payload)

    if error:
        return jsonify({"error": error}), 400

    result = predict_mood(answers)

    # Save just the mood outcome, not the raw answers, to the database.
    record = MoodResult(
        primary_mood=result["primaryMood"],
        secondary_mood=result["secondaryMood"],
        energy=result["energy"],
        social_battery=result["socialBattery"],
        social_level=result["socialLevel"],
        overthinking=result["overthinking"],
    )
    db.session.add(record)
    db.session.commit()

    return jsonify(result)
