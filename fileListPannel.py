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

        # Cached copy of the checked files, kept in sync via _on_item_changed
        # and populate(). Other UI files should read this through the
        # `checked_files` property (or by listening to `files_checked`)
        # rather than reaching into list_widget directly.
        self._checked_files: list[Path] = []

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

        # New file list means nothing is checked yet.
        self._checked_files = []
        self.files_checked.emit(self._checked_files)

    @property
    def checked_files(self) -> list[Path]:
        """The Paths of all currently-checked items.

        This is the accessor other UI files should use, e.g.:

            from file_list_panel import FileListPanel
            panel = FileListPanel()
            ...
            selected = panel.checked_files          # read whenever you need it
            panel.files_checked.connect(on_change)  # or react live to changes
        """
        return list(self._checked_files)

    # Recomputes the checked list from the widget state and caches it.
    def _refresh_checked_files(self) -> list[Path]:
        result = []
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            if item.checkState() == Qt.Checked:
                result.append(item.data(Qt.UserRole))
        self._checked_files = result
        return result

    # Fires when the highlighted row changes; emits the Path of that row (or None).
    def _on_selection_changed(self) -> None:
        current_item = self.list_widget.currentItem()
        path = current_item.data(Qt.UserRole) if current_item else None
        self.file_selected.emit(path)

    # Fires when an item's checkbox is toggled; updates the stored list and
    # emits the updated checked list.
    # (itemChanged also fires on text edits, but items here aren't editable,
    # so in practice this only fires on check-state changes.)
    def _on_item_changed(self, item: QListWidgetItem) -> None:
        self.files_checked.emit(self._refresh_checked_files())