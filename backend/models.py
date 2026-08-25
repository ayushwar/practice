from datetime import datetime

from database import db


class MoodResult(db.Model):
    """
    Stores only the mood result itself - no names, no contact info, no
    identifying details, and no free-text answers. Just enough to see
    mood history/trends later if you ever want to build that feature.
    """

    __tablename__ = "mood_results"

    id = db.Column(db.Integer, primary_key=True)
    primary_mood = db.Column(db.String(50), nullable=False)
    secondary_mood = db.Column(db.String(50), nullable=True)
    energy = db.Column(db.String(20), nullable=False)
    social_battery = db.Column(db.Integer, nullable=False)
    social_level = db.Column(db.String(20), nullable=False)
    overthinking = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "primaryMood": self.primary_mood,
            "secondaryMood": self.secondary_mood,
            "energy": self.energy,
            "socialBattery": self.social_battery,
            "socialLevel": self.social_level,
            "overthinking": self.overthinking,
            "createdAt": self.created_at.isoformat() if self.created_at else None,
        }
