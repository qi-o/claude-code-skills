# Output Directory Specification

## Root Output Directory

All generated assets are saved to `minimax-output/` relative to the current working directory where the skill was invoked.

## Subdirectory Structure

```
minimax-output/
├── tmp/                    # Intermediate files
│   ├── cover.html
│   ├── cover.pdf
│   └── ...
├── audio/                  # TTS and music outputs
│   ├── narration.mp3
│   └── background_music.mp3
├── images/                 # Generated images
│   ├── hero.png
│   └── character.png
├── video/                  # Generated videos
│   ├── scene1.mp4
│   └── animation.mp4
└── final/                  # Final deliverables (merged/compiled)
    └── presentation.mp4
```

## File Naming

- Use descriptive names with underscores: `hero_image_16x9.png`
- Include dimensions in name if relevant: `character_portrait_512x512.png`
- Timestamps optional for unique versions: `hero_v2_20240101.png`

## Cleanup

The `tmp/` directory should be cleaned up after final deliverables are created. Do not auto-delete — leave to user discretion.
