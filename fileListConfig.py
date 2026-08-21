# pdfListConfig.py
"""Configuration for ordering and grouping the PDF file list."""

from pathlib import Path

PDF_ORDER = {
    "Botox consent form.pdf": 0,
    "Continuation sheet.pdf": 1,
    "Filler Consent.pdf": 2,
    "GDPR Consent.pdf": 3,
    "Injectable patient notes AUTOFORM PRINT INSTRUCTIONS 2 sheets per page plus single hairline border copy.pdf": 4,
    "MS Safer Surgery and op notes.pdf": 5,
    "Photographic consent.pdf": 6,
    "Private Px clarithro Mogs Blank.pdf": 7,
    "Sage Demographics PMHx GP NOK.pdf": 8,
    "Sage Dermoscopy Consultation & consent.pdf": 9,
    "Sage MinSurg Consent.pdf": 10,
}

DIVIDER_AFTER = 4  # divider appears after this many ordered files


def sorted_pdf_files(files: list[Path]) -> list[Path]:
    """Sort PDFs by PDF_ORDER; unlisted files fall back to alphabetical, appended at the end."""
    max_order = len(PDF_ORDER)
    return sorted(
        files,
        key=lambda p: (PDF_ORDER.get(p.name, max_order), p.name.lower()),
    )