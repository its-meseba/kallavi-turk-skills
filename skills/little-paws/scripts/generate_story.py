#!/usr/bin/env python3
"""
Little Paws Daily Story Generator - Updated with close-up shots and accurate characters
"""

import os
import json
from datetime import datetime
from pathlib import Path

SKILL_DIR = Path("/root/.openclaw/workspace/kallavi-turk-skills/skills/little-paws")
OUTPUT_DIR = SKILL_DIR / "output"

# IMPROVED CHARACTER PROMPT - based on user's reference image
CHARACTER_PROMPT = """TWO chibi-style white cats in kawaii cartoon style.

MALE CHARACTER (bigger, left):
- Slightly broader face, bulkier body, larger head
- Large circular dark brown/black eyes with ONE white highlight (small round dot)
- Dark thick collar with LARGE ROUND PENDANT (~25% head width, blue/teal)
- Sometimes half-lidded or mischievous eyes
- Short fur tufts around cheeks, chest, tail
- Small dark speckle/freckle marks on face

FEMALE CHARACTER (smaller, right):
- Rounder, slightly smaller head and body, softer facial features
- Large emerald-green eyes with ONE white highlight
- Necklace of SMALL EVENLY SPACED BEADS (~10-12% head width each)
- More open, wide-eyed, affectionate expressions
- More blush on cheeks
- Small dark speckle marks on face

ART STYLE (CRITICAL):
- CLOSE-UP/MEDIUM-CLOSE SHOTS - heads prominent, head-to-midbody framing
- Minimal background - mostly white space with simple horizontal floor line
- Thick clean black outlines, consistent stroke weight
- Flat colors, minimal/no shading
- Small heart icons floating for affection
- Simple motion lines for action
- Three whiskers per side, light pink nose and inner ears

COLOR: White fur #FFFFFF, black outlines #000000, blue/teal pendant, green eyes (female), brown eyes (male)

TEXT DISPLAY: Show narrator text as small caption ABOVE the panel or in speech bubble below."""

# Updated topics with improved scene descriptions
TOPICS = {
    "cozy-morning": {
        "title": "Cozy Morning",
        "scenes": [
            {"description": "CLOSE-UP: Both cats waking up, big heads, morning light. Male yawning, female rubbing eyes. White background with simple floor line.", "text": "Good morning, my love 💕"},
            {"description": "CLOSE-UP: Female preparing tiny breakfast plate, male watching from bed beside her. Both heads in frame.", "text": "Breakfast time!"},
            {"description": "CLOSE-UP: Two cats eating together, heads close, bumping affectionately. Hearts appearing.", "text": "*head bump*"},
            {"description": "CLOSE-UP: Saying goodbye at door, hugging, hearts floating. Both faces visible.", "text": "Have a great day!"}
        ]
    },
    "work-hard-play-hard": {
        "title": "Work Hard, Play Hard", 
        "scenes": [
            {"description": "CLOSE-UP: Male at laptop, tired eyes with dark circles, messy fur, working hard. Female watching from side, concerned expression. Simple desk background.", "text": "You've been working so hard..."},
            {"description": "CLOSE-UP: Female brings coffee to male, both looking at each other with love. Female slightly pouting. Hearts.", "text": "Take a break, please?"},
            {"description": "CLOSE-UP: Male collapsed on desk exhausted, eyes half-closed, papers scattered. Female reaches out worried.", "text": "*exhausted sigh*"},
            {"description": "CLOSE-UP: Female wrapping blanket around male, gently petting his head, pink hearts floating above. Cozy.", "text": "I'll take care of you 💕"}
        ]
    },
    "love-is-all-around": {
        "title": "Love Is All Around",
        "scenes": [
            {"description": "CLOSE-UP: Reading together, heads touching, looking at book. White background.", "text": "Reading together 📚"},
            {"description": "CLOSE-UP: Female giving flower to male, both with loving expressions, big eyes.", "text": "For you 🌸"},
            {"description": "CLOSE-UP: Playing with yarn ball, chasing, action lines, happy expressions.", "text": "Tag! You're it!"},
            {"description": "CLOSE-UP: Curled up sleeping together, tails intertwined, peaceful, tiny hearts.", "text": "Goodnight, my love 💤"}
        ]
    }
}

def generate_story(topic_key: str = None, panels: int = 1):
    if not topic_key:
        day_of_year = datetime.now().timetuple().tm_yday
        topic_key = list(TOPICS.keys())[day_of_year % len(TOPICS)]
    
    topic = TOPICS[topic_key]
    today = datetime.now().strftime("%Y-%m-%d")
    output_subdir = OUTPUT_DIR / today
    output_subdir.mkdir(parents=True, exist_ok=True)
    (output_subdir / "scenes").mkdir(exist_ok=True)
    
    image_prompts = []
    positions = ["top-left", "top-right", "bottom-left", "bottom-right"]
    
    for i, scene in enumerate(topic["scenes"], 1):
        prompt = f"""{CHARACTER_PROMPT}

Scene {i}/4: {scene['description']}

Show this text in the image: "{scene['text']}" (as caption above or speech bubble)
Composition: Scene will be in {positions[i-1]} of 2x2 grid panel
Keep characters LARGE in frame - close-up style
Minimal background - white space with simple floor line
Hearts and motion lines for emotion/action"""
        image_prompts.append({
            "scene_num": i,
            "text": scene["text"],
            "description": scene["description"],
            "prompt": prompt
        })
    
    story_plan = {
        "date": today,
        "topic": topic_key,
        "title": topic["title"],
        "scenes": image_prompts,
        "created_at": datetime.now().isoformat()
    }
    
    with open(output_subdir / "story.json", "w") as f:
        json.dump(story_plan, f, indent=2)
    
    caption = f"""🐾 Little Paws: {topic['title']}

#LittlePaws #CuteCats #Kawaii #CatCouple #ChibiCats #CatComic #Webtoon #DailyComic #CatLovers #FluffyCats #KawaiiArt #CatStory"""
    
    with open(output_subdir / "caption.txt", "w") as f:
        f.write(caption)
    
    print(f"Generated {topic['title']}")
    for sp in image_prompts:
        print(f"  Scene {sp['scene_num']}: {sp['text']}")
    
    return output_subdir, topic, image_prompts

if __name__ == "__main__":
    import sys
    topic = sys.argv[1] if len(sys.argv) > 1 else None
    generate_story(topic)
