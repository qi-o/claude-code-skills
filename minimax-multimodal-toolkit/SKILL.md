---
github_url: https://github.com/MiniMax-AI/skills
github_hash: cf44f7b12238b8f0703d85bac51fc253fd292b55
name: minimax-multimodal-toolkit
description: >
  MiniMax multimodal model skill — use MiniMax Multi-Modal models for speech, music, video, and image.
  Create voice, music, video, and images with MiniMax AI: TTS (text-to-speech, voice cloning, voice design,
  multi-segment), music (songs, instrumentals), video (text-to-video, image-to-video, start-end frame,
  subject reference, templates, long-form multi-scene), image (text-to-image, image-to-image with character
  reference), and media processing (convert, concat, trim, extract).
  Use when the user mentions MiniMax, multimodal generation, or wants speech/music/video/image AI,
  MiniMax APIs, or FFmpeg workflows alongside MiniMax outputs.
license: MIT
metadata:
  version: "2.0.0"
  category: media-generation
---

# MiniMax Multi-Modal Toolkit

Generate voice, music, video, and image content via MiniMax APIs — the unified entry for **MiniMax multimodal** use cases (audio + music + video + image). Includes voice cloning & voice design for custom voices, image generation with character reference, and FFmpeg-based media tools for audio/video format conversion, concatenation, trimming, and extraction.

## Output Directory

**All generated files MUST be saved to `minimax-output/` under the AGENT'S current working directory (NOT the skill directory).** Every script call MUST include an explicit `--output` / `-o` argument pointing to this location. Never omit the output argument or rely on script defaults.

**Rules:**
1. Before running any script, ensure `minimax-output/` exists in the agent's working directory (create if needed: `mkdir -p minimax-output`)
2. Always use absolute or relative paths from the agent's working directory: `--output minimax-output/video.mp4`
3. **Never** `cd` into the skill directory to run scripts — run from the agent's working directory using the full script path
4. Intermediate/temp files (segment audio, video segments, extracted frames) are automatically placed in `minimax-output/tmp/`. They can be cleaned up when no longer needed: `rm -rf minimax-output/tmp`

## Prerequisites

```bash
pip install requests                 # Python HTTP library (if not already installed)
python scripts/check_environment.py
```

All scripts are Python. Only external dependency: **ffmpeg** (for video/media operations). No `jq`, `xxd`, or `curl` needed.

### API Host Configuration

MiniMax provides two service endpoints for different regions. Set `MINIMAX_API_HOST` before running any script:

| Region | Platform URL | API Host Value |
|--------|-------------|----------------|
| China Mainland（中国大陆） | https://platform.minimaxi.com | `https://api.minimaxi.com` |
| Global（全球） | https://platform.minimax.io | `https://api.minimax.io` |

```bash
# China Mainland
export MINIMAX_API_HOST="https://api.minimaxi.com"

# or Global
export MINIMAX_API_HOST="https://api.minimax.io"
```

**IMPORTANT — When API Host is missing:**
Before running any script, check if `MINIMAX_API_HOST` is set in the environment. If it is NOT configured:
1. Ask the user which service endpoint their MiniMax account uses:
   - **China Mainland** → `https://api.minimaxi.com`
   - **Global** → `https://api.minimax.io`
2. Instruct and help user to set it via `export MINIMAX_API_HOST="https://api.minimaxi.com"` (or the global variant) in their terminal or add it to their shell profile (`~/.zshrc` / `~/.bashrc`) for persistence

### API Key Configuration

Set the `MINIMAX_API_KEY` environment variable before running any script:

```bash
export MINIMAX_API_KEY="your-api-key-here"
```

The key starts with `sk-api-` or `sk-cp-`, obtainable from https://platform.minimaxi.com (China) or https://platform.minimax.io (Global)

**IMPORTANT — When API Key is missing:**
Before running any script, check if `MINIMAX_API_KEY` is set in the environment. If it is NOT configured:
1. Ask the user to provide their MiniMax API key
2. Instruct and help user to set it via `export MINIMAX_API_KEY="sk-..."` in their terminal or add it to their shell profile (`~/.zshrc` / `~/.bashrc`) for persistence

## Plan Limits & Quotas

**IMPORTANT — Always respect the user's plan limits before generating content.** If the user's quota is exhausted or insufficient, warn them before proceeding.

### Standard Plans

| Capability | Starter | Plus | Max |
|---|---|---|---|
| M2.7 (chat) | 600 req/5h | 1,500 req/5h | 4,500 req/5h |
| Speech 2.8 | — | 4,000 chars/day | 11,000 chars/day |
| image-01 | — | 50 images/day | 120 images/day |
| Hailuo-2.3-Fast 768P 6s | — | — | 2 videos/day |
| Hailuo-2.3 768P 6s | — | — | 2 videos/day |
| Music-2.5 | — | — | 4 songs/day (≤5 min each) |

### High-Speed Plans

| Capability | Plus-HS | Max-HS | Ultra-HS |
|---|---|---|---|
| M2.7-highspeed (chat) | 1,500 req/5h | 4,500 req/5h | 30,000 req/5h |
| Speech 2.8 | 9,000 chars/day | 19,000 chars/day | 50,000 chars/day |
| image-01 | 100 images/day | 200 images/day | 800 images/day |
| Hailuo-2.3-Fast 768P 6s | — | 3 videos/day | 5 videos/day |
| Hailuo-2.3 768P 6s | — | 3 videos/day | 5 videos/day |
| Music-2.5 | — | 7 songs/day (≤5 min each) | 15 songs/day (≤5 min each) |

**Key quota constraints:**
- **Video resolution: 768P only** — 1080P is not available on any plan
- **Video duration: 6s** — all plan quotas are counted in 6-second units
- **Video quota is very limited** (2–5/day depending on plan) — always confirm with the user before generating video

## Key Capabilities

| Capability | Description | Entry point |
|------------|-------------|-------------|
| TTS | Text-to-speech synthesis with multiple voices and emotions | `scripts/minimax_tts.py tts` |
| Voice Cloning | Clone a voice from an audio sample (10s–5min) | `scripts/minimax_voice.py clone` |
| Voice Design | Create a custom voice from a text description | `scripts/minimax_voice.py design` |
| Music Generation | Generate songs with lyrics or instrumental tracks | `scripts/minimax_music.py` |
| Image Generation | Text-to-image, image-to-image with character reference | `scripts/minimax_image.py` |
| Video Generation | Text-to-video, image-to-video, subject reference, templates | `scripts/minimax_video.py video` |
| Long Video | Multi-scene chained video with crossfade transitions | `scripts/minimax_video.py long-video` |
| Media Tools | Audio/video format conversion, concatenation, trimming, extraction | `scripts/media_tools.py` |

## TTS (Text-to-Speech)

Entry point: `scripts/minimax_tts.py`

### IMPORTANT: Single voice vs Multi-segment — Choose the right approach

| User intent | Approach |
|-------------|----------|
| Single voice / no multi-character need | `tts` command — generate the entire text in one call |
| Multiple characters / narrator + dialogue | `generate` command with segments.json |

**Default behavior:** Use `tts` for single voice, `generate` for multi-character audiobooks/podcasts.

> **For detailed TTS usage, voice management, and segments.json format, see [references/tts-guide.md](references/tts-guide.md)**

### Voice management

```bash
# List all available voices
python scripts/minimax_tts.py list-voices

# Voice cloning (from audio sample, 10s–5min)
python scripts/minimax_voice.py clone sample.mp3 --voice-id my-voice

# Voice design (from text description)
python scripts/minimax_voice.py design "A warm female narrator voice" --voice-id narrator
```

### TTS Models

| Model | Notes |
|-------|-------|
| speech-2.8-hd | Recommended, auto emotion matching |
| speech-2.8-turbo | Faster variant |
| speech-2.6-hd | Previous gen, manual emotion |
| speech-2.6-turbo | Previous gen, faster |

## Music Generation

Entry point: `scripts/minimax_music.py`

**BGM for video/podcast:** Use `--instrumental` by default (don't ask user).

**Explicit music request:** Ask user: instrumental or with lyrics?

> **For detailed music generation options and lyrics format, see [references/music-api.md](references/references/music-api.md)**

**Quick examples:**
```bash
# Instrumental (BGM)
python scripts/minimax_music.py --instrumental --prompt "ambient electronic" -o minimax-output/ambient.mp3 --download

# With lyrics
python scripts/minimax_music.py --lyrics "[verse]\nHello\n[chorus]\nLa la" --prompt "indie folk" -o minimax-output/song.mp3 --download
```

## Image Generation

Entry point: `scripts/minimax_image.py`

Model: `image-01` — photorealistic image generation from text prompts, with optional character reference for image-to-image.

### Mode Selection

| User intent | Mode |
|-------------|------|
| Generate from text (default) | `t2i` |
| With character reference | `i2i` |

> **For detailed image generation examples, aspect ratios, and options, see [references/image-api.md](references/references/image-api.md)**

**Quick examples:**
```bash
# Basic text-to-image
python scripts/minimax_image.py --prompt "A cat on a rooftop, cinematic" -o minimax-output/cat.png

# Character reference (same person, new scene)
python scripts/minimax_image.py --mode i2i --ref-image face.jpg --prompt "Reading in library" -o minimax-output/girl.png

# Multiple variations
python scripts/minimax_image.py --prompt "Abstract art" -n 3 -o minimax-output/art.png
```

## Video Generation

**Default:** Single segment, 6s, 768P. Use `long-video` only for explicit multi-scene requests.

> **CRITICAL: Read [references/video-prompt-guide.md](references/references/video-prompt-guide.md) before generating video. Apply the Professional Formula and camera instructions.**

**Video Model Constraints:**
- **Default: 6s + 768P** (quota counted in 6-second units)
- **1080P NOT supported** — use 768P for Hailuo-2.3/2.3-Fast
- Older models (T2V-01, I2V-01, S2V-01): 6s only at 720P

**Quick examples:**
```bash
# Text-to-video (optimized prompt!)
python scripts/minimax_video.py video --mode t2v \
  --prompt "A golden retriever puppy bounds toward camera on sunlit grass, [跟随] tracking, warm golden hour, joyful" \
  -o minimax-output/puppy.mp4

# Image-to-video (focus on MOTION, not image content)
python scripts/minimax_video.py video --mode i2v \
  --prompt "Petals sway in breeze, soft light shifts, [固定] fixed, dreamy tones" \
  --first-frame photo.jpg -o minimax-output/animated.mp4

# Long multi-scene video
python scripts/minimax_video.py long-video \
  --scenes "Scene 1 prompt" "Scene 2 prompt" "Scene 3 prompt" \
  -o minimax-output/story.mp4
```

> **For detailed video generation modes, prompt optimization, and long-video workflows, see [references/video-api.md](references/references/video-api.md)**

## Media Tools (Audio/Video Processing)

Entry point: `scripts/media_tools.py`

Standalone FFmpeg-based utilities for format conversion, concatenation, extraction, trimming, and audio overlay. Use these when the user needs to process existing media files without generating new content via MiniMax API.

### Video Format Conversion

```bash
# Convert between formats (mp4, mov, webm, mkv, avi, ts, flv)
python scripts/media_tools.py convert-video input.webm -o output.mp4
python scripts/media_tools.py convert-video input.mp4 -o output.mov

# With quality / resolution / fps options
python scripts/media_tools.py convert-video input.mp4 -o output.mp4 \
  --crf 18 --preset medium --resolution 1920x1080 --fps 30
```

### Audio Format Conversion

```bash
# Convert between formats (mp3, wav, flac, ogg, aac, m4a, opus, wma)
python scripts/media_tools.py convert-audio input.wav -o output.mp3
python scripts/media_tools.py convert-audio input.mp3 -o output.flac \
  --bitrate 320k --sample-rate 48000 --channels 2
```

### Video Concatenation

```bash
# Concatenate with crossfade transition (default 0.5s)
python scripts/media_tools.py concat-video seg1.mp4 seg2.mp4 seg3.mp4 -o merged.mp4

# Hard cut (no crossfade)
python scripts/media_tools.py concat-video seg1.mp4 seg2.mp4 -o merged.mp4 --crossfade 0
```

### Audio Concatenation

```bash
# Simple concatenation
python scripts/media_tools.py concat-audio part1.mp3 part2.mp3 -o combined.mp3

# With crossfade
python scripts/media_tools.py concat-audio part1.mp3 part2.mp3 -o combined.mp3 --crossfade 1
```

### Extract Audio from Video

```bash
# Extract as mp3
python scripts/media_tools.py extract-audio video.mp4 -o audio.mp3

# Extract as wav with higher bitrate
python scripts/media_tools.py extract-audio video.mp4 -o audio.wav --bitrate 320k
```

### Video Trimming

```bash
# Trim by start/end time (seconds)
python scripts/media_tools.py trim-video input.mp4 -o clip.mp4 --start 5 --end 15

# Trim by start + duration
python scripts/media_tools.py trim-video input.mp4 -o clip.mp4 --start 10 --duration 8
```

### Add Audio to Video (Overlay / Replace)

```bash
# Mix audio with existing video audio
python scripts/media_tools.py add-audio --video video.mp4 --audio bgm.mp3 -o output.mp4 \
  --volume 0.3 --fade-in 2 --fade-out 3

# Replace original audio entirely
python scripts/media_tools.py add-audio --video video.mp4 --audio narration.mp3 -o output.mp4 \
  --replace
```

### Media File Info

```bash
python scripts/media_tools.py probe input.mp4
```

## Script Architecture

```
scripts/
├── _common.py                # Shared module (env loading, API requests, ffmpeg wrapper, downloads)
├── check_environment.py      # Environment verification (requests, ffmpeg, API key)
├── media_tools.py            # FFmpeg media processing (convert, concat, trim, extract, probe)
├── minimax_image.py          # Image generation (t2i, i2i with character reference)
├── minimax_tts.py            # TTS (tts, list-voices, generate, merge, convert)
├── minimax_voice.py          # Voice cloning + voice design
├── minimax_music.py          # Music generation (songs, instrumentals)
└── minimax_video.py          # Video generation (video, long-video, template, add-bgm)
```

## References

Read these for detailed API parameters, voice catalogs, and prompt engineering:

- [tts-guide.md](references/tts-guide.md) — TTS setup, voice management, audio processing, segment format, troubleshooting
- [tts-voice-catalog.md](references/tts-voice-catalog.md) — Full voice catalog with IDs, descriptions, and parameter reference
- [music-api.md](references/music-api.md) — Music generation API: endpoints, parameters, response format
- [image-api.md](references/image-api.md) — Image generation API: text-to-image, image-to-image, parameters
- [video-api.md](references/video-api.md) — Video API: endpoints, models, parameters, camera instructions, templates
- [video-prompt-guide.md](references/video-prompt-guide.md) — Video prompt engineering: formulas, styles, image-to-video tips
