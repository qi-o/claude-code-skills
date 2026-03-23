import sys
from pypdf import PdfReader


# Script for Claude to run to determine whether a PDF has fillable form fields. See forms.md.


def main():
    if len(sys.argv) != 2:
        print("Usage: check_fillable_fields.py <pdf_file>")
        sys.exit(1)
    try:
        reader = PdfReader(sys.argv[1])
        if reader.get_fields():
            print("This PDF has fillable form fields")
        else:
            print("This PDF does not have fillable form fields; you will need to visually determine where to enter data")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
