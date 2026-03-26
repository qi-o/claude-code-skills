# MiniMax API Reference

## Base URL

- **International**: `https://api.minimax.io/v1`
- **China**: `https://api.minimaxi.com/v1`

Set via `MINIMAX_API_HOST` environment variable.

## Authentication

All requests require:
```
Authorization: Bearer {MINIMAX_API_KEY}
Content-Type: application/json
```

## Endpoints

### Text-to-Speech

**POST** `/t2a_v2`

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| model | string | speech-2.8-hd | speech-2.8-hd, speech-2.8-turbo, speech-2.6-hd, speech-2.6-turbo |
| text | string | required | Text to synthesize |
| voice_id | string | required | Voice identifier |
| speed | float | 1.0 | 0.5-2.0 |
| pitch | float | 0 | -12 to 12 |
| volume | float | 1.0 | 0.1-10 |
| emotion | string | neutral | happy, sad, angry, anxious, neutral |
| sample_rate | int | 32000 | 32000 |
| bitrate | int | 128000 | 128000 |
| output_format | string | hex | hex, mp3, wav |

### Music Generation

**POST** `/music_generation`

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| model | string | music-2.5+ | Model identifier |
| prompt | string | required | Style/mood description (max 2000 chars) |
| lyrics | string | | Lyrics with structure tags (max 3500 chars) |
| is_instrumental | bool | false | Generate without vocals |
| lyrics_optimizer | bool | false | Optimize lyrics |
| output_format | string | url | url, hex |

### Image Generation

**POST** `/image_generation`

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| model | string | image-01 | image-01, image-01-live |
| prompt | string | required | Image description (max 1500 chars) |
| aspect_ratio | string | 1:1 | 1:1, 16:9, 4:3, 3:2, 2:3, 3:4, 9:16, 21:9 |
| n | int | 1 | Number of images (1-9) |
| response_format | string | url | url, base64 |
| prompt_optimizer | bool | true | Optimize prompt |
| seed | int | | Random seed for reproducibility |

### Video Generation

**POST** `/video_generation`

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| model | string | MiniMax-Hailuo-2.3 | MiniMax-Hailuo-2.3, MiniMax-Hailuo-02, T2V-01-Director, T2V-01, I2V-01-Director, I2V-01 |
| prompt | string | required | Scene description |
| duration | int | 10 | 6 or 10 seconds |
| resolution | string | 768P | 720P, 768P, 1080P |
| prompt_optimizer | bool | true | Optimize prompt |
| camera_commands | string | | Camera movement commands |

**GET** `/query/video_generation?task_id={id}`

Status values: `Pending`, `Processing`, `Success`, `Fail`

**GET** `/files/retrieve?file_id={id}`

Returns `{ "file_id": "...", "file_url": { "url": "..." } }`

### Voice Clone

**POST** `/v1/voice_clone`

| Parameter | Type | Description |
|-----------|------|-------------|
| voice_id | string | Target voice identifier |
| file | file | Audio sample (mp3/wav, <5MB) |

### Voice Design

**POST** `/v1/voice_design`

| Parameter | Type | Description |
|-----------|------|-------------|
| voice_id | string | Target voice identifier |
| description | string | Voice characteristics description |
