---
name: gif-sticker-maker
description: Create animated GIF stickers from photos — Funko Pop / Pop Mart style 3D figurines with captions. Uses MiniMax Image→Video→GIF pipeline. Trigger when user asks to make GIF stickers, animated stickers, or dynamic emoji from photos.
type: skill
github_url: https://github.com/MiniMax-AI/skills
github_hash: b4c7c3fcd4d8c1f6e2a3d7b9c5e1f4a8d2b7c3e9
version: 1.0.0
---

# GIF Sticker Maker

Create 4 animated GIF stickers from a photo (person, pet, object, logo) in Funko Pop / Pop Mart blind box style. MiniMax Image→Video→GIF pipeline.

## Prerequisites

1. `MINIMAX_API_KEY` set (via `~/.claude/env.d/minimax.env`)
2. Python with `requests` library
3. `ffmpeg` on PATH (for GIF conversion)
4. MiniMax multimodal toolkit scripts available at `../minimax-multimodal-toolkit/scripts/`

## Full Workflow

### Step 0: Collect Captions

Ask user: "Custom captions or use defaults?"

**Default captions** (by language):
| Action | EN | CN | JP |
|--------|----|----|-----|
| Waving | Hi~ | 嗨~ | やあ~ |
| Laughing | LOL | 哈哈哈 | 笑 |
| Crying | Boo-hoo | 呜呜呜 | えーん |
| Heart | Love ya | 爱你哦 | 大好き |

**Default actions**:
1. Happy waving — wave hand, slight head tilt
2. Laughing hard — shake with laughter, eyes squint
3. Crying tears — tears stream, body trembles
4. Heart gesture — heart hands, eyes sparkle

### Step 1: Generate 4 Static Sticker Images

```bash
python ../minimax-multimodal-toolkit/scripts/minimax_image.py \
  --prompt "Transform the subject into a Funko Pop / Pop Mart blind box style 3D figurine. Cute cartoon proportions (large head, small body), 3D rendered (C4D/Octane quality), premium plastic/vinyl finish, clean white background, soft studio lighting. Action: waving cheerfully. Caption: Hi~" \
  --subject-ref photo.jpg \
  --subject-type character \
  -o minimax-output/sticker_hi.png --ratio 1:1
```

Run all 4 concurrently:
- `sticker_hi.png` — Hi~ / waving
- `sticker_laugh.png` — LOL / laughing
- `sticker_cry.png` — Boo-hoo / crying
- `sticker_love.png` — Love ya / heart gesture

### Step 2: Animate Each Image → Video (I2V)

```bash
python ../minimax-multimodal-toolkit/scripts/minimax_video.py \
  --mode i2v \
  --prompt "Animate this cute 3D cartoon figurine waving hand cheerfully, slight head tilt. Smooth loopable motion, character stays centered, white background remains static." \
  --image minimax-output/sticker_hi.png \
  -o minimax-output/sticker_hi.mp4 --duration 6 --resolution 768P
```

Run all 4 concurrently.

### Step 3: Convert Videos → GIF

Use `scripts/convert_mp4_to_gif.py`:

```bash
python scripts/convert_mp4_to_gif.py \
  minimax-output/sticker_hi.mp4 \
  minimax-output/sticker_laugh.mp4 \
  minimax-output/sticker_cry.mp4 \
  minimax-output/sticker_love.mp4 \
  --fps 15 --width 360
```

Output: `minimax-output/sticker_hi.gif`, `sticker_laugh.gif`, `sticker_cry.gif`, `sticker_love.gif`

### Step 4: Deliver

Output format:
1. Brief status line
2. `<deliver_assets>` block with all 4 GIF files
3. NO text after deliver_assets

## Caption Prompt Template

```
Transform the subject into a Funko Pop / Pop Mart blind box style 3D figurine.

Style:
- Cute cartoon proportions (large head, small body)
- 3D rendered (C4D/Octane quality), premium plastic/vinyl finish
- Clean white background, soft studio lighting

Subject handling:
- Person: preserve facial features, hairstyle, clothing
- Animal/Pet: preserve species, fur color, markings
- Object: stylize into cute mascot figurine
- Logo/Icon: transform to 3D toy, preserve original colors and shape

Action: {action}
Caption: "{caption}"

Caption rendering:
- Black bold text with thick white outline stroke
- Large, clear sans-serif font
- Placed at absolute bottom center of image as standalone text banner
- NOT on character's body, clothing, or any accessory
- Leave visible gap between character's feet and caption text
```

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| No face recognized | subject-ref not working | Try without --subject-ref, use full prompt description |
| GIF too large | fps or resolution too high | Lower --fps to 12, --width to 280 |
|表情动作不自然 | Video prompt too vague | Be specific: "wave hand", not just "action" |
