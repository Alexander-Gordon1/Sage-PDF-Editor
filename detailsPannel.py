from __future__ import annotations

from pathlib import Path
from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout


class DetailsPanel(QFrame):
    """Right-hand panel: shows details about whatever file is selected."""

    PLACEHOLDER_TEXT = "Select a file from the list on the left."

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        self.details_label = QLabel(self.PLACEHOLDER_TEXT)
        self.details_label.setWordWrap(True)
        self.details_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        layout.addWidget(self.details_label)
        layout.addStretch(1)

    def show_file(self, path: Optional[Path]) -> None:
        """Display details for `path`, or the placeholder if None."""
        if path is None:
            self.details_label.setText(self.PLACEHOLDER_TEXT)
            return
        self.details_label.setText(
            f"Selected file:\n\n{path.name}\n\nFull path:\n{path}"
        )

    def show_message(self, message: str) -> None:
        """Display an arbitrary status message (e.g. 'no files found')."""
        self.details_label.setText(message)