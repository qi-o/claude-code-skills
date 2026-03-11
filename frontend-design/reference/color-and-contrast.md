# Color & Contrast Reference

## Color Palette Building

### Dominant + Accent Strategy
- One dominant color (60-70% of visual weight)
- One accent color (10-20%)
- Neutrals for rest

### Color Temperature
- Warm: red, orange, yellow
- Cool: blue, green, purple
- Mix intentionally, avoid accidental mixing

## Accessibility Contrast Ratios

| Level | Requirement |
|-------|-------------|
| AA Normal | 4.5:1 |
| AA Large | 3:1 |
| AAA Normal | 7:1 |
| AAA Large | 4.5:1 |

Large text = 18px+ regular or 14px+ bold

## CSS Custom Properties Example

```css
:root {
  /* Dominant */
  --color-primary: #1a1a2e;
  --color-primary-light: #16213e;

  /* Accent */
  --color-accent: #e94560;
  --color-accent-hover: #ff6b6b;

  /* Neutrals */
  --color-bg: #fafafa;
  --color-bg-alt: #ffffff;
  --color-text: #1a1a2e;
  --color-text-muted: #6b7280;

  /* Semantic */
  --color-success: #10b981;
  --color-warning: #f59e0b;
  --color-error: #ef4444;
  --color-info: #3b82f6;
}
```

## Dark Mode Considerations
- Don't just invert colors
- Reduce contrast slightly in dark mode
- Use desaturated colors for backgrounds
- Maintain brand identity

## Color Psychology
- Red: urgency, passion, energy
- Blue: trust, calm, professional
- Green: growth, health, nature
- Yellow: optimism, attention
- Purple: luxury, creativity
- Orange: enthusiasm, warmth
