from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QFrame, QLabel, QListWidget, QListWidgetItem, QVBoxLayout


class FileListPanel(QFrame):
    """Left-hand panel: a titled list of files.

    Emits `file_selected` with the selected Path (or None if the
    selection is cleared) whenever the current selection changes.
    """

    file_selected = Signal(object)

    def __init__(self, title: str = "PDF Files", parent=None) -> None:
        super().__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 18px; font-weight: 600;")
        layout.addWidget(title_label)

        self.list_widget = QListWidget()
        self.list_widget.itemSelectionChanged.connect(self._on_selection_changed)
        layout.addWidget(self.list_widget)

    def populate(self, files: list[Path]) -> None:
        """Replace the list contents with the given files."""
        self.list_widget.clear()
        for file_path in files:
            item = QListWidgetItem(file_path.name)
            item.setData(Qt.UserRole, file_path)
            self.list_widget.addItem(item)

        if files:
            self.list_widget.setCurrentRow(0)
        else:
            self.file_selected.emit(None)

    def _on_selection_changed(self) -> None:
        current_item = self.list_widget.currentItem()
        path = current_item.data(Qt.UserRole) if current_item else None
        self.file_selected.emit(path)