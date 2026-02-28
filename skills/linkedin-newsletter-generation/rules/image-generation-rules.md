---
trigger: always_on
---

# Image Generation Rules

This module defines the process for generating abstract, high-end visuals for LinkedIn posts. It enforces the navy-dominant brand identity while allowing "relatable objects" to ground abstract topics.

**Note: This skill generates 1 image, not 3.**

## Image Generation Workflow

Generate ONE relatable object visually compatible with the topic.

1. **Ideation**: Identify 1 distinct object or metaphor strongly associated with the topic (e.g., "shield" for security, "gears" for mechanisms, "glass scales" for trade-offs).

2. **Styling**: Render as **stylized, geometric, wireframe, or glass-morphism elements**. Strictly avoid photorealism.

3. **Requirements**:
   - Navy blue dominant (#1a365d)
   - Abstract/geometric
   - No humans/text
   - Premium, intellectual, "memo-like"

4. **Review**: Ensure it feels premium and intellectual.

5. **Output**: Save to `posts/[topic-slug]/images/1.png`
