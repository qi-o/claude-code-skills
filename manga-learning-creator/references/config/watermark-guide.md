---
name: watermark-guide
description: Watermark configuration guide for baoyu-comic
---

# Watermark Guide

## Position Diagram

```
鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
鈹?                 [top-right]鈹?鈫?Avoid (conflicts with page numbers)
鈹?                            鈹?
鈹?                            鈹?
鈹?      COMIC PAGE CONTENT    鈹?
鈹?                            鈹?
鈹?                            鈹?
鈹俒bottom-left][bottom-center][bottom-right]鈹?
鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
```

## Position Recommendations

| Position | Best For | Avoid When |
|----------|----------|------------|
| `bottom-right` | Default choice, works with most panel layouts | Key panel in bottom-right |
| `bottom-left` | Right-heavy layouts | Key panel in bottom-left |
| `bottom-center` | Webtoon vertical scroll, centered designs | Text-heavy bottom area |
| `top-right` | **Not recommended for comics** | Always - conflicts with page numbers |

## Content Format

| Format | Example | Style |
|--------|---------|-------|
| Handle | `@username` | Social media style |
| Text | `Studio Name` | Professional branding |
| Chinese | `婕敾宸ヤ綔瀹 | Chinese market |
| Initials | `ABC` | Minimal, clean |

## Best Practices for Comics

1. **Panel-aware placement**: Avoid placing over speech bubbles or key action
2. **Consistency**: Use same watermark across all pages in comic
3. **Size**: Keep subtle - should not distract from storytelling
4. **Style matching**: Watermark style should complement comic's visual style
5. **Webtoon special**: Use `bottom-center` for vertical scroll format

## Prompt Integration

When watermark is enabled, add to image generation prompt:

```
Include a subtle watermark "[content]" positioned at [position].
The watermark should be legible but not distracting from the comic panels
and storytelling. Ensure watermark does not overlap speech bubbles or key action.
```

## Common Issues

| Issue | Solution |
|-------|----------|
| Watermark invisible on dark panels | Adjust contrast or add subtle outline |
| Watermark overlaps speech bubble | Change position or lower on page |
| Watermark inconsistent across pages | Use session ID for consistency |
| Watermark too prominent | Change position or reduce size |
| Conflicts with page number | Never use top-right position |
