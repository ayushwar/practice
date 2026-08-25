"""
Mood Engine
===========

This is a plain rule-based scoring system. No AI, no ML, no external API.

The idea is simple:

  * Every answer to every question nudges a handful of "mood points"
    (Happy, Tired, Overthinking, etc.), an "energy" number, and a
    "social battery" number.
  * Once all 10 answers are in, we add everything up and read off:
      - the two strongest moods (primary + secondary)
      - an energy level (High / Medium / Low)
      - a social battery percentage + level
      - an overthinking level (Low / Medium / High / Very High)
      - a friendly, Hinglish message that matches the mood combination

Nothing here is random - the same answers will always produce the same
result. If you want to tweak how "sensitive" a question is, just change
the numbers in ANSWER_RULES below.

Q8 (Maggie) and Q9 (dance mood) are fun/personal questions. They're
intentionally given small point values so they act as light supporting
signals only, never enough to flip the overall prediction by themselves
(see the module docstring in data/questions.py).
"""

from data.questions import QUESTION_LABELS

# All mood categories the engine can talk about.
MOOD_CATEGORIES = [
    "Happy",
    "Normal",
    "Talkative",
    "Excited",
    "Tired",
    "Bored",
    "Overthinking",
    "Low",
    "Irritated",
    "Quiet",
    "Needs Space",
    "Playful",
]


def _mood(**kwargs):
    """Small helper so the table below reads like plain English."""
    return kwargs


# ---------------------------------------------------------------------------
# ANSWER_RULES
#
# For every question, for every possible answer value (1-4), this table
# says exactly how many points go where:
#   - "mood":   dict of {MoodCategory: points} added to the running totals
#   - "energy": points added to (or subtracted from) the energy score
#   - "social": points added to (or subtracted from) the social battery
#
# Energy and social battery both start at a neutral baseline of 50 and are
# clamped to the 0-100 range once every answer has been added in.
#
# Q1-Q7 and Q10 are the "serious" mood-signal questions and carry the
# most weight. Q8 (Maggie) and Q9 (dance mood) are fun/personal questions
# and are kept deliberately small (max 2-4 points) so they only ever
# nudge the result, never decide it.
# ---------------------------------------------------------------------------
ANSWER_RULES = {
    "q1": {  # How do you feel right now, mam?
        1: {"mood": _mood(Happy=3, Excited=1), "energy": 10, "social": 8},
        2: {"mood": _mood(Normal=3), "energy": 4, "social": 2},
        3: {"mood": _mood(Low=3, Quiet=1), "energy": -8, "social": -8},
        4: {"mood": _mood(Overthinking=2, Quiet=1, Normal=1), "energy": -2, "social": -3},
    },
    "q2": {  # Was your day tiring, mam?
        1: {"mood": _mood(Happy=1, Excited=1), "energy": 10, "social": 4},
        2: {"mood": _mood(Tired=1), "energy": 2, "social": 0},
        3: {"mood": _mood(Tired=3, Quiet=1), "energy": -8, "social": -5},
        4: {"mood": _mood(Tired=5, **{"Needs Space": 2}, Quiet=2), "energy": -16, "social": -10},
    },
    "q3": {  # Did you smile/laugh today, mam?
        1: {"mood": _mood(Happy=3, Talkative=2, Excited=1), "energy": 8, "social": 15},
        2: {"mood": _mood(Happy=1, Normal=1), "energy": 3, "social": 5},
        3: {"mood": _mood(Low=2, Quiet=1), "energy": -5, "social": -8},
        4: {"mood": _mood(Low=3, Irritated=1, **{"Needs Space": 1}), "energy": -8, "social": -15},
    },
    "q4": {  # Do you feel well or not, mam?
        1: {"mood": _mood(Happy=2, Excited=1), "energy": 10, "social": 5},
        2: {"mood": _mood(Normal=2), "energy": 3, "social": 1},
        3: {"mood": _mood(Low=2, Tired=1), "energy": -8, "social": -4},
        4: {"mood": _mood(Low=3, Tired=2, **{"Needs Space": 1}), "energy": -15, "social": -6},
    },
    "q5": {  # Describe today in one word, mam
        1: {"mood": _mood(Happy=2, Normal=1), "energy": 5, "social": 3},
        2: {"mood": _mood(Normal=3), "energy": 2, "social": 0},
        3: {"mood": _mood(Tired=3, Quiet=1), "energy": -10, "social": -4},
        4: {"mood": _mood(Overthinking=2, Irritated=1, Bored=1), "energy": -3, "social": -3},
    },
    "q6": {  # Did you overthink today, mam? (strongest overthinking signal)
        1: {"mood": _mood(Overthinking=0, Normal=1), "energy": 1, "social": 1},
        2: {"mood": _mood(Overthinking=1), "energy": 0, "social": 0},
        3: {"mood": _mood(Overthinking=3, Quiet=1), "energy": -3, "social": -3},
        4: {"mood": _mood(Overthinking=5, Quiet=2, **{"Needs Space": 1}), "energy": -5, "social": -6},
    },
    "q7": {  # Did you feel bored today, mam?
        1: {"mood": _mood(Bored=0, Talkative=1), "energy": 2, "social": 10},
        2: {"mood": _mood(Bored=1), "energy": 0, "social": 3},
        3: {"mood": _mood(Bored=2, Irritated=1), "energy": -3, "social": -8},
        4: {"mood": _mood(Bored=3, Irritated=2, **{"Needs Space": 1}), "energy": -5, "social": -15},
    },
    "q8": {  # Maggie mili ya nahi, mam? (small supporting signal only)
        1: {"mood": _mood(Happy=1, Playful=1), "energy": 2, "social": 2},
        2: {"mood": _mood(Low=1, Irritated=1), "energy": -2, "social": -1},
        3: {"mood": _mood(Normal=1, Tired=1), "energy": -1, "social": 0},
        4: {"mood": _mood(Low=1, Tired=1, **{"Needs Space": 1}), "energy": -3, "social": -2},
    },
    "q9": {  # Aaj dance karne ka mann hai ya nahi, mam? (small supporting signal only)
        1: {"mood": _mood(Happy=1, Excited=1, Playful=2), "energy": 4, "social": 3},
        2: {"mood": _mood(Happy=1, Playful=1), "energy": 2, "social": 1},
        3: {"mood": _mood(Tired=1, Normal=1), "energy": -2, "social": -1},
        4: {"mood": _mood(Low=1, Irritated=1, Tired=1), "energy": -4, "social": -3},
    },
    "q10": {  # Do you feel like talking to someone right now, mam?
        1: {"mood": _mood(Talkative=3, Happy=1), "energy": 3, "social": 15},
        2: {"mood": _mood(Talkative=1, Normal=1), "energy": 1, "social": 3},
        3: {"mood": _mood(Quiet=2), "energy": -2, "social": -8},
        4: {"mood": _mood(Quiet=2, **{"Needs Space": 3}), "energy": -4, "social": -18},
    },
}

ENERGY_BASELINE = 50
SOCIAL_BASELINE = 50


def _clamp(value, low=0, high=100):
    return max(low, min(high, value))


def calculate_scores(answers):
    """
    answers: dict like {"q1": 1, "q2": 3, ...} (values are ints 1-4)

    Returns a dict with:
      mood_totals   -> {"Happy": 5, "Tired": 2, ...} for every category
      energy_score  -> 0-100
      social_score  -> 0-100
    """
    mood_totals = {category: 0 for category in MOOD_CATEGORIES}
    energy_score = ENERGY_BASELINE
    social_score = SOCIAL_BASELINE

    for question_id, answer_value in answers.items():
        rule = ANSWER_RULES[question_id][answer_value]
        for mood_name, points in rule["mood"].items():
            mood_totals[mood_name] += points
        energy_score += rule["energy"]
        social_score += rule["social"]

    energy_score = _clamp(energy_score)
    social_score = _clamp(social_score)

    return {
        "mood_totals": mood_totals,
        "energy_score": energy_score,
        "social_score": social_score,
    }


def determine_primary_secondary(mood_totals):
    """Pick the strongest mood, then the strongest *different* mood."""
    ranked = sorted(mood_totals.items(), key=lambda pair: pair[1], reverse=True)

    primary = ranked[0][0]
    secondary = None
    for mood_name, points in ranked[1:]:
        if points > 0:
            secondary = mood_name
            break

    return primary, secondary


def energy_level(energy_score):
    if energy_score >= 65:
        return "High"
    if energy_score >= 35:
        return "Medium"
    return "Low"


def social_level(social_score):
    if social_score >= 70:
        return "High"
    if social_score >= 40:
        return "Medium"
    return "Low"


def overthinking_level(mood_totals):
    score = mood_totals.get("Overthinking", 0)
    if score >= 7:
        return "Very High"
    if score >= 4:
        return "High"
    if score >= 2:
        return "Medium"
    return "Low"


def overall_label(primary, energy_lvl):
    """A one/two word overall flavour tag, purely cosmetic."""
    positive = {"Happy", "Excited", "Talkative", "Playful", "Normal"}
    negative = {"Low", "Tired", "Irritated", "Bored"}

    if primary in positive and energy_lvl == "High":
        return "Very Positive"
    if primary in positive:
        return "Pretty Good"
    if primary in negative and energy_lvl == "Low":
        return "Mentally Drained"
    if primary in negative:
        return "Could Be Better"
    return "Mixed Bag"


# ---------------------------------------------------------------------------
# Result messages (natural Hinglish, "mam" flavoured)
#
# Keyed by a sorted tuple of (primary, secondary) so order doesn't matter,
# e.g. ("Excited", "Happy") and ("Happy", "Excited") hit the same entry.
# Add as many combinations here as you like - anything not listed falls
# back to FALLBACK_MESSAGES for a single mood.
# ---------------------------------------------------------------------------
COMBO_MESSAGES = {
    tuple(sorted(["Happy", "Excited"])):
        "Okay mam, aaj toh vibes kaafi achhi hain. Energy high hai aur mood bhi full mast.",
    tuple(sorted(["Happy", "Talkative"])):
        "Madam aaj baat karne ke mood mein lag rahi hain. Social battery bhi theek-thaak hai, so baat kar lo.",
    tuple(sorted(["Happy", "Normal"])):
        "Aaj ka din mam ke liye ekdum theek-thaak, easy-going tarah ka raha.",
    tuple(sorted(["Excited", "Talkative"])):
        "Mam full energy mein hain aur baat karne ka mood bhi hai - abhi disturb karna safe hai.",
    tuple(sorted(["Happy", "Playful"])):
        "Mam thoda playful mood mein lag rahi hain aaj - Maggie ho ya dance, sab ka vibe positive hai.",
    tuple(sorted(["Happy", "Overthinking"])):
        "Upar se sab theek lag raha hai, par dimaag thoda kaam kar raha hai. Overall mood positive hi hai.",
    tuple(sorted(["Tired", "Quiet"])):
        "Aaj mam ki battery thodi low lag rahi hai. Zyada disturb mat karo, pehle recharge hone do.",
    tuple(sorted(["Tired", "Overthinking"])):
        "Body tired hai aur dimaag apni hi meeting chala raha hai. Mam ko thoda peace chahiye lagta hai.",
    tuple(sorted(["Tired", "Needs Space"])):
        "Mam thak gayi hain aaj. Thoda alone time de do, khud recharge ho jayengi.",
    tuple(sorted(["Tired", "Bored"])):
        "Na energy hai na kuch interesting hua - aaj ka din bas flat sa nikal gaya mam ke liye.",
    tuple(sorted(["Low", "Overthinking"])):
        "Dimaag mein thoda zyada traffic chal raha hai aur mood bhi thoda heavy hai. Mam ko space chahiye.",
    tuple(sorted(["Low", "Quiet"])):
        "Aaj mam ka social battery low hai. Thoda space dena better rahega... warna 'kuch nahi hua' wala reply mil sakta hai.",
    tuple(sorted(["Low", "Needs Space"])):
        "Aaj ka din thoda bhaari raha lagta hai mam ke liye. Thodi der akeli chhod do, better feel karengi.",
    tuple(sorted(["Low", "Tired"])):
        "Mam aaj mood se bhi aur energy se bhi thodi down hain. Thoda gentle rehna aaj.",
    tuple(sorted(["Bored", "Irritated"])):
        "Mam aaj clearly bore ho rahi hain aur patience bhi kam hai. Kuch interesting activity ki zarurat hai.",
    tuple(sorted(["Bored", "Tired"])):
        "Kuch khaas hua nahi aaj, aur wahi boring-ness thodi tiring bhi lag rahi hai mam ko.",
    tuple(sorted(["Normal", "Needs Space"])):
        "Kuch seriously wrong nahi lag raha. Bas mam thodi 'apna space chahiye' wale mood mein hain.",
    tuple(sorted(["Normal", "Quiet"])):
        "Ekdum balanced, low-key din raha mam ka - na zyada high na zyada low.",
    tuple(sorted(["Overthinking", "Quiet"])):
        "Bahar se shaant lag rahi hain mam, par dimaag ke andar kaafi kuch chal raha hai.",
    tuple(sorted(["Overthinking", "Needs Space"])):
        "Aaj mam ke dimaag mein kaafi kuch chal raha hai. Thodi saans lene ki space chahiye unhe.",
    tuple(sorted(["Irritated", "Needs Space"])):
        "Aaj mam ka patience thoda test ho raha tha. Thodi der distance rakhna better rahega.",
    tuple(sorted(["Excited", "Playful"])):
        "Mam aaj full masti ke mood mein hain - energy bhi high hai aur mood bhi mast.",
    tuple(sorted(["Talkative", "Playful"])):
        "Mam aaj baatuni aur thodi masti wale mood mein hain - perfect time hai unse chat karne ka.",
}

FALLBACK_MESSAGES = {
    "Happy": "Aaj toh mam ka mood kaafi accha lag raha hai. Smile bhi ki, happy bhi feel kiya... kuch toh hua hai.",
    "Normal": "Kuch khaas high ya low nahi - bas ek average, theek-thaak din raha mam ka.",
    "Talkative": "Madam aaj baat karne ke mood mein lag rahi hain. Social battery bhi theek-thaak hai, so baat kar lo.",
    "Excited": "Mam mein aaj ek achhi si energy dikh rahi hai - kuch toh spark hai.",
    "Tired": "Aaj mam ki battery thodi low lag rahi hai. Zyada disturb mat karo, pehle recharge hone do.",
    "Bored": "Mam aaj clearly bore ho rahi hain. Kuch interesting activity ki zarurat hai.",
    "Overthinking": "Dimaag mein thoda zyada traffic chal raha hai aaj mam ke.",
    "Low": "Lagta hai aaj ka din mam ke favour mein nahi tha. Thoda rest aur thoda acha mood material chahiye.",
    "Irritated": "Aaj mam ko zyada irritate karna safe nahi lag raha. Thoda sambhal ke baat karna.",
    "Quiet": "Aaj mam ka social battery low hai. Thoda space dena better rahega.",
    "Needs Space": "Mam ko aaj thodi apni space chahiye lag rahi hai. Thoda time do unhe.",
    "Playful": "Mam aaj thodi playful, halki-phulki mood mein hain aaj.",
}

# Special-case override: a happy primary mood combined with genuinely low
# overthinking gets its own, more specific line.
HAPPY_LOW_OVERTHINKING_MESSAGE = (
    "Aaj ka din mam ke liye un rare peaceful days mein se hai, jahan dimaag "
    "bhi unnecessary problems nahi bana raha."
)


def build_message(primary, secondary, overthinking_lvl):
    if secondary:
        key = tuple(sorted([primary, secondary]))
        if key in COMBO_MESSAGES:
            return COMBO_MESSAGES[key]

    if primary == "Happy" and overthinking_lvl == "Low":
        return HAPPY_LOW_OVERTHINKING_MESSAGE

    return FALLBACK_MESSAGES.get(primary, "Aaj ka din mam ke liye apni hi tarah ka raha.")


def build_answer_summary(answers):
    """Small human-readable summary of what she picked, e.g. for the result page."""
    summary = []
    for question_id in sorted(answers.keys(), key=lambda qid: int(qid[1:])):
        value = answers[question_id]
        label = QUESTION_LABELS.get(question_id, {}).get(value, str(value))
        summary.append({"question": question_id, "answer": label})
    return summary


def predict_mood(answers):
    """
    Main entry point. answers is a dict of {"q1": 1, ..., "q10": 4}
    (already validated by the route before this is called).
    """
    scores = calculate_scores(answers)
    mood_totals = scores["mood_totals"]

    primary, secondary = determine_primary_secondary(mood_totals)
    energy_lvl = energy_level(scores["energy_score"])
    social_lvl = social_level(scores["social_score"])
    overthinking_lvl = overthinking_level(mood_totals)
    message = build_message(primary, secondary, overthinking_lvl)
    overall = overall_label(primary, energy_lvl)

    return {
        "primaryMood": primary,
        "secondaryMood": secondary,
        "energy": energy_lvl,
        "socialBattery": scores["social_score"],
        "socialLevel": social_lvl,
        "overthinking": overthinking_lvl,
        "message": message,
        "overall": overall,
        "moodBreakdown": mood_totals,
        "answerSummary": build_answer_summary(answers),
    }
