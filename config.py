from pathlib import Path

from utils import resource_path


# This file lives at the project root, alongside main.py and origonalPDFs/.
BASE_DIR = Path(resource_path("."))
PDF_DIR = BASE_DIR / "origonalPDFs"