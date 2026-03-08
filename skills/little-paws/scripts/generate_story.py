#!/usr/bin/env python3
"""
Little Paws Daily Story Generator
Generates 4-frame or 8-frame stories for Instagram Reels
"""

import os
import json
import random
from datetime import datetime
from pathlib import Path

# Paths
SKILL_DIR = Path("/root/.openclaw/workspace/kallavi-turk-skills/skills/little-paws")
OUTPUT_DIR = SKILL_DIR / "output"
REFERENCE_DIR = SKILL_DIR / "reference"
SCRIPTS_DIR = Path("/root/.openclaw/workspace/kallavi-turk-skills/skills/frame-forge/scripts")

# Story topics
TOPICS = {
    "cozy-morning": {
        "title": "Cozy Morning",
        "synopsis": "A sweet morning routine where the couple starts their day with love and warmth.",
        "scenes": [
            "Sunlight streams through the window as both cats wake up stretchily",
            "The caregiver cat prepares breakfast while the other watches sleepily", 
            "They eat together, heads bumping affectionately",
            "A goodbye hug at the door, hearts floating around"
        ],
        "texts": [
            "Good morning, my love 💕",
            "Breakfast time!",
            "*head bump*",
            "Have a great day!"
        ]
    },
    "work-hard-play-hard": {
        "title": "Work Hard, Play Hard",
        "synopsis": "One cat works too hard, the other takes care of them with love.",
        "scenes": [
            "The overworked cat is at laptop, fur messy, tired eyes",
            "The caregiver cat brings coffee/snacks, concerned expression",
            "The overworked cat finally collapses, exhausted",
            "The caregiver wraps them in a blanket, pets their head, hearts appear"
        ],
        "texts": [
            "You've been working so hard...",
            "Take a break, please?",
            "*exhausted sigh*",
            "I'll take care of you 💕"
        ]
    },
    "love-is-all-around": {
        "title": "Love Is All Around",
        "synopsis": "Small everyday moments that show their love through actions.",
        "scenes": [
            "Reading together on the couch, heads touching",
            "One cat finds a pretty flower, gives it to the other",
            "Playing with a yarn ball, chasing each other",
            "Sleeping curled up together, peaceful hearts"
        ],
        "texts": [
            "Reading together 📚",
            "For you 🌸",
            "Tag! You're it!",
            "Goodnight, my love 💤"
        ]
    }
}

# Character prompt block for consistency
CHARACTER_PROMPT = """Two chibi-style white cats in kawaii cartoon style. 

Cat 1 (left, caregiver): Small round fluffy white cat, large sparkling green eyes with multiple white highlights, small pink nose, tiny blush on cheeks, pearl necklace, clean neat white fur, thick black outlines.

Cat 2 (right, overworked): Small fluffy white cat, tired droopy eyes with dark under-eye bags, small pink nose, dark brown collar with teardrop-shaped green pendant, slightly ruffled fur, thick black outlines.

Style: Kawaii chibi cartoon, thick consistent black outlines, flat solid colors with minimal shading, multi-highlight eyes (one large round white highlight + smaller dot), short fur stroke details around edges, small heart motifs. Pure white fur #FFFFFF, black outlines #000000."""

def generate_story(topic_key: str = None, panels: int = 1):
    """Generate a Little Paws story"""
    
    # Select topic
    if not topic_key:
        day_of_year = datetime.now().timetuple().tm_yday
        topics = list(TOPICS.keys())
        topic_key = topics[day_of_year % len(topics)]
    
    topic = TOPICS[topic_key]
    
    # Create output directory for today
    today = datetime.now().strftime("%Y-%m-%d")
    output_subdir = OUTPUT_DIR / today
    output_subdir.mkdir(parents=True, exist_ok=True)
    
    print(f"Generating {topic['title']} story ({panels} panel(s))")
    print(f"Output: {output_subdir}")
    
    # Save story plan
    story_plan = {
        "date": today,
        "topic": topic_key,
        "title": topic["title"],
        "synopsis": topic["synopsis"],
        "panels": panels,
        "created_at": datetime.now().isoformat()
    }
    
    with open(output_subdir / "story.json", "w") as f:
        json.dump(story_plan, f, indent=2)
    
    # Generate caption
    caption = generate_caption(topic["title"], topic["synopsis"])
    with open(output_subdir / "caption.txt", "w") as f:
        f.write(caption)
    
    print(f"\n📝 Instagram Caption:\n{caption}")
    print(f"\n✅ Story plan saved to {output_subdir / 'story.json'}")
    
    return output_subdir, topic

def generate_caption(title: str, synopsis: str) -> str:
    """Generate Instagram caption with hashtags"""
    caption = f"""🐾 Little Paws: {title}

{synopsis}

#LittlePaws #CuteCats #Kawaii #CatCouple #ChibiCats #CatComic #Webtoon #DailyComic #CatLovers #FluffyCats #KawaiiArt #CatStory #PetComic #CuteArt #CatCartoon #FelineArt #KawaiiCats #CatLover #DailyComics #Webcomic"""
    return caption

if __name__ == "__main__":
    import sys
    
    topic = sys.argv[1] if len(sys.argv) > 1 else None
    panels = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    
    output, topic_data = generate_story(topic, panels)
    print(f"\n🎬 Next: Use frame-forge to generate images for {output}")
    print(f"📺 Then: Create video with 2.5s per frame, 9:16 ratio")