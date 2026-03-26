---
name: minimax-multimodal-toolkit
description: Unified MiniMax multi-modal generation — TTS, music, image, video, voice cloning, and voice design. Trigger when user asks to generate images, videos, music, speech, or clone voices.
type: skill
github_url: https://github.com/MiniMax-AI/skills
github_hash: b4c7c3fcd4d8c1f6e2a3d7b9c5e1f4a8d2b7c3e9
version: 1.0.0
---

# MiniMax Multi-Modal Toolkit

Unified entry point for all MiniMax generation APIs. All scripts read `MINIMAX_API_KEY` from environment and output to `minimax-output/`.

## Quick Reference

| Asset | Command | Sync |
|-------|---------|------|
| Text-to-Speech | `python scripts/minimax_tts.py "text" -o output.mp3` | Sync |
| Music | `python scripts/minimax_music.py --prompt "style" -o music.mp3` | Sync |
| Image | `python scripts/minimax_image.py --prompt "description" -o image.png` | Sync |
| Video (T2V) | `python scripts/minimax_video.py --prompt "scene" -o video.mp4` | Async |
| Video (I2V) | `python scripts/minimax_video.py --prompt "scene" --image src.png -o video.mp4` | Async |
| Voice Clone | `python scripts/minimax_voice.py clone sample.mp3 --voice-id myvoice` | Async |
| Voice Design | `python scripts/minimax_voice.py design "description" --voice-id myvoice` | Async |

## Environment Setup

```bash
# Source the API key from env.d
# Scripts automatically read MINIMAX_API_KEY from environment
export MINIMAX_API_KEY=sk-api-ttnnh_...   # already configured in ~/.claude/env.d/minimax.env
export MINIMAX_API_HOST=https://api.minimax.io  # or https://api.minimaxi.com for China
```

## Output

All output files are saved to `minimax-output/` in the current working directory. Create it if missing:

```bash
mkdir -p minimax-output
```

## TTS (Text-to-Speech)

### Basic TTS
```bash
python scripts/minimax_tts.py "你好世界" -o minimax-output/hello.mp3
```

### TTS with emotion and voice
```bash
python scripts/minimax_tts.py "I'm so excited!" --voice female-shaonu --emotion happy -o minimax-output/excited.mp3
```

### Available voices: male-qn-qingse, female-shaonu, male-qn-qingse, etc.
### Available emotions: happy, sad, angry, anxious, neutral

### Multi-segment TTS (for dialogue)
```bash
python scripts/minimax_voice.py merge segment1.mp3 segment2.mp3 -o dialogue.mp3
```

## Music Generation

### Instrumental
```bash
python scripts/minimax_music.py --instrumental --prompt "ambient electronic relaxing" -o minimax-output/music.mp3 --download
```

### With lyrics
```bash
python scripts/minimax_music.py --lyrics --prompt "upbeat pop" --lyrics-content "Verse:... Chorus:..." -o minimax-output/song.mp3 --download
```

## Image Generation

### Text-to-Image
```bash
python scripts/minimax_image.py --prompt "A serene lake at sunset with mountains in the background" -o minimax-output/landscape.png --ratio 16:9
```

### Image-to-Image (with subject reference)
```bash
python scripts/minimax_image.py --prompt "same character in a cyberpunk city" --subject-ref photo.png --subject-type character -o minimax-output/character.png
```

### Available aspect ratios: 1:1, 16:9, 4:3, 3:2, 2:3, 3:4, 9:16, 21:9

## Video Generation

### Text-to-Video (Async — polls until complete)
```bash
python scripts/minimax_video.py --mode t2v --prompt "A cat playing piano dramatically" -o minimax-output/cat.mp4
```

### Image-to-Video (Animate a still image)
```bash
python scripts/minimax_video.py --mode i2v --prompt "The character waving" --image input.png -o minimax-output/animation.mp4
```

### With camera commands
```bash
python scripts/minimax_video.py --mode t2v --prompt "A drone shot over ocean" --camera "[Drone right]" -o minimax-output/ocean.mp4
```

**Camera commands**: [Truck left], [Push in], [Static shot], [Orbit right], [Drone left], etc.

### Resolution and Duration
- `--resolution`: 720P, 768P, 1080P (default 768P)
- `--duration`: 6 or 10 seconds

## Voice Clone & Design

### Clone a voice
```bash
python scripts/minimax_voice.py clone audio_sample.mp3 --voice-id my-clone
```

### Design a custom voice
```bash
python scripts/minimax_voice.py design "Warm male narrator voice with slight British accent" --voice-id narrator
```

## Error Handling

All scripts exit with:
- `0`: Success
- `1`: API error or validation failure
- `2`: Missing dependencies

If you see `API Error [1001]: ...`, check your API key and network connection.

## API Reference

See `references/api-reference.md` for full endpoint documentation.


## User-Learned Best Practices & Constraints

> **Auto-Generated Section**: This section is maintained by `skill-evolution-manager`. Do not edit manually.

### Known Fixes & Workarounds
- TTS API output_format 只支持 hex，不支持 mp3，否则返回 2013 invalid params
- TTS 默认 voice 应为 female-tianmei，female-shaonu 返回 2054 voice id not exist