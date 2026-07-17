import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

def _user_prefs_from_profile(user: "UserProfile") -> Dict:
    """Adapt a UserProfile dataclass into the user_prefs dict shape score_song() expects."""
    return {
        "genre": user.favorite_genre,
        "mood": user.favorite_mood,
        "energy": user.target_energy,
    }

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        user_prefs = _user_prefs_from_profile(user)
        scored = [(song, score_song(user_prefs, asdict(song))[0]) for song in self.songs]
        ranked = sorted(scored, key=lambda item: item[1], reverse=True)
        return [song for song, _ in ranked[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        user_prefs = _user_prefs_from_profile(user)
        _, reasons = score_song(user_prefs, asdict(song))
        return ", ".join(reasons) if reasons else "no strong matches"

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file into a list of dicts, converting numeric fields to float/int."""
    numeric_fields = ("energy", "tempo_bpm", "valence", "danceability", "acousticness")

    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"] = int(row["id"])
            for field in numeric_fields:
                row[field] = float(row[field])
            songs.append(row)

    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a song against user preferences using the Phase 2 algorithm recipe (genre, mood, energy)."""
    score = 0.0
    reasons = []

    # +2.0 for a genre match
    if song["genre"] == user_prefs.get("genre"):
        score += 2.0
        reasons.append(f"matches your favorite genre ({song['genre']}) (+2.0)")

    # +1.0 for a mood match
    if song["mood"] == user_prefs.get("mood"):
        score += 1.0
        reasons.append(f"matches your preferred mood ({song['mood']}) (+1.0)")

    # up to +2.0 for energy closeness: 2.0 * (1 - |song.energy - target_energy|)
    target_energy = user_prefs.get("energy")
    if target_energy is not None:
        energy_points = 2.0 * (1 - abs(song["energy"] - target_energy))
        score += energy_points
        reasons.append(
            f"energy ({song['energy']:.2f}) is close to your target "
            f"of {target_energy:.2f} (+{energy_points:.2f})"
        )

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song against user preferences and return the top k, ranked highest to lowest."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = ", ".join(reasons) if reasons else "no strong matches"
        scored.append((song, score, explanation))

    ranked = sorted(scored, key=lambda item: item[1], reverse=True)
    return ranked[:k]
