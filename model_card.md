# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeCheck 1.0**

---

## 2. Intended Use  

VibeCheck takes one listener's stated taste (a favorite genre, a favorite mood, and a target energy level) and suggests the 5 best-matching songs from a small 18-song catalog, along with a plain-English reason for each pick. It assumes the listener already knows and honestly reports their own taste — it does not learn from listening history or behavior over time, and it assumes that one fixed "target" can represent a person's whole taste at once.

This is a **classroom exploration project**, not a production system. It's meant to demonstrate how content-based filtering and weighted scoring work, not to actually recommend music to real users at scale.

**Intended use:** learning and demonstrating how a simple content-based recommender turns song attributes and user preferences into a ranked, explained list.

**Not intended for:** recommending music to real listeners in production, replacing a real streaming platform's recommender, making decisions about what music gets promoted or hidden, or any use where fairness/bias guarantees matter — the tiny hand-built catalog and single-profile design make it unsuitable for anything beyond a learning demo.

---

## 3. How the Model Works  

Every song has two kinds of labels: describing tags like genre and mood, and number "dials" like energy (how intense it feels, from 0 to 1). A listener's taste profile is just three things: a favorite genre, a favorite mood, and a target energy level.

To score a song, VibeCheck checks three things and adds up points:
- Does the genre match? If yes, +2 points.
- Does the mood match? If yes, +1 point.
- How close is the song's energy to the target? The closer it is, the more points it earns, up to +2.

It does this for every song in the catalog, adds up the points into one total score per song, sorts all the songs from highest score to lowest, and hands back the top 5 — each with a plain-language reason showing exactly which parts matched.

Compared to the starter file (which was just empty placeholders), the real changes were: actually loading and converting the CSV data, scoring energy by "how close" instead of "how high," and turning the scoring reasons into full sentences instead of raw labels.

---

## 4. Data  

The catalog is `data/songs.csv`: 18 songs total. It started as 10 songs across 7 genres, and I added 8 more songs (Phase 2) to cover genres and moods that weren't there yet — hip-hop, classical, folk, r&b, metal, country, house, and reggae — bringing it to 15 genres and 14 moods total.

Each song has 7 features: `genre`, `mood`, `energy`, `tempo_bpm`, `valence`, `danceability`, and `acousticness`. All the numeric values were made up by hand (or by me and AI) to feel plausible — none of it comes from real audio analysis.

What's missing: most genres only have 1 song, so a "genre match" is really just matching to one specific track's other traits, not a genre's typical range. Energy values only span 0.28 to 0.97, so nobody who wants something super chill (near 0) or super intense (near 1) is well represented. There's also nothing about lyrics, language, era/decade, or real listening behavior — this dataset only captures a narrow slice of what "musical taste" actually means.

---

## 5. Strengths  

For the three "core" profiles I tested (High-Energy Pop, Chill Lofi, Deep Intense Rock), the #1 recommendation always matched genre, mood, *and* energy — exactly what I'd expect a good recommendation to look like, and it matched my own intuition every time.

The system also correctly tells opposite tastes apart: Chill Lofi and Deep Intense Rock shared zero songs in their top 5 lists, which shows the scoring logic isn't just returning the same "popular" songs no matter who's asking, at least when tastes are far apart.

It's also honest about *why* it recommended something — every result comes with a plain-language reason showing exactly which parts matched, instead of a mystery number. And it doesn't crash on weird input: an unknown genre, an unmatched mood, or a missing preference all degrade gracefully instead of throwing an error.

---

## 6. Limitations and Bias 

The clearest weakness I found came from the Phase 4 experiments: a small handful of "generalist" songs (especially **Sunrise City** and **Gym Hero**, both mid-to-high energy pop tracks) appeared in the top 5 for 5 of the 6 test profiles I ran, including profiles with completely different target genres and moods. This happens because `energy` closeness is weighted as strongly as a genre match (both max out at 2.0 points), so a song whose energy happens to sit near the "typical" value tested (0.8–0.95) can ride energy similarity alone into the top 5 of almost any high-energy-seeking profile, genre or mood match or not. I confirmed this wasn't just a weighting-ratio problem: in Step 3 I halved the genre weight and doubled the energy weight, and the same songs still dominated — they just won for a different reason. With only 18 songs and most genres represented by a single track, the catalog is simply too small to offer a close alternative, so a couple of "safe, central" songs end up over-recommended across very different listeners rather than each user getting a genuinely distinct list.

---

## 7. Evaluation  

I tested the recommender (`python -m src.main`) against six profiles: three "core" taste profiles and three adversarial/edge-case profiles designed to try to break or confuse the scoring logic.

### Core profiles

```
=== High-Energy Pop ===
User profile: {'genre': 'pop', 'mood': 'happy', 'energy': 0.9}

Top 5 recommendations:
------------------------------------------------------------
1. Sunrise City (Neon Echo) - Score: 4.84
   Because: matches your favorite genre (pop) (+2.0), matches your preferred mood (happy) (+1.0), energy (0.82) is close to your target of 0.90 (+1.84)

2. Gym Hero (Max Pulse) - Score: 3.94
   Because: matches your favorite genre (pop) (+2.0), energy (0.93) is close to your target of 0.90 (+1.94)

3. Rooftop Lights (Indigo Parade) - Score: 2.72
   Because: matches your preferred mood (happy) (+1.0), energy (0.76) is close to your target of 0.90 (+1.72)

4. Storm Runner (Voltline) - Score: 1.98
   Because: energy (0.91) is close to your target of 0.90 (+1.98)

5. Neon Tide (DJ Halcyon) - Score: 1.96
   Because: energy (0.88) is close to your target of 0.90 (+1.96)
```

```
=== Chill Lofi ===
User profile: {'genre': 'lofi', 'mood': 'chill', 'energy': 0.3}

Top 5 recommendations:
------------------------------------------------------------
1. Library Rain (Paper Lanterns) - Score: 4.90
   Because: matches your favorite genre (lofi) (+2.0), matches your preferred mood (chill) (+1.0), energy (0.35) is close to your target of 0.30 (+1.90)

2. Midnight Coding (LoRoom) - Score: 4.76
   Because: matches your favorite genre (lofi) (+2.0), matches your preferred mood (chill) (+1.0), energy (0.42) is close to your target of 0.30 (+1.76)

3. Focus Flow (LoRoom) - Score: 3.80
   Because: matches your favorite genre (lofi) (+2.0), energy (0.40) is close to your target of 0.30 (+1.80)

4. Spacewalk Thoughts (Orbit Bloom) - Score: 2.96
   Because: matches your preferred mood (chill) (+1.0), energy (0.28) is close to your target of 0.30 (+1.96)

5. Autumn Sonata (Elena Voss) - Score: 2.00
   Because: energy (0.30) is close to your target of 0.30 (+2.00)
```

```
=== Deep Intense Rock ===
User profile: {'genre': 'rock', 'mood': 'intense', 'energy': 0.95}

Top 5 recommendations:
------------------------------------------------------------
1. Storm Runner (Voltline) - Score: 4.92
   Because: matches your favorite genre (rock) (+2.0), matches your preferred mood (intense) (+1.0), energy (0.91) is close to your target of 0.95 (+1.92)

2. Gym Hero (Max Pulse) - Score: 2.96
   Because: matches your preferred mood (intense) (+1.0), energy (0.93) is close to your target of 0.95 (+1.96)

3. Iron Collapse (Grave Circuit) - Score: 1.96
   Because: energy (0.97) is close to your target of 0.95 (+1.96)

4. Neon Tide (DJ Halcyon) - Score: 1.86
   Because: energy (0.88) is close to your target of 0.95 (+1.86)

5. Sunrise City (Neon Echo) - Score: 1.74
   Because: energy (0.82) is close to your target of 0.95 (+1.74)
```

All three core profiles put the "obvious" best-matching song in first place (exact genre + mood + closest energy), which is what I looked for and expected.

### Adversarial / edge-case profiles

```
=== Conflicting Signals (metal genre + sad mood) ===
User profile: {'genre': 'metal', 'mood': 'sad', 'energy': 0.9}

Top 5 recommendations:
------------------------------------------------------------
1. Iron Collapse (Grave Circuit) - Score: 3.86
   Because: matches your favorite genre (metal) (+2.0), energy (0.97) is close to your target of 0.90 (+1.86)

2. Storm Runner (Voltline) - Score: 1.98
   Because: energy (0.91) is close to your target of 0.90 (+1.98)

3. Neon Tide (DJ Halcyon) - Score: 1.96
   Because: energy (0.88) is close to your target of 0.90 (+1.96)

4. Gym Hero (Max Pulse) - Score: 1.94
   Because: energy (0.93) is close to your target of 0.90 (+1.94)

5. Sunrise City (Neon Echo) - Score: 1.84
   Because: energy (0.82) is close to your target of 0.90 (+1.84)
```

```
=== Genre Not In Catalog (opera) ===
User profile: {'genre': 'opera', 'mood': 'happy', 'energy': 0.5}

Top 5 recommendations:
------------------------------------------------------------
1. Rooftop Lights (Indigo Parade) - Score: 2.48
   Because: matches your preferred mood (happy) (+1.0), energy (0.76) is close to your target of 0.50 (+1.48)

2. Sunrise City (Neon Echo) - Score: 2.36
   Because: matches your preferred mood (happy) (+1.0), energy (0.82) is close to your target of 0.50 (+1.36)

3. Velvet Hours (Marlow James) - Score: 2.00
   Because: energy (0.50) is close to your target of 0.50 (+2.00)

4. Dust Road Home (Wren & Compass) - Score: 1.90
   Because: energy (0.45) is close to your target of 0.50 (+1.90)

5. Island Drift (Solar Bay) - Score: 1.90
   Because: energy (0.55) is close to your target of 0.50 (+1.90)
```

```
=== Missing Mood Preference ===
User profile: {'genre': 'pop', 'energy': 0.5}

Top 5 recommendations:
------------------------------------------------------------
1. Sunrise City (Neon Echo) - Score: 3.36
   Because: matches your favorite genre (pop) (+2.0), energy (0.82) is close to your target of 0.50 (+1.36)

2. Gym Hero (Max Pulse) - Score: 3.14
   Because: matches your favorite genre (pop) (+2.0), energy (0.93) is close to your target of 0.50 (+1.14)

3. Velvet Hours (Marlow James) - Score: 2.00
   Because: energy (0.50) is close to your target of 0.50 (+2.00)

4. Dust Road Home (Wren & Compass) - Score: 1.90
   Because: energy (0.45) is close to your target of 0.50 (+1.90)

5. Island Drift (Solar Bay) - Score: 1.90
   Because: energy (0.55) is close to your target of 0.50 (+1.90)
```

### What surprised me

- **The "conflicting signals" profile didn't break anything, but it did reveal a real gap:** `mood: "sad"` never matches any song, because no song in the catalog actually has the mood label "sad" (the closest is "melancholic"). The system doesn't error or warn about this — it just quietly scores every song's mood component as 0 and falls back to genre + energy. A user profile with a typo'd or unsupported mood value is silently treated the same as "no mood preference at all," which could be confusing since nothing signals that the mood was ignored.
- **An unknown genre ("opera") behaves the same way** — genre_pts is 0 for every song, and ranking collapses to mood + energy only. Again, no error, just silent degradation to a smaller feature set.
- **A missing key (`mood` left out entirely) behaves identically to an unmatched mood value** — `user_prefs.get("mood")` returns `None`, which never equals a song's mood string, so it degrades gracefully rather than crashing. This was reassuring: the scoring function is robust to incomplete profiles without needing extra validation code.
- Across all three "broken" profiles, the recommender never crashed and always returned a plausibly-ranked top 5 — but it also never tells the user "your genre/mood preference didn't match anything," which is worth noting as a limitation (see Section 6).

### Comparing profiles side-by-side

- **High-Energy Pop vs. Chill Lofi:** these two share zero songs in their top 5. That makes total sense — their energy targets (0.9 vs. 0.3) are almost as far apart as the scale allows, so nothing that scores well for one can score well for the other. This is the system working correctly: truly opposite tastes get truly different lists.
- **Chill Lofi vs. Deep Intense Rock:** again, no overlap at all. Same reasoning as above, but even more extreme since genre, mood, *and* energy target are all different. This is the clearest "did the system actually separate these users" sanity check, and it passes.
- **High-Energy Pop vs. Deep Intense Rock:** these *do* overlap — Gym Hero, Neon Tide, and Sunrise City show up in both top 5s, even though one wants pop/happy and the other wants rock/intense. Why? Both profiles target roughly the same high energy zone (0.9 and 0.95), so once the #1 spot is claimed by the genre-correct pick (Sunrise City for pop, Storm Runner for rock), the rest of each list fills in with "generically high-energy" songs regardless of genre. This is the generalist-song problem from Section 6 showing up directly in a comparison.
- **High-Energy Pop vs. Conflicting Signals (metal + sad, energy 0.9):** despite having a completely different genre and a mood (`sad`) that doesn't exist anywhere in the catalog, 4 of the 5 songs recommended (Storm Runner, Neon Tide, Gym Hero, Sunrise City) are the *same* as High-Energy Pop's list. Once genre and mood stop contributing (because "metal"+"sad" barely match anything besides one song), energy alone drives the ranking — and since both profiles want ~0.9 energy, they converge on nearly the same songs.
- **Genre Not In Catalog (opera) vs. Missing Mood Preference:** both target energy 0.5, and their outputs are nearly identical (3 of 5 songs match). This reveals something important: asking for a genre that doesn't exist ("opera") behaves *exactly* the same as asking for no genre at all, because both score 0 genre points for every song. The system can't tell the difference between "user wants something we don't have" and "user has no genre preference" — they collapse to the same behavior.
- **High-Energy Pop vs. Missing Mood Preference:** both target the pop genre, so Sunrise City and Gym Hero stay on top in both cases — but Missing Mood's lower energy target (0.5 vs. 0.9) pulls in three new songs (Velvet Hours, Dust Road Home, Island Drift) that weren't relevant at all to the high-energy version. This is a good sign: energy target changes are having the expected effect even when genre is held constant.

### Explaining a specific case, in plain language: why does "Gym Hero" keep showing up for people who just want "Happy Pop"?

Imagine grading a quiz where you get partial credit for each answer you get right, and the answers don't have to *all* be correct to still pass. Gym Hero is a pop song (correct!) with very high energy (also correct, if the listener wants an energetic vibe!) — but its actual mood label is "intense," not "happy." A listener who explicitly said "I want happy pop" doesn't get the "happy" part from this song at all.

But because the system just *adds up* points for whatever matches — genre points, plus mood points, plus energy points — Gym Hero still racks up a high total score from genre + energy alone, even with zero credit for mood. It's like a student who skips the essay question but aces the multiple choice — they can still end up with a solid grade overall, even though they clearly didn't answer everything the assignment asked for. That's exactly why Gym Hero keeps appearing near the top for "happy pop" listeners: it's a strong partial match being scored as if partial credit were nearly as good as a full match.

---

## 8. Future Work  

1. **Grow the catalog** so each genre has several songs instead of just one or two. This would directly fix the "generalist song domination" problem from Section 6 by giving close alternatives instead of one song winning by default.
2. **Let a user profile hold more than one taste at once** — like a couple of favorite genres/moods, or "sometimes chill, sometimes intense" — instead of forcing every listener into a single fixed point. This addresses the single-taste bias from Phase 2.
3. **Add a message when nothing really matched** — right now, asking for a genre or mood that isn't in the catalog silently falls back to scoring on energy alone, with no signal to the user that their real preference wasn't found. A simple "no strong genre/mood match — showing closest energy matches instead" note would make the system a lot more honest about its own limits.

---

## 9. Personal Reflection  

My biggest learning moment was the Phase 4 weight experiment. Halving the genre weight and doubling the energy weight sounds like a small tweak, but watching a completely irrelevant song (an R&B track, Velvet Hours) jump ahead of a song that actually matched the user's mood — just because its energy number happened to land closer to the target — made "weights" stop being an abstract design choice. It became a real, visible bug I could point at.

AI helped me move fast without getting stuck on setup details — catching, for example, that the starter code's import in `main.py` would crash under the documented run command, and fixing it before I even had to debug it myself. But I made sure to double-check the things that mattered to my own judgment: when the scoring reasons came back, I didn't just accept "friendly" or "shows the math" as an either/or choice — I pushed for both, since I wanted the explanation to stay honest about what the score was actually based on.

What surprised me most is how much a simple algorithm can still *feel* like a real recommendation. The three core profiles I tested (High-Energy Pop, Chill Lofi, Deep Intense Rock) all returned a top pick that matched my own gut instinct, using nothing more than a genre check, a mood check, and one distance formula. I expected "real" recommendations to require something a lot more complex to feel right.

It also changed how I think about bias in real recommender apps. With only 18 songs, it was easy to catch a couple of "generalist" songs getting over-recommended across very different tastes, purely because the catalog didn't have anything closer. Real platforms have way more songs, so this same failure mode is probably still happening — it's just invisible at that scale, instead of showing up in 5 out of 6 test profiles like it did here.

If I kept building this, I'd want a bigger catalog first, since that fixes the "generalist song" problem directly, and then a way for one user profile to hold more than one taste at once, since real listeners don't have just one mood.
