# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Real platforms like Spotify or YouTube combine two approaches: **collaborative filtering**, which looks at patterns across many users' listening behavior ("people who liked what you liked also liked..."), and **content-based filtering**, which looks at the attributes of the songs themselves (tempo, energy, mood, genre) and matches them to what a listener already engages with. At scale, these are blended into a hybrid system that also factors in context like time of day or session behavior. Because this simulation works with a single small song catalog and no real cross-user history, my version focuses entirely on **content-based filtering**: each song is represented as a set of attributes, each user is represented as a preference profile over those same attributes, and the recommender scores songs by how *close* their attributes are to the user's stated preferences, rather than just favoring high values. Different features are weighted differently, for example, a genre match counts for more than a mood match, and the resulting scores are used to rank the full song list into a top-N recommendation.

**`Song` features** (from `data/songs.csv`, 18 songs total):
- `genre` — categorical style (pop, lofi, rock, ambient, jazz, synthwave, indie pop, hip-hop, classical, folk, r&b, metal, country, house, reggae)
- `mood` — descriptive label (happy, chill, intense, relaxed, moody, focused, confident, melancholic, nostalgic, romantic, angry, peaceful, euphoric, playful)
- `energy` — numeric, 0 to 1
- `tempo_bpm` — numeric tempo in beats per minute
- `valence` — numeric mood positivity, 0 to 1
- `danceability` — numeric, 0 to 1
- `acousticness` — numeric, 0 to 1

**`UserProfile` stores:**
- a preferred `genre` (and optionally a preferred `mood`)
- target values for the numeric features: `energy`, `valence`, `danceability`, `tempo_bpm`
- a weight for each feature, reflecting how much it should count toward the final score (e.g., genre weighted higher than mood)

Example profile used to design and test the scoring logic:

```python
user_profile = {
    "favorite_genre": "rock",
    "favorite_mood": "intense",
    "target_energy": 0.85,
    "target_valence": 0.55,
    "target_danceability": 0.65,
    "target_tempo_bpm": 140,
}
```

### Data Flow

```mermaid
flowchart LR
    A[UserProfile
    favorite_genre, favorite_mood,
    target_energy, weights] --> B

    subgraph B [Loop: score every song in songs.csv]
        direction TB
        B1[Read one Song row] --> B2{genre match?}
        B2 -->|yes +2.0| B3
        B2 -->|no +0| B3
        B3{mood match?}
        B3 -->|yes +1.0| B4
        B3 -->|no +0| B4
        B4[energy similarity
        2.0 * 1 - |song.energy - target_energy|] --> B5[sum → song.score]
    end

    B --> C[Collect all scored songs]
    C --> D[Sort descending by score]
    D --> E[Take Top K]
    E --> F[Output: Ranked Recommendations]
```

### Algorithm Recipe (Finalized)

```
score(song, user) =
      2.0  if song.genre == user.favorite_genre else 0.0
    + 1.0  if song.mood  == user.favorite_mood  else 0.0
    + 2.0 * (1 - |song.energy - user.target_energy|)
```

1. For each numeric feature, compute closeness: `score = 1 - |song_value - user_target|`, so songs *closer* to the user's target score higher, not just songs with high raw values.
2. For categorical features (genre, mood), score a fixed number of points for an exact match, 0 otherwise. Genre (2.0) is weighted 2x mood (1.0), since genre defines the broad "sound world" a listener wants while mood is a finer emotional shading within it.
3. Sum the weighted terms into a single total score per song.
4. Score every song in the catalog this way, sort descending, and return the top K as the recommendation list.

### Potential Biases

- **Genre-dominance bias:** because genre and mood are additive rather than a strict filter, songs can still rank reasonably well purely on a strong energy match even if the genre is wrong — but in practice the 2.0-point genre weight means the system will generally over-prioritize genre matches, potentially burying a great mood/energy match from a genre the user didn't explicitly list as a favorite.
- **Single-taste bias:** the `UserProfile` represents one fixed point in feature-space, so it can't represent a listener with genuinely split tastes (e.g., someone who loves both intense rock and chill lofi depending on the day). Averaging those tastes into one profile would produce a "compromise" target that matches neither well.
- **Catalog bias:** with only 18 songs across 15 genres, most genres have just one representative track, so a genre match is really just matching to one specific song's other attributes rather than a genre's typical range — a much larger catalog would behave differently.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Output of `python -m src.main` using the default `pop` / `happy` / `energy=0.8` profile:

```
Loaded songs: 18

User profile: genre=pop, mood=happy, energy=0.8

Top 5 recommendations:
------------------------------------------------------------
1. Sunrise City (Neon Echo) - Score: 4.96
   Because: matches your favorite genre (pop) (+2.0), matches your preferred mood (happy) (+1.0), energy (0.82) is close to your target of 0.80 (+1.96)

2. Gym Hero (Max Pulse) - Score: 3.74
   Because: matches your favorite genre (pop) (+2.0), energy (0.93) is close to your target of 0.80 (+1.74)

3. Rooftop Lights (Indigo Parade) - Score: 2.92
   Because: matches your preferred mood (happy) (+1.0), energy (0.76) is close to your target of 0.80 (+1.92)

4. Night Drive Loop (Neon Echo) - Score: 1.90
   Because: energy (0.75) is close to your target of 0.80 (+1.90)

5. Neon Tide (DJ Halcyon) - Score: 1.84
   Because: energy (0.88) is close to your target of 0.80 (+1.84)
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



