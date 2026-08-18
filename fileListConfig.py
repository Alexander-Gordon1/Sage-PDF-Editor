# pdfListConfig.py
"""Configuration for ordering and grouping the PDF file list."""

from pathlib import Path

PDF_ORDER = {
    "Botox consent form 2025.pdf": 0,
    "Filler Consent 2025.pdf": 1,
    "GDPR Notice for signature.pdf": 2,
    "Photographic consent form.pdf": 3,
    "COVID Pre assessment.pdf": 4,
    "GP Information existing patients.pdf": 5,
    "Continuation Sheet.pdf": 6,
    "Injectable patient notes PRINT INSTRUCTIONS 2 sheets per page plus single hairline border.pdf": 7,
    "Next of Kin existing patients form .pdf": 8,
    "Private Prescription Blank.pdf": 9,
    "Sage Demographics and medical History sheet combo.pdf": 10,
    "Sage MS Consent Form V 1.pdf": 11,
}

DIVIDER_AFTER = 4  # divider appears after this many ordered files


def sorted_pdf_files(files: list[Path]) -> list[Path]:
    """Sort PDFs by PDF_ORDER; unlisted files fall back to alphabetical, appended at the end."""
    max_order = len(PDF_ORDER)
    return sorted(
        files,
        key=lambda p: (PDF_ORDER.get(p.name, max_order), p.name.lower()),
    )