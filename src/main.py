"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs

# Core taste profiles
PROFILES = {
    "High-Energy Pop": {"genre": "pop", "mood": "happy", "energy": 0.9},
    "Chill Lofi": {"genre": "lofi", "mood": "chill", "energy": 0.3},
    "Deep Intense Rock": {"genre": "rock", "mood": "intense", "energy": 0.95},
    # Adversarial / edge-case profiles, meant to try to "trick" the scoring logic
    "Conflicting Signals (metal genre + sad mood)": {
        "genre": "metal",
        "mood": "sad",
        "energy": 0.9,
    },
    "Genre Not In Catalog (opera)": {"genre": "opera", "mood": "happy", "energy": 0.5},
    "Missing Mood Preference": {"genre": "pop", "energy": 0.5},
}


def print_recommendations(name: str, user_prefs: dict, songs: list) -> None:
    recommendations = recommend_songs(user_prefs, songs, k=5)

    print(f"\n=== {name} ===")
    print(f"User profile: {user_prefs}")
    print(f"\nTop {len(recommendations)} recommendations:")
    print("-" * 60)
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"{rank}. {song['title']} ({song['artist']}) - Score: {score:.2f}")
        print(f"   Because: {explanation}")
        print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    for name, user_prefs in PROFILES.items():
        print_recommendations(name, user_prefs, songs)


if __name__ == "__main__":
    main()
