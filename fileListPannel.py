from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QFrame, QLabel, QListWidget, QListWidgetItem, QVBoxLayout


# Left-hand panel: a titled list of files with checkboxes.
# Emits file_selected with the currently highlighted Path (or None)
# whenever the current selection changes.
# Emits files_checked with the list of Paths whose checkboxes are
# checked, whenever any checkbox is toggled.
class FileListPanel(QFrame):

    file_selected = Signal(object)
    files_checked = Signal(list)

    # Builds the panel UI: title label + list widget, and connects signals.
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
        self.list_widget.itemChanged.connect(self._on_item_changed)
        layout.addWidget(self.list_widget)

    # Replaces the list contents with the given files, each with an
    # unchecked checkbox, and selects the first row if any files exist.
    def populate(self, files: list[Path]) -> None:
        self.list_widget.blockSignals(True)  # avoid firing itemChanged per row while building the list
        self.list_widget.clear()
        for file_path in files:
            item = QListWidgetItem(file_path.name)
            item.setData(Qt.UserRole, file_path)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)  # makes the checkbox appear
            item.setCheckState(Qt.Unchecked)
            self.list_widget.addItem(item)
        self.list_widget.blockSignals(False)

        if files:
            self.list_widget.setCurrentRow(0)
        else:
            self.file_selected.emit(None)
        self.files_checked.emit([])

    # Returns the Paths of all currently-checked items.
    def checked_files(self) -> list[Path]:
        result = []
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            if item.checkState() == Qt.Checked:
                result.append(item.data(Qt.UserRole))
        return result

    # Fires when the highlighted row changes; emits the Path of that row (or None).
    def _on_selection_changed(self) -> None:
        current_item = self.list_widget.currentItem()
        path = current_item.data(Qt.UserRole) if current_item else None
        self.file_selected.emit(path)

    # Fires when an item's checkbox is toggled; emits the updated checked list.
    # (itemChanged also fires on text edits, but items here aren't editable,
    # so in practice this only fires on check-state changes.)
    def _on_item_changed(self, item: QListWidgetItem) -> None:
        self.files_checked.emit(self.checked_files())