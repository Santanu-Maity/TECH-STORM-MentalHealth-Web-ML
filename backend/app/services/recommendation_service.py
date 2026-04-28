"""
recommendation_service.py
Returns personalised wellness content based on mental health score and mood.
"""
import random
from typing import Dict, Any, Optional


# ─── Motivational Quotes ────────────────────────────────────────────────────

QUOTES = {
    "low_score": [
        {"text": "You don't have to be positive all the time. It's perfectly okay to feel sad, angry, annoyed, frustrated, scared and anxious.", "author": "Lori Deschene"},
        {"text": "There is hope, even when your brain tells you there isn't.", "author": "John Green"},
        {"text": "Sometimes the people around you won't understand your journey. They don't need to, it's not for them.", "author": "Joubert Botha"},
    ],
    "moderate": [
        {"text": "You are stronger than you think.", "author": "A.A. Milne"},
        {"text": "Mental health is not a destination, but a process. It's about how you drive, not where you're going.", "author": "Noam Shpancer"},
        {"text": "Take it one day at a time.", "author": "Unknown"},
    ],
    "high_score": [
        {"text": "The mind is everything. What you think you become.", "author": "Buddha"},
        {"text": "Self-care is not self-indulgence, it is self-preservation.", "author": "Audre Lorde"},
        {"text": "You are enough, just as you are.", "author": "Meghan Markle"},
    ],
    "neutral": [
        {"text": "Every day is a new beginning.", "author": "Unknown"},
        {"text": "Be gentle with yourself.", "author": "Unknown"},
    ],
}

# ─── Yoga & Exercise ────────────────────────────────────────────────────────

YOGA_EXERCISES = {
    "beginner": [
        {"name": "Child's Pose (Balasana)", "duration_minutes": 5, "description": "A gentle resting pose that calms the mind.", "benefits": "Reduces anxiety, relieves back tension"},
        {"name": "Cat-Cow Stretch", "duration_minutes": 5, "description": "Synchronize breath with movement to release tension.", "benefits": "Reduces stress, improves focus"},
        {"name": "Legs Up The Wall (Viparita Karani)", "duration_minutes": 10, "description": "Restorative inversion to calm the nervous system.", "benefits": "Reduces anxiety, improves sleep"},
        {"name": "Corpse Pose (Savasana)", "duration_minutes": 10, "description": "Total relaxation pose.", "benefits": "Reduces stress, promotes mindfulness"},
    ],
    "intermediate": [
        {"name": "Warrior I & II", "duration_minutes": 10, "description": "Standing poses building strength and confidence.", "benefits": "Boosts self-esteem, reduces anxiety"},
        {"name": "Downward Dog", "duration_minutes": 5, "description": "Full-body stretch energising pose.", "benefits": "Reduces fatigue, relieves depression"},
        {"name": "Seated Forward Bend (Paschimottanasana)", "duration_minutes": 5, "description": "Calming forward fold.", "benefits": "Reduces anxiety, calms the mind"},
    ],
    "advanced": [
        {"name": "Tree Pose (Vrikshasana)", "duration_minutes": 10, "description": "Balance pose promoting focus.", "benefits": "Improves concentration, stability"},
        {"name": "Headstand (Sirsasana)", "duration_minutes": 5, "description": "King of asanas — improves blood flow to the brain.", "benefits": "Reduces anxiety, boosts mood"},
    ],
}

# ─── Music ──────────────────────────────────────────────────────────────────

MUSIC_RECS = {
    "calm": [
        {"title": "Weightless", "artist": "Marconi Union", "genre": "Ambient", "mood": "Relaxing", "spotify_search": "Weightless Marconi Union"},
        {"title": "Clair de Lune", "artist": "Claude Debussy", "genre": "Classical", "mood": "Peaceful", "spotify_search": "Clair de Lune Debussy"},
        {"title": "Holocene", "artist": "Bon Iver", "genre": "Indie Folk", "mood": "Reflective", "spotify_search": "Holocene Bon Iver"},
    ],
    "uplifting": [
        {"title": "Here Comes The Sun", "artist": "The Beatles", "genre": "Rock", "mood": "Happy", "spotify_search": "Here Comes The Sun Beatles"},
        {"title": "Walking on Sunshine", "artist": "Katrina and the Waves", "genre": "Pop", "mood": "Energetic", "spotify_search": "Walking on Sunshine Katrina"},
        {"title": "Happy", "artist": "Pharrell Williams", "genre": "Pop", "mood": "Joyful", "spotify_search": "Happy Pharrell Williams"},
    ],
    "focus": [
        {"title": "Experience", "artist": "Ludovico Einaudi", "genre": "Classical", "mood": "Focused", "spotify_search": "Experience Einaudi"},
        {"title": "Time", "artist": "Hans Zimmer", "genre": "Soundtrack", "mood": "Inspired", "spotify_search": "Time Hans Zimmer Inception"},
    ],
    "energetic": [
        {"title": "Eye of the Tiger", "artist": "Survivor", "genre": "Rock", "mood": "Motivated", "spotify_search": "Eye of the Tiger Survivor"},
        {"title": "Stronger", "artist": "Kanye West", "genre": "Hip-Hop", "mood": "Confident", "spotify_search": "Stronger Kanye West"},
    ],
}

# ─── Movies ─────────────────────────────────────────────────────────────────

MOVIE_RECS = {
    "uplifting": [
        {"title": "The Pursuit of Happyness", "year": 2006, "genre": "Drama", "description": "A story of resilience and hope."},
        {"title": "Soul", "year": 2020, "genre": "Animation", "description": "Explores the meaning of life with warmth."},
        {"title": "Good Will Hunting", "year": 1997, "genre": "Drama", "description": "Healing through human connection."},
    ],
    "comedy": [
        {"title": "Yes Man", "year": 2008, "genre": "Comedy", "description": "Saying yes to life's possibilities."},
        {"title": "Hera Pheri", "year": 2000, "genre": "Bollywood Comedy", "description": "Classic Bollywood laughter therapy."},
    ],
    "inspirational": [
        {"title": "A Beautiful Mind", "year": 2001, "genre": "Biographical Drama", "description": "Triumph over mental illness."},
        {"title": "Silver Linings Playbook", "year": 2012, "genre": "Drama/Comedy", "description": "Finding joy through mental health struggles."},
        {"title": "3 Idiots", "year": 2009, "genre": "Bollywood", "description": "Rethinking success and happiness."},
    ],
}

# ─── Meditation ─────────────────────────────────────────────────────────────

MEDITATION_GUIDES = [
    {"name": "4-7-8 Breathing", "duration_minutes": 5, "steps": ["Inhale for 4 counts", "Hold for 7 counts", "Exhale for 8 counts", "Repeat 4 times"], "benefits": "Reduces anxiety quickly"},
    {"name": "Body Scan Meditation", "duration_minutes": 10, "steps": ["Lie down comfortably", "Focus attention from feet upward", "Notice sensations without judgement", "Release tension with each exhale"], "benefits": "Reduces physical stress"},
    {"name": "Loving-Kindness Meditation", "duration_minutes": 15, "steps": ["Sit comfortably", "Silently repeat: May I be happy. May I be healthy. May I be at peace.", "Extend these wishes to loved ones, then all beings"], "benefits": "Improves compassion and mood"},
    {"name": "5-Minute Mindfulness", "duration_minutes": 5, "steps": ["Close your eyes", "Focus only on your breath", "When mind wanders, gently return to breath", "Continue for 5 minutes"], "benefits": "Immediate calm"},
]

# ─── Coping Strategies ───────────────────────────────────────────────────────

COPING_STRATEGIES = {
    "critical": [
        "Reach out to a trusted person right now — you don't have to face this alone.",
        "Call a mental health helpline immediately (see Emergency Resources).",
        "Ground yourself: name 5 things you can see, 4 you can touch, 3 you can hear.",
        "Remove yourself from any harmful environment and go to a safe place.",
    ],
    "high": [
        "Talk to a therapist or counsellor this week.",
        "Practice daily journaling — even 5 minutes helps.",
        "Limit social media; take a 24-hour digital detox.",
        "Try 10 minutes of gentle yoga or stretching each morning.",
        "Ensure at least 7-8 hours of sleep per night.",
    ],
    "moderate": [
        "Maintain a consistent sleep schedule.",
        "Add 20-30 minutes of walking to your daily routine.",
        "Practice gratitude: write 3 things you're grateful for each day.",
        "Connect with a friend or family member today.",
        "Try a new hobby to stimulate positive emotions.",
    ],
    "low": [
        "Continue your current healthy habits!",
        "Share your wellness strategies with someone who might benefit.",
        "Set new personal growth goals.",
        "Practice mindfulness meditation to maintain balance.",
    ],
}

# ─── Lifestyle Tips ──────────────────────────────────────────────────────────

LIFESTYLE_TIPS = {
    "sleep": ["Maintain a consistent bed/wake time", "Avoid screens 1 hour before sleep", "Keep your bedroom cool and dark", "Avoid caffeine after 2 PM"],
    "diet": ["Eat Omega-3 rich foods (fish, flaxseed)", "Stay hydrated — 8 glasses of water daily", "Limit sugar and ultra-processed foods", "Include probiotics (curd, yoghurt) for gut-brain health"],
    "exercise": ["Aim for 30 minutes of moderate exercise daily", "Even a 10-minute walk improves mood", "Try swimming or dancing — joyful movement matters", "Strength training 2-3x per week boosts confidence"],
    "social": ["Schedule one social activity per week", "Volunteer for a cause you care about", "Join a support group or community", "Limit toxic relationships where possible"],
}


# ─── Main Function ──────────────────────────────────────────────────────────

def get_personalized_recommendations(score: float, risk_level: str, mood_log=None) -> Dict[str, Any]:
    quote_pool = QUOTES["low_score"] if score < 40 else QUOTES["moderate"] if score < 70 else QUOTES["high_score"]

    yoga_level = "beginner" if score < 50 else "intermediate"
    music_mood = "calm" if score < 40 else "uplifting" if score < 70 else "energetic"
    movie_mood = "uplifting" if score < 60 else "inspirational"

    # Pick meditation guides by duration preference
    guides = sorted(MEDITATION_GUIDES, key=lambda x: x["duration_minutes"])

    return {
        "score": score,
        "risk_level": risk_level,
        "quote": random.choice(quote_pool),
        "coping_strategies": COPING_STRATEGIES.get(risk_level, COPING_STRATEGIES["moderate"]),
        "yoga_exercises": YOGA_EXERCISES.get(yoga_level, YOGA_EXERCISES["beginner"]),
        "music": MUSIC_RECS.get(music_mood, MUSIC_RECS["calm"]),
        "movies": MOVIE_RECS.get(movie_mood, MOVIE_RECS["uplifting"]),
        "meditation": guides[:2],
        "lifestyle_tips": {
            "sleep": LIFESTYLE_TIPS["sleep"],
            "diet": LIFESTYLE_TIPS["diet"][:2],
            "exercise": LIFESTYLE_TIPS["exercise"][:2],
            "social": LIFESTYLE_TIPS["social"][:2],
        },
    }


def get_motivational_quotes(mood: str) -> list:
    return QUOTES.get(mood, QUOTES["neutral"])


def get_yoga_exercises(level: str) -> list:
    return YOGA_EXERCISES.get(level, YOGA_EXERCISES["beginner"])


def get_music_recommendations(mood: str) -> list:
    return MUSIC_RECS.get(mood, MUSIC_RECS["calm"])


def get_movie_recommendations(mood: str) -> list:
    return MOVIE_RECS.get(mood, MOVIE_RECS["uplifting"])


def get_meditation_guides(duration_minutes: int) -> list:
    return [g for g in MEDITATION_GUIDES if g["duration_minutes"] <= duration_minutes] or MEDITATION_GUIDES[:1]
