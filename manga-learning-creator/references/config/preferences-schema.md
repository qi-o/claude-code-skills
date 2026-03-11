---
name: preferences-schema
description: EXTEND.md YAML schema for baoyu-comic user preferences
---

# Preferences Schema

## Full Schema

```yaml
---
version: 2

watermark:
  enabled: false
  content: ""
  position: bottom-right  # bottom-right|bottom-left|bottom-center|top-right

preferred_art: null       # ligne-claire|manga|realistic|ink-brush|chalk
preferred_tone: null      # neutral|warm|dramatic|romantic|energetic|vintage|action
preferred_layout: null    # standard|cinematic|dense|splash|mixed|webtoon
preferred_aspect: null    # 3:4|4:3|16:9

language: null            # zh|en|ja|ko|auto

character_presets:
  - name: my-characters
    roles:
      learner: "Name"
      mentor: "Name"
      challenge: "Name"
      support: "Name"
---
```

## Field Reference

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `version` | int | 2 | Schema version |
| `watermark.enabled` | bool | false | Enable watermark |
| `watermark.content` | string | "" | Watermark text (@username or custom) |
| `watermark.position` | enum | bottom-right | Position on image |
| `preferred_art` | string | null | Art style (ligne-claire, manga, realistic, ink-brush, chalk) |
| `preferred_tone` | string | null | Tone (neutral, warm, dramatic, romantic, energetic, vintage, action) |
| `preferred_layout` | string | null | Layout preference or null |
| `preferred_aspect` | string | null | Aspect ratio (3:4, 4:3, 16:9) |
| `language` | string | null | Output language (null = auto-detect) |
| `character_presets` | array | [] | Preset character roles for styles like ohmsha |

## Art Style Options

| Value | 涓枃 | Description |
|-------|------|-------------|
| `ligne-claire` | 娓呯嚎 | Uniform lines, flat colors, European comic tradition |
| `manga` | 鏃ユ极 | Large eyes, manga conventions, expressive emotions |
| `realistic` | 鍐欏疄 | Digital painting, realistic proportions |
| `ink-brush` | 姘村ⅷ | Chinese brush strokes, ink wash effects |
| `chalk` | 绮夌瑪 | Chalkboard aesthetic, hand-drawn warmth |

## Tone Options

| Value | 涓枃 | Description |
|-------|------|-------------|
| `neutral` | 涓€?| Balanced, rational, educational |
| `warm` | 娓╅Θ | Nostalgic, personal, comforting |
| `dramatic` | 鎴忓墽 | High contrast, intense, powerful |
| `romantic` | 娴极 | Soft, beautiful, decorative elements |
| `energetic` | 娲诲姏 | Bright, dynamic, exciting |
| `vintage` | 澶嶅彜 | Historical, aged, period authenticity |
| `action` | 鍔ㄤ綔 | Speed lines, impact effects, combat |

## Position Options

| Value | Description |
|-------|-------------|
| `bottom-right` | Lower right corner (default, works with most panel layouts) |
| `bottom-left` | Lower left corner |
| `bottom-center` | Bottom center (good for webtoon vertical scroll) |
| `top-right` | Upper right corner (avoid - conflicts with page numbers) |

## Character Preset Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Unique preset identifier |
| `roles.learner` | No | Character representing the learner/protagonist |
| `roles.mentor` | No | Character representing the teacher/guide |
| `roles.challenge` | No | Character representing obstacles/antagonist |
| `roles.support` | No | Character providing support/comic relief |

## Example: Minimal Preferences

```yaml
---
version: 2
watermark:
  enabled: true
  content: "@myusername"
preferred_art: ligne-claire
preferred_tone: neutral
---
```

## Example: Full Preferences

```yaml
---
version: 2
watermark:
  enabled: true
  content: "@comicstudio"
  position: bottom-right

preferred_art: manga
preferred_tone: neutral

preferred_layout: webtoon

preferred_aspect: "3:4"

language: zh

character_presets:
  - name: tech-tutorial
    roles:
      learner: "灏忔槑"
      mentor: "鏁欐巿"
      challenge: "闅鹃鎬?
      support: "灏忓姪鎵?
  - name: doraemon
    roles:
      learner: "澶ч泟"
      mentor: "鍝嗗暒A姊?
      challenge: "鑳栬檸"
      support: "闈欓"
---
```

## Migration from v1

If you have a v1 preferences file with `preferred_style`, migrate as follows:

| Old `preferred_style.name` | New `preferred_art` | New `preferred_tone` |
|---------------------------|---------------------|---------------------|
| classic | ligne-claire | neutral |
| dramatic | ligne-claire | dramatic |
| warm | ligne-claire | warm |
| sepia | realistic | vintage |
| vibrant | manga | energetic |
| ohmsha | manga | neutral |
| realistic | realistic | neutral |
| wuxia | ink-brush | action |
| shoujo | manga | romantic |
| chalkboard | chalk | neutral |
