# PPTX Style Presets

This directory contains predefined style configurations for creating professional PowerPoint presentations.

## Usage

Load a style preset in your PptxGenJS code:

```javascript
const fs = require('fs');

// Load style preset
const style = JSON.parse(fs.readFileSync('./styles/midnight-executive.json', 'utf8'));

// Use in your presentation
let pres = new pptxgen();
pres.title = style.name;

// Apply colors
let slide = pres.addSlide();
slide.background = { color: style.colors.primary };
slide.addText("Title", {
  fontFace: style.fonts.header,
  color: style.colors.accent
});
```

## Available Presets

| Preset | Description | Best For |
|--------|-------------|----------|
| `midnight-executive.json` | Deep navy with ice blue | Corporate, executive |
| `forest-moss.json` | Nature-inspired green | Environmental, wellness |
| `coral-energy.json` | Vibrant coral and gold | Startup, energetic |
| `warm-terracotta.json` | Earthy terracotta tones | Food, hospitality |
| `ocean-gradient.json` | Deep blue to teal | Tech, marine |
| `charcoal-minimal.json` | Clean monochrome | Minimalist, modern |
| `teal-trust.json` | Fresh teal palette | Healthcare, finance |
| `berry-cream.json` | Rich berry with cream | Fashion, lifestyle |
| `sage-calm.json` | Soft sage greens | Wellness, calm |
| `cherry-bold.json` | Bold cherry red | Bold statements |

## Style Structure

Each preset is a JSON file with:

```json
{
  "name": "Preset Name",
  "description": "Use case description",
  "colors": {
    "primary": "#1E2761",
    "secondary": "#CADCFC",
    "accent": "#FFFFFF"
  },
  "fonts": {
    "header": "Arial Black",
    "body": "Arial"
  },
  "layout": "cards",
  "background": "gradient"
}
```

### Fields

- **name**: Display name of the preset
- **description**: Brief description of use cases
- **colors.primary**: Main background color (hex without #)
- **colors.secondary**: Secondary/accent background
- **colors.accent**: Text and highlight color
- **fonts.header**: Font for titles and headers
- **fonts.body**: Font for body text
- **layout**: Suggested layout type (cards, grid, split)
- **background**: Background style (solid, gradient, image)

## Creating Custom Presets

Copy an existing preset and modify the values to create your own:

1. Choose a preset closest to your needs
2. Adjust colors to match your brand
3. Update fonts if needed
4. Save as `your-custom-style.json`
