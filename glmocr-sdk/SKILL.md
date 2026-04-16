---
name: glmocr
description: |
  Trigger when: (1) User wants to extract text, tables, formulas, or structured data from images/PDFs/scanned documents, (2) User mentions "OCR", "文字识别", "文档解析", (3) User has a document (screenshot, scanned page, invoice, paper, whiteboard photo) and needs its content in structured form, (4) User asks to parse, digitize, or extract content from a visual document.

  Invokes the GLM-OCR SDK (pip install glmocr) to parse documents via Zhipu's cloud API. No GPU required. Returns structured JSON (regions with labels + bounding boxes) and Markdown. Agent can operate entirely via CLI — no YAML files needed.

  NOT for: real-time camera feeds, audio transcription, or non-document images (photos, illustrations).
metadata:
  openclaw:
    requires:
      env:
        - ZHIPU_API_KEY
      bins:
        - python
    primaryEnv: ZHIPU_API_KEY
    emoji: "📄"
    homepage: https://github.com/zai-org/GLM-OCR/tree/main/skills/sdk
github_url: https://github.com/zai-org/GLM-OCR
github_hash: 20ad544638d586dee100c21046ce8c7c929592fc
---

# OpenClaw Skill: glmocr

Parses documents (images, PDFs, scans) via the GLM-OCR SDK.

> **📌 On-demand**: This skill requires only `ZHIPU_API_KEY` in the environment. No YAML config files or GPU needed.

## ⚡ Quick Start

```bash
# Install
pip install glmocr

# Set API key (once)
export ZHIPU_API_KEY=sk-xxx
# or add to .env file in working directory:
echo "ZHIPU_API_KEY=sk-xxx" >> .env
```

```python
# One-liner
import glmocr
result = glmocr.parse("document.pdf")
print(result.markdown_result)
print(result.to_dict())
```

```bash
# CLI — pass API key directly (no env setup needed)
glmocr parse image.png --api-key sk-xxx

# Or load from a specific .env file
glmocr parse image.png --env-file /path/to/.env

# Or rely on env var / auto-discovered .env (set once, then omit)
glmocr parse image.png
glmocr parse ./scans/ --output ./output/ --stdout
```

---

## Configuration Priority

```
Constructor kwargs  >  os.environ  >  .env file  >  config.yaml  >  built-in defaults
```

Agents override everything via constructor kwargs or env vars — no YAML editing needed.

### Key Environment Variables

| Variable               | Description                            | Example     |
| ---------------------- | -------------------------------------- | ----------- |
| `ZHIPU_API_KEY`        | API key (required for MaaS)            | `sk-abc123` |
| `GLMOCR_MODEL`         | Model name                             | `glm-ocr`   |
| `GLMOCR_TIMEOUT`       | Request timeout (seconds)              | `600`       |
| `GLMOCR_ENABLE_LAYOUT` | Layout detection on/off                | `true`      |
| `GLMOCR_LOG_LEVEL`     | `DEBUG` / `INFO` / `WARNING` / `ERROR` | `INFO`      |

---

## Python API

### Convenience function (single call)

```python
import glmocr

# Single file → PipelineResult
result = glmocr.parse("invoice.png")

# Multiple files → list[PipelineResult]
results = glmocr.parse(["page1.png", "page2.png", "report.pdf"])

# From URL (new — no local file needed)
result = glmocr.parse("https://example.com/document.pdf")
```

### Class-based (multiple calls / resource reuse)

```python
from glmocr import GlmOcr

parser = GlmOcr(api_key="sk-xxx")   # mode auto-set to "maas"
parser = GlmOcr(mode="maas")        # reads ZHIPU_API_KEY from env

# Always use as context manager or call .close()
with GlmOcr(api_key="sk-xxx") as parser:
    result = parser.parse("document.png")
    print(result.markdown_result)

parser.close()   # if not using `with`

# Place layout model on CPU (keep GPU free for OCR)
with GlmOcr(api_key="sk-xxx", layout_device="cpu") as parser:
    result = parser.parse("image.png")

# Place layout model on a specific GPU
with GlmOcr(api_key="sk-xxx", layout_device="cuda:1") as parser:
    result = parser.parse("image.png")
```

### Constructor Parameters

| Parameter       | Type   | Description                                     |
| --------------- | ------ | ----------------------------------------------- |
| `api_key`       | `str`  | API key. Providing this auto-enables MaaS mode. |
| `api_url`       | `str`  | Override MaaS endpoint URL                      |
| `model`         | `str`  | Model name override                             |
| `timeout`       | `int`  | Request timeout in seconds (default: 600)       |
| `enable_layout` | `bool` | Enable layout detection                         |
| `layout_device` | `str`  | Device for layout model: `"cpu"`, `"cuda:1"`, etc. Keeps GPU free for OCR. |
| `log_level`     | `str`  | Logging level                                   |

---

## Working with `PipelineResult`

### Fields

```python
result.markdown_result    # str — full document as Markdown
result.json_result        # list[list[dict]] — structured regions per page
result.original_images    # list[str] — absolute paths of input images
```

### `json_result` structure

List of pages → list of regions per page:

```json
[
  [
    {
      "index": 0,
      "label": "title",
      "content": "Annual Report 2024",
      "bbox_2d": [100, 50, 900, 120]
    },
    {
      "index": 1,
      "label": "table",
      "content": "| Q1 | Q2 |\n|---|---|\n| 120 | 145 |",
      "bbox_2d": [100, 140, 900, 400]
    }
  ]
]
```

**Bounding boxes** (`bbox_2d`): `[x1, y1, x2, y2]` normalised to **0–1000** scale.

**Region labels**: `title`, `text`, `table`, `figure`, `formula`, `header`, `footer`, `page_number`, `reference`, `seal`

### Serialization

```python
# Dict (JSON-serializable, for passing to other tools)
d = result.to_dict()
# Keys: json_result, markdown_result, original_images, usage (MaaS), data_info (MaaS)

# JSON string
json_str = result.to_json()                 # pretty-printed, ensure_ascii=False
json_str = result.to_json(indent=None)      # compact single line

# Save to disk: writes <stem>/<stem>.json + <stem>/<stem>.md + layout_vis/
result.save(output_dir="./output")
result.save(output_dir="./output", save_layout_visualization=False)
```

### Error Handling

The SDK **does not raise** on MaaS errors — check `to_dict()` for an `"error"` key:

```python
result = parser.parse("image.png")
d = result.to_dict()
if "error" in d:
    # Handle failure
    print("OCR failed:", d["error"])
else:
    print(d["markdown_result"])
```

---

## CLI Reference

> **Agent-preferred interface**: use the CLI for most operations. Set `ZHIPU_API_KEY` in env once, then invoke as needed.

**Supported input formats**: `.jpg`, `.jpeg`, `.png`, `.bmp`, `.gif`, `.webp`, `.pdf`, **URLs** (`https://...`)

### Basic usage

```bash
# Parse a single file → saves to ./output/<stem>/
# MaaS mode is the default; ZHIPU_API_KEY must be set (or use --api-key)
glmocr parse image.png

# Pass API key directly without any env setup
glmocr parse image.png --api-key sk-xxx

# Parse a directory → saves each file to ./output/<stem>/
glmocr parse ./scans/

# Parse from URL (new — no local file needed)
glmocr parse https://example.com/document.pdf

# Use self-hosted vLLM/SGLang instead of cloud
glmocr parse image.png --mode selfhosted

# Specify output directory
glmocr parse image.png --output ./results/
```

### Read results in the terminal (agent-friendly)

```bash
# Print Markdown + JSON to stdout (and still save to disk)
glmocr parse image.png --stdout

# Print to stdout ONLY — do not write any files
glmocr parse image.png --stdout --no-save

# JSON only (no Markdown output)
glmocr parse image.png --stdout --json-only

# Pipe JSON into jq for structured extraction
glmocr parse image.png --stdout --json-only --no-save | jq '.[0] | map(select(.label=="table"))'
```

### Save control

```bash
# Skip layout visualization images (faster, smaller output)
glmocr parse image.png --no-layout-vis

# Parse and save only JSON + Markdown, skip layout vis
glmocr parse image.png --no-layout-vis --output ./results/
```

### Batch processing

```bash
# All images in a folder
glmocr parse ./invoice_scans/ --output ./parsed/ --no-layout-vis

# With progress visible in logs
glmocr parse ./docs/ --output ./parsed/ --log-level INFO
```

### Debugging

```bash
glmocr parse image.png --log-level DEBUG
```

### Layout device control (new)

```bash
# Run layout detection on CPU (keep GPU free for OCR model)
glmocr parse image.png --layout-device cpu

# Run layout detection on a specific GPU
glmocr parse image.png --layout-device cuda:1
```

### Override config values (new)

```bash
# Override any config value via --set (dotted path, repeatable)
glmocr parse image.png --set pipeline.ocr_api.api_port 8080
glmocr parse ./scans/ --set pipeline.layout.use_polygon true --set logging.level DEBUG
```

### Full flag reference

| Flag              | Default    | Description                                           |
| ----------------- | ---------- | ----------------------------------------------------- |
| `--api-key / -k`  | env var    | API key for MaaS mode (overrides `ZHIPU_API_KEY`)     |
| `--mode`          | `maas`     | `maas` (cloud, default) or `selfhosted` (local GPU)   |
| `--env-file`      | auto       | Path to `.env` file (default: auto-discover from cwd) |
| `--output / -o`   | `./output` | Output directory                                      |
| `--stdout`        | off        | Print JSON + Markdown to stdout                       |
| `--no-save`       | off        | Skip writing files (use with `--stdout`)              |
| `--json-only`     | off        | stdout JSON only, no Markdown                         |
| `--no-layout-vis` | off        | Skip layout visualization images                      |
| `--layout-device` | auto       | Device for layout model (`cpu`, `cuda:1`, etc.)       |
| `--set`           | none       | Override config values (dotted path, repeatable)      |
| `--config / -c`   | none       | Path to YAML config override                          |
| `--log-level`     | `INFO`     | `DEBUG` / `INFO` / `WARNING` / `ERROR`                |

---

## Typical Agent Workflow

```
receive document path / URL
       │
       ▼
glmocr.parse(path)            ← single call, handles PDF/image
       │
       ▼
result.to_dict()              ← safe to pass as tool output
       │
       ├── markdown_result    → hand to LLM for reading / summarization
       └── json_result        → structured extraction (tables, formulas, regions by label)
```

### Filter by label

```python
result = glmocr.parse("report.png")
regions = result.json_result[0]  # first page

tables = [r for r in regions if r["label"] == "table"]
formulas = [r for r in regions if r["label"] == "formula"]
body_text = [r for r in regions if r["label"] == "text"]
```

### Multi-page PDF → iterate pages

```python
with GlmOcr(api_key="sk-xxx") as parser:
    result = parser.parse("document.pdf")   # all pages in one PipelineResult
    for page_idx, page_regions in enumerate(result.json_result):
        print(f"Page {page_idx + 1}: {len(page_regions)} regions")
        for region in page_regions:
            print(f"  [{region['label']}] {region['content'][:60]}")
```

### Programmatic config (no env vars)

```python
from glmocr.config import GlmOcrConfig

cfg = GlmOcrConfig.from_env(
    api_key="sk-xxx",
    mode="maas",
    timeout=600,
    log_level="DEBUG",
)
```

---

## Output Directory Layout

After `result.save(output_dir)`:

```
output_dir/
  <image_stem>/
    <image_stem>.json         ← structured regions
    <image_stem>.md           ← full Markdown (with cropped figure images)
    imgs/                     ← cropped figures referenced in Markdown
    layout_vis/               ← layout detection overlay images (if enabled)
      <image_stem>.jpg
```

---

## Flask Service (new)

Run GLM-OCR as an HTTP API service:

```bash
# Install with server support
pip install "glmocr[server]"

# Start service (default port 5002)
python -m glmocr.server

# With debug logging
python -m glmocr.server --log-level DEBUG
```

```bash
# Call API
curl -X POST http://localhost:5002/glmocr/parse \
  -H "Content-Type: application/json" \
  -d '{"images": ["./document.png"]}'
```

- `images` can be a string or a list (list = pages of one document)
- For multiple documents, call the endpoint multiple times

---

## Ollama / MLX Deployment (new)

For specialized hardware:

- **Apple Silicon**: Use [mlx-vlm](https://github.com/zai-org/GLM-OCR/tree/main/examples/mlx-deploy) for optimized inference on Apple Silicon Macs
- **Ollama**: Use [Ollama deployment](https://github.com/zai-org/GLM-OCR/tree/main/examples/ollama-deploy) for simple local deployment

---

## Common Pitfalls

- **`ZHIPU_API_KEY` not set**: SDK defaults to MaaS mode. Without a key, `parse()` will fail with a clear error message and quick-fix instructions. Set via `export ZHIPU_API_KEY=sk-xxx`, add to a `.env` file, or pass `--api-key sk-xxx` to the CLI.
- **Large PDFs**: Default timeout is 600s. For very long documents increase with `timeout=1200`.
- **`result.json_result` is a string**: Happens when the model returns malformed JSON. The SDK preserves the raw string — parse or log it manually.

## 用户确认检查点

以下操作前**必须暂停并询问用户确认**：

| 检查点 | 触发条件 | 确认内容 |
|--------|---------|---------|
| 批量文档解析 | 对目录下多个文件执行 glmocr parse 时 | 确认文件数量和预计 API 调用费用 |
| PDF 页数过多 | 单个 PDF 超过 50 页时 | 提醒处理时间可能较长，建议增加 timeout 参数 |
| 结果质量验证 | OCR 结果用于科研论文数据提取时 | 展示解析结果摘要，让用户确认表格/公式区域识别准确 |
| 自托管模式切换 | 用户要求使用 selfhosted 模式时 | 确认本地已部署 vLLM/SGLang 服务且模型已加载 |

## 错误处理与回退

| 错误场景 | 检测信号 | 回退策略 |
|---------|---------|---------|
| API Key 未配置 | SDK 报错 "ZHIPU_API_KEY not set" | 检查环境变量或 .env 文件，提示用户设置 `export ZHIPU_API_KEY=sk-xxx` |
| 请求超时 | SDK 运行超过 timeout 限制 | 增大 timeout 参数（默认 600s，大文档设 1200s），或拆分文档分页处理 |
| JSON 结果格式异常 | `result.json_result` 为字符串而非列表 | 手动 `json.loads()` 解析，或检查模型返回的原始内容 |
| 图片分辨率不足 | 裁切区域文字模糊无法辨认 | 提高输入图片 DPI，或对 PDF 使用更高 DPI 转换 |
