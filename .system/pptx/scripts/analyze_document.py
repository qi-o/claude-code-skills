#!/usr/bin/env python3
"""
AI Document Analyzer for PPTX

Analyzes documents (Markdown/TXT/PDF) and generates structured slides_plan.json
using Claude API for intelligent content planning.

Usage:
    python scripts/analyze_document.py document.md --slides 5 --output slides_plan.json
    python scripts/analyze_document.py document.pdf --slides 10
    python scripts/analyze_document.py notes.txt --slides 3 --api-key YOUR_API_KEY
"""

import argparse
import json
import os
import sys
from pathlib import Path

# Try to import required dependencies
try:
    import anthropic
except ImportError:
    print("Error: 'anthropic' package is required.")
    print("Install it with: pip install anthropic")
    sys.exit(1)


def read_document(file_path: str) -> str:
    """Read document content based on file extension."""
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Document not found: {file_path}")

    suffix = path.suffix.lower()

    if suffix == '.pdf':
        try:
            import pymupdf
        except ImportError:
            print("Error: 'pymupdf' package is required for PDF processing.")
            print("Install it with: pip install pymupdf")
            sys.exit(1)

        doc = pymupdf.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text

    elif suffix in ['.md', '.markdown', '.txt', '.text']:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

    else:
        # Try to read as plain text
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            with open(file_path, 'r', encoding='latin-1') as f:
                return f.read()


def analyze_with_claude(content: str, num_slides: int, api_key: str) -> dict:
    """Analyze document content using Claude API and generate slides plan."""

    prompt = f"""You are a PPTX presentation planning assistant. Analyze the following document content and create a structured slides plan for a presentation.

Document Content:
---
{content}
---

Generate a JSON output with exactly {num_slides} slides following this structure:

{{
  "title": "Presentation Title",
  "total_slides": {num_slides},
  "slides": [
    {{
      "slide_number": 1,
      "page_type": "cover",
      "title": "Slide Title",
      "content": "Subtitle or description"
    }},
    {{
      "slide_number": 2,
      "page_type": "content",
      "title": "Slide Title",
      "bullet_points": ["Point 1", "Point 2", "Point 3"]
    }},
    {{
      "slide_number": 3,
      "page_type": "content",
      "title": "Slide Title",
      "content": "Main content text",
      "bullet_points": ["Point 1", "Point 2"]
    }}
  ]
}}

Requirements:
1. First slide should always be a "cover" type with title and subtitle
2. Last slide should be a "thankyou" or "conclusion" type
3. Content slides should have clear, concise bullet points (3-5 items max per slide)
4. Use "page_type" values: "cover", "content", "section", "thankyou", "image"
5. Extract the most important information - don't include everything
6. Title should be a concise, catchy presentation title derived from the content

Respond ONLY with valid JSON, no other text."""

    client = anthropic.Anthropic(api_key=api_key)

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4000,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    # Parse the JSON response
    result_text = response.content[0].text

    # Try to extract JSON from response
    try:
        # First try direct parsing
        result = json.loads(result_text)
    except json.JSONDecodeError:
        # Try to extract JSON from markdown code block
        import re
        json_match = re.search(r'```json\s*(.*?)\s*```', result_text, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group(1))
        else:
            # Try to find JSON without code block markers
            json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group(0))
            else:
                raise ValueError("Could not parse JSON from Claude response")

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Analyze documents and generate PPTX slides plan using AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s document.md --slides 5
  %(prog)s report.pdf --slides 10 --output plan.json
  %(prog)s notes.txt --slides 3 --api-key $ANTHROPIC_API_KEY

Environment:
  ANTHROPIC_API_KEY    API key for Claude (can also use --api-key)
        """
    )

    parser.add_argument(
        'document',
        help="Path to document (Markdown, TXT, or PDF)"
    )

    parser.add_argument(
        '--slides', '-n',
        type=int,
        default=5,
        help="Number of slides to generate (default: 5)"
    )

    parser.add_argument(
        '--output', '-o',
        help="Output JSON file path (default: slides_plan.json)"
    )

    parser.add_argument(
        '--api-key',
        help="Claude API key (or set ANTHROPIC_API_KEY environment variable)"
    )

    parser.add_argument(
        '--model',
        default="claude-sonnet-4-20250514",
        help="Claude model to use (default: claude-sonnet-4-20250514)"
    )

    args = parser.parse_args()

    # Get API key from args or environment
    api_key = args.api_key or os.environ.get('ANTHROPIC_API_KEY')

    if not api_key:
        print("Error: API key is required.")
        print("Set ANTHROPIC_API_KEY environment variable or use --api-key")
        sys.exit(1)

    # Determine output path
    output_path = args.output or "slides_plan.json"

    print(f"Reading document: {args.document}")
    content = read_document(args.document)

    if not content.strip():
        print("Error: Document is empty")
        sys.exit(1)

    print(f"Analyzing content with Claude (generating {args.slides} slides)...")

    try:
        result = analyze_with_claude(content, args.slides, api_key)
    except Exception as e:
        print(f"Error during analysis: {e}")
        sys.exit(1)

    # Write output
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"Slides plan saved to: {output_path}")
    print(f"Title: {result.get('title', 'N/A')}")
    print(f"Total slides: {result.get('total_slides', 0)}")


if __name__ == "__main__":
    main()
