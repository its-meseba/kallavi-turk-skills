---
name: little-paws
description: >
  Daily story generation for Little Paws Instagram Reels. Creates 4-frame (1 panel) or 8-frame (2 panel) 
  cute couple cat stories for Instagram. Uses frame-forge skill. Triggers daily at 8pm or via "/little-paws" command.
  Topics: cozy-morning, work-hard-play-hard, love-is-all-around.
---

# Little Paws - Daily Story Generator

Generate cute couple cat stories for Instagram Reels using the frame-forge skill.

## Reference Images

**Location:** `skills/little-paws/reference/`

- `story1.jpg` - Couple dynamics: larger protective cat + smaller playful cat with fish
- `story2.jpg` - Caregiver vs overworked dynamic (pupsik)

**Character Details:**

### Cat 1 (Caregiver/Green Eyes)
- Small, round, fluffy white chibi cat
- Large sparkling green eyes with multi-highlight
- Pearl necklace (sometimes)
- Clean, neat fur
- Expressive, caring, affectionate
- Pink inner ears, blush on cheeks

### Cat 2 (Overworked/Teal Pendant)
- Small, fluffy white chibi cat  
- Tired expressions, reddish under-eye bags
- Dark collar with teardrop-shaped green pendant
- Ruffled/mussed fur when exhausted
- Works too hard, needs caring

**Art Style:** Kawaii/chibi cartoon, thick black outlines, flat colors, multi-highlight eyes

## Main Story Topics (3)

### 1. Cozy Morning (cozy-morning)
The couple wakes up together, has breakfast, starts the day with love.

### 2. Work Hard, Play Hard (work-hard-play-hard)
One cat works too hard, the other takes care of them.

### 3. Love Is All Around (love-is-all-around)
Simple cute moments showing their love through actions.

## Commands

| Command | Description |
|---------|-------------|
| `/little-paws` | Generate today's story (1 panel = 4 frames) |
| `/little-paws:2` | Generate with 2 panels (8 frames) |
| `/little-paws:topic` | Generate specific topic |

## Workflow

### Step 1: Select Topic
Rotate through topics or pick specific one:
- Day 1: cozy-morning
- Day 2: work-hard-play-hard  
- Day 3: love-is-all-around
- Repeat

### Step 2: Generate Story
Use frame-forge to create:
- 1 panel = 4 scenes (default, 2.5s each = 10s reel)
- 2 panels = 8 scenes (20s reel)

### Step 3: Create Video
- Instagram ratio: 9:16 (1080x1920)
- Each frame: 2.5 seconds
- Transition: fade

### Step 4: Generate HTML Viewer
Create HTML with:
- All generated images
- Video player
- Instagram caption with hashtags
- Title

## Output

Save to: `skills/little-paws/output/<date>/`
- `1.png` - Panel 1
- `2.png` - Panel 2 (if 2 panels)
- `story.mp4` - Video
- `viewer.html` - Interactive viewer
- `caption.txt` - Instagram caption

## Instagram Caption Template

```
🐾 Little Paws: [Title]

[Story one-liner]

#LittlePaws #CuteCats #Kawaii #CatCouple #ChibiCats #CatComic #Webtoon #DailyComic #CatLovers #FluffyCats #KawaiiArt #CatStory #PetComic #CuteArt
```

## Daily Automation (8pm)

Create cron job:
```
0 20 * * * curl -X POST http://localhost:18789/v1/sessions/main/agent-turn -d '{"message": "/little-paws"}'
```

Or use OpenClaw's cron system with systemEvent payload.