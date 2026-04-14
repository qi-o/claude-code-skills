---
name: gif-sticker-maker
description: |
  Convert photos (people, pets, objects, logos) into 4 animated GIF stickers with captions.
  Use when: user wants to create cartoon stickers, GIF expressions, emoji packs, animated avatars,
  or convert photos to Funko Pop / Pop Mart blind box style animations.
  Triggers: sticker, GIF, cartoon, emoji, expression pack, avatar animation.
license: MIT
metadata:
  version: "1.2"
  category: creative-tools
  style: Funko Pop / Pop Mart
  output_format: GIF
  output_count: 4
  sources:
    - MiniMax Image Generation API
    - MiniMax Video Generation API
---

# GIF Sticker Maker

Convert user photos into 4 animated GIF stickers (Funko Pop / Pop Mart style).

## Style Spec

- Funko Pop / Pop Mart blind box 3D figurine
- C4D / Octane rendering quality
- White background, soft studio lighting
- Caption: black text + white outline, bottom of image

## Prerequisites

Before starting any generation step, ensure:

1. **Python venv** is activated with dependencies from [requirements.txt](references/requirements.txt) installed
2. **`MINIMAX_API_KEY`** is exported (e.g. `export MINIMAX_API_KEY='your-key'`)
3. **`ffmpeg`** is available on PATH (for Step 3 GIF conversion)

If any prerequisite is missing, set it up first. Do NOT proceed to generation without all three.

## Workflow

### Step 0: Collect Captions

Ask user (in their language):
> "Would you like to customize the captions for your stickers, or use the defaults?"

- **Custom**: Collect 4 short captions (1–3 words). Actions auto-match caption meaning.
- **Default**: Look up [captions table](references/captions.md) by **detected user language**. **Never mix languages.**

### Step 1: Generate 4 Static Sticker Images

**Tool**: `scripts/minimax_image.py`

1. Analyze the user's photo — identify subject type (person / animal / object / logo).
2. For each of the 4 stickers, build a prompt from [image-prompt-template.txt](assets/image-prompt-template.txt) by filling `{action}` and `{caption}`.
3. **If subject is a person**: pass `--subject-ref <user_photo_path>` so the generated figurine preserves the person's actual facial likeness.
4. Generate (all 4 are independent — **run concurrently**):

```bash
python3 scripts/minimax_image.py "<prompt>" -o output/sticker_hi.png --ratio 1:1 --subject-ref <photo>
python3 scripts/minimax_image.py "<prompt>" -o output/sticker_laugh.png --ratio 1:1 --subject-ref <photo>
python3 scripts/minimax_image.py "<prompt>" -o output/sticker_cry.png --ratio 1:1 --subject-ref <photo>
python3 scripts/minimax_image.py "<prompt>" -o output/sticker_love.png --ratio 1:1 --subject-ref <photo>
```

> `--subject-ref` only works for person subjects (API limitation: type=character).
> For animals/objects/logos, omit the flag and rely on text description.

### Step 2: Animate Each Image → Video

**Tool**: `scripts/minimax_video.py` with `--image` flag (image-to-video mode)

For each sticker image, build a prompt from [video-prompt-template.txt](assets/video-prompt-template.txt), then:

```bash
python3 scripts/minimax_video.py "<prompt>" --image output/sticker_hi.png -o output/sticker_hi.mp4
python3 scripts/minimax_video.py "<prompt>" --image output/sticker_laugh.png -o output/sticker_laugh.mp4
python3 scripts/minimax_video.py "<prompt>" --image output/sticker_cry.png -o output/sticker_cry.mp4
python3 scripts/minimax_video.py "<prompt>" --image output/sticker_love.png -o output/sticker_love.mp4
```

All 4 calls are independent — **run concurrently**.

### Step 3: Convert Videos → GIF

**Tool**: `scripts/convert_mp4_to_gif.py`

```bash
python3 scripts/convert_mp4_to_gif.py output/sticker_hi.mp4 output/sticker_laugh.mp4 output/sticker_cry.mp4 output/sticker_love.mp4
```

Outputs GIF files alongside each MP4 (e.g. `sticker_hi.gif`).

### Step 4: Deliver

Output format (strict order):
1. Brief status line (e.g. "4 stickers created:")
2. `<deliver_assets>` block with all GIF files
3. **NO text after deliver_assets**

```xml
<deliver_assets>
<item><path>output/sticker_hi.gif</path></item>
<item><path>output/sticker_laugh.gif</path></item>
<item><path>output/sticker_cry.gif</path></item>
<item><path>output/sticker_love.gif</path></item>
</deliver_assets>
```

## Default Actions

| # | Action | Filename ID | Animation |
|---|--------|-------------|-----------|
| 1 | Happy waving | hi | Wave hand, slight head tilt |
| 2 | Laughing hard | laugh | Shake with laughter, eyes squint |
| 3 | Crying tears | cry | Tears stream, body trembles |
| 4 | Heart gesture | love | Heart hands, eyes sparkle |

See [references/captions.md](references/captions.md) for multilingual caption defaults.

## Rules

- Detect user's language, all outputs follow it
- Captions MUST come from [captions.md](references/captions.md) matching user's language column — never mix languages
- All image prompts must be in **English** regardless of user language (only caption text is localized)
- `<deliver_assets>` must be LAST in response, no text after

## 用户确认检查点

以下操作前**必须暂停并询问用户确认**：

| 检查点 | 触发条件 | 确认内容 |
|--------|---------|---------|
| 自定义文案 | Step 0 询问用户是否自定义 caption | 确认使用默认文案或收集 4 条自定义短文案（1-3 词） |
| 使用用户照片 | 检测到人物主体需要 `--subject-ref` | 确认照片路径和是否同意将面部 likeness 用于生成 |
| API 调用开销 | 首次执行将调用 4 次图像 + 4 次视频 API | 提示将消耗 MiniMax API 额度，确认后开始 |

## 错误处理与回退

| 错误场景 | 检测信号 | 回退策略 |
|---------|---------|---------|
| MINIMAX_API_KEY 未配置 | 脚本报错缺少 API key | 提示设置环境变量，参考 `~/.claude/env.d/minimax.env` |
| ffmpeg 不可用 | Step 3 MP4 转 GIF 失败 | 提示安装 ffmpeg，或提供手动转换命令 |
| 图像生成质量不佳 | 生成结果与预期风格不符 | 调整 prompt 中的动作描述和风格关键词，重新生成单张 |
| 视频生成超时或失败 | minimax_video.py 返回失败状态码 | 检查 API 响应中的 status_msg，降低 prompt 复杂度后重试 |

**原则**：不要静默失败——报错时同时提供修复建议。
