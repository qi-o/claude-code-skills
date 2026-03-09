#!/usr/bin/env python3
"""
HTML Preview Generator for PPTX

Converts PPTX files to interactive HTML previews with keyboard navigation,
animations, and fullscreen mode.

Usage:
    python scripts/generate_preview.py output.pptx --output preview.html
    python scripts/generate_preview.py presentation.pptx --theme dark
    python scripts/generate_preview.py deck.pptx --title "My Presentation"
"""

import argparse
import json
import os
import sys
import zipfile
import base64
from pathlib import Path
from io import BytesIO

# Try to import required dependencies
try:
    from PIL import Image
except ImportError:
    print("Error: 'Pillow' package is required.")
    print("Install it with: pip install Pillow")
    sys.exit(1)


def extract_pptx_content(pptx_path: str) -> dict:
    """Extract slide content from PPTX file."""

    slides_data = []

    with zipfile.ZipFile(pptx_path, 'r') as zip_ref:
        # Get list of slide files
        slide_files = sorted([
            f for f in zip_ref.namelist()
            if f.startswith('ppt/slides/slide') and f.endswith('.xml')
        ])

        # Get theme colors if available
        theme_colors = extract_theme_colors(zip_ref)

        for slide_file in slide_files:
            slide_num = int(slide_file.split('slide')[1].split('.')[0])

            # Try to extract thumbnail or render slide
            slide_content = extract_slide_content(zip_ref, slide_file, slide_num)

            slides_data.append({
                'slide_number': slide_num,
                'content': slide_content
            })

    return {
        'slides': slides_data,
        'theme_colors': theme_colors,
        'total_slides': len(slides_data)
    }


def extract_theme_colors(zip_ref) -> dict:
    """Extract theme colors from PPTX if available."""

    colors = {
        'primary': '1E2761',
        'secondary': 'CADCFC',
        'accent': 'FFFFFF'
    }

    try:
        # Look for theme files
        theme_files = [f for f in zip_ref.namelist() if 'theme/theme' in f.lower()]

        if theme_files:
            import xml.etree.ElementTree as ET

            theme_xml = zip_ref.read(theme_files[0])

            # Try to extract colors from theme
            # This is a simplified extraction
            pass

    except Exception:
        pass

    return colors


def extract_slide_content(zip_ref, slide_file: str, slide_num: int) -> dict:
    """Extract content from a single slide."""

    content = {
        'title': '',
        'text_content': [],
        'images': []
    }

    try:
        import xml.etree.ElementTree as ET

        slide_xml = zip_ref.read(slide_file)
        root = ET.fromstring(slide_xml)

        # Define namespaces
        namespaces = {
            'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
            'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
            'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
        }

        # Extract title (usually in shape with txBody)
        titles = root.findall('.//p:sp/p:nvSpPr/p:cNvPr', namespaces)
        for title in titles:
            title_text = title.get('descr', '')
            if title_text and not content['title']:
                content['title'] = title_text

        # Extract text content
        text_elements = root.findall('.//a:t', namespaces)
        for elem in text_elements:
            if elem.text:
                content['text_content'].append(elem.text)

        # Extract images
        media_files = [f for f in zip_ref.namelist()
                      if f'ppt/media/slide{slide_num}' in f or f'ppt/media/image' in f]

        for media_file in media_files:
            try:
                image_data = zip_ref.read(media_file)
                ext = Path(media_file).suffix.lower()

                if ext in ['.png', '.jpg', '.jpeg', '.gif']:
                    mime_type = f'image/{ext[1:]}'
                    if ext == '.jpg':
                        mime_type = 'image/jpeg'

                    content['images'].append({
                        'name': Path(media_file).name,
                        'data': base64.b64encode(image_data).decode('utf-8'),
                        'mime_type': mime_type
                    })
            except Exception:
                pass

    except Exception as e:
        content['error'] = str(e)

    return content


def generate_html(pptx_data: dict, args) -> str:
    """Generate HTML preview from PPTX data."""

    slides = pptx_data['slides']
    theme = pptx_data.get('theme_colors', {})

    html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
            background: #1a1a2e;
            color: #eee;
            overflow: hidden;
            height: 100vh;
        }}

        .presentation {{
            width: 100%;
            height: 100vh;
            display: flex;
            flex-direction: column;
        }}

        .slide-container {{
            flex: 1;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
            position: relative;
        }}

        .slide {{
            width: {slide_width};
            height: {slide_height};
            background: white;
            border-radius: 8px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.5);
            position: absolute;
            opacity: 0;
            transform: translateX(100px);
            transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
            overflow: hidden;
        }}

        .slide.active {{
            opacity: 1;
            transform: translateX(0);
        }}

        .slide.prev {{
            transform: translateX(-100px);
        }}

        .slide-content {{
            padding: 40px;
            height: 100%;
            display: flex;
            flex-direction: column;
            background: linear-gradient(135deg, {primary_color} 0%, {secondary_color} 100%);
        }}

        .slide-title {{
            font-size: 28px;
            font-weight: bold;
            color: {accent_color};
            margin-bottom: 20px;
        }}

        .slide-text {{
            font-size: 16px;
            color: #333;
            line-height: 1.6;
            flex: 1;
        }}

        .slide-text ul {{
            list-style: none;
            padding: 0;
        }}

        .slide-text li {{
            padding: 8px 0;
            padding-left: 20px;
            position: relative;
        }}

        .slide-text li::before {{
            content: "•";
            color: {accent_color};
            position: absolute;
            left: 0;
            font-weight: bold;
        }}

        .slide-image {{
            max-width: 100%;
            max-height: 200px;
            object-fit: contain;
            margin: 10px 0;
            border-radius: 4px;
        }}

        .progress-bar {{
            height: 4px;
            background: rgba(255,255,255,0.2);
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            z-index: 100;
        }}

        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, {accent_color}, {secondary_color});
            transition: width 0.3s ease;
        }}

        .controls {{
            position: fixed;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            gap: 10px;
            z-index: 100;
        }}

        .control-btn {{
            background: rgba(255,255,255,0.1);
            border: 1px solid rgba(255,255,255,0.2);
            color: white;
            padding: 10px 20px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
            transition: all 0.2s;
        }}

        .control-btn:hover {{
            background: rgba(255,255,255,0.2);
        }}

        .control-btn.active {{
            background: {accent_color};
            color: {primary_color};
        }}

        .slide-counter {{
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: rgba(0,0,0,0.5);
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 14px;
            z-index: 100;
        }}

        .fullscreen-btn {{
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 100;
        }}

        .help-text {{
            position: fixed;
            top: 20px;
            left: 20px;
            background: rgba(0,0,0,0.5);
            padding: 8px 16px;
            border-radius: 6px;
            font-size: 12px;
            color: #aaa;
            z-index: 100;
        }}

        @media (max-width: 768px) {{
            .slide {{
                width: 95%;
                height: auto;
                aspect-ratio: 16/9;
            }}

            .slide-content {{
                padding: 20px;
            }}

            .slide-title {{
                font-size: 20px;
            }}
        }}
    </style>
</head>
<body>
    <div class="progress-bar">
        <div class="progress-fill" id="progress"></div>
    </div>

    <div class="help-text">
        ← → Space: Navigate | F: Fullscreen | ESC: Exit
    </div>

    <div class="presentation">
        <div class="slide-container" id="slide-container">
            {slides_html}
        </div>
    </div>

    <div class="controls">
        <button class="control-btn" onclick="prevSlide()">← Previous</button>
        <button class="control-btn" onclick="toggleFullscreen()">⛶ Fullscreen</button>
        <button class="control-btn" onclick="nextSlide()">Next →</button>
    </div>

    <div class="slide-counter">
        <span id="current-slide">1</span> / <span id="total-slides">{total_slides}</span>
    </div>

    <script>
        let currentSlide = 0;
        const slides = document.querySelectorAll('.slide');
        const totalSlides = slides.length;

        function showSlide(index) {{
            slides.forEach((slide, i) => {{
                slide.classList.remove('active', 'prev');
                if (i === index) {{
                    slide.classList.add('active');
                }} else if (i < index) {{
                    slide.classList.add('prev');
                }}
            }});

            document.getElementById('current-slide').textContent = index + 1;
            document.getElementById('progress').style.width = ((index + 1) / totalSlides * 100) + '%';
        }}

        function nextSlide() {{
            if (currentSlide < totalSlides - 1) {{
                currentSlide++;
                showSlide(currentSlide);
            }}
        }}

        function prevSlide() {{
            if (currentSlide > 0) {{
                currentSlide--;
                showSlide(currentSlide);
            }}
        }}

        function toggleFullscreen() {{
            if (!document.fullscreenElement) {{
                document.documentElement.requestFullscreen();
            }} else {{
                document.exitFullscreen();
            }}
        }}

        document.addEventListener('keydown', (e) => {{
            switch(e.key) {{
                case 'ArrowRight':
                case ' ':
                    e.preventDefault();
                    nextSlide();
                    break;
                case 'ArrowLeft':
                    prevSlide();
                    break;
                case 'f':
                case 'F':
                    toggleFullscreen();
                    break;
                case 'Escape':
                    if (document.fullscreenElement) {{
                        document.exitFullscreen();
                    }}
                    break;
            }}
        }});

        // Initialize
        showSlide(0);
    </script>
</body>
</html>"""

    # Generate slides HTML
    slides_html = []
    primary = theme.get('primary', '1E2761')
    secondary = theme.get('secondary', 'CADCFC')
    accent = theme.get('accent', 'FFFFFF')

    for slide_data in slides:
        content = slide_data['content']
        title = content.get('title', f'Slide {slide_data["slide_number"]}')
        text_items = content.get('text_content', [])

        # Build text HTML
        text_html = '<ul>'
        for item in text_items[:10]:  # Limit to 10 items
            text_html += f'<li>{item}</li>'
        text_html += '</ul>'

        # Build images HTML
        images_html = ''
        for img in content.get('images', []):
            images_html += f'<img class="slide-image" src="data:{img["mime_type"]};base64,{img["data"]}" alt="Slide image">'

        slide_html = f'''
            <div class="slide">
                <div class="slide-content">
                    <div class="slide-title">{title}</div>
                    <div class="slide-text">
                        {images_html}
                        {text_html}
                    </div>
                </div>
            </div>
        '''
        slides_html.append(slide_html)

    # Format HTML
    html = html_template.format(
        title=args.title or 'PPTX Preview',
        slide_width='960px',
        slide_height='540px',
        primary_color=f'#{primary}',
        secondary_color=f'#{secondary}',
        accent_color=f'#{accent}',
        slides_html=''.join(slides_html),
        total_slides=len(slides)
    )

    return html


def main():
    parser = argparse.ArgumentParser(
        description="Generate HTML preview from PPTX file",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s output.pptx --output preview.html
  %(prog)s presentation.pptx --title "My Presentation"
  %(prog)s deck.pptx --theme dark

Note: This creates a simplified HTML preview. For full visual accuracy,
      convert to PDF and images first:
      python scripts/office/soffice.py --headless --convert-to pdf input.pptx
        """
    )

    parser.add_argument(
        'pptx',
        help="Path to PPTX file"
    )

    parser.add_argument(
        '--output', '-o',
        help="Output HTML file path (default: preview.html)"
    )

    parser.add_argument(
        '--title',
        help="Presentation title for HTML"
    )

    parser.add_argument(
        '--theme',
        choices=['light', 'dark'],
        default='dark',
        help="HTML theme (default: dark)"
    )

    args = parser.parse_args()

    # Check file exists
    if not os.path.exists(args.pptx):
        print(f"Error: File not found: {args.pptx}")
        sys.exit(1)

    # Determine output path
    output_path = args.output or "preview.html"

    print(f"Extracting content from: {args.pptx}")

    try:
        pptx_data = extract_pptx_content(args.pptx)
    except Exception as e:
        print(f"Error reading PPTX: {e}")
        sys.exit(1)

    print(f"Found {pptx_data['total_slides']} slides")

    # Generate HTML
    html_content = generate_html(pptx_data, args)

    # Write output
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"HTML preview saved to: {output_path}")
    print("Open in browser to view. Use arrow keys or space to navigate.")


if __name__ == "__main__":
    main()
