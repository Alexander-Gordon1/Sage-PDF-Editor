from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt, Signal, QEvent
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QFrame, QLabel, QListWidget, QListWidgetItem, QVBoxLayout, QWidget


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
        title_label.setStyleSheet("font-size: 24px; font-weight: 600;")
        layout.addWidget(title_label)

        self.list_widget = QListWidget()
        self.list_widget.itemSelectionChanged.connect(self._on_selection_changed)
        self.list_widget.itemChanged.connect(self._on_item_changed)
        self.list_widget.itemClicked.connect(self._on_item_clicked)

        layout.addWidget(self.list_widget)

        # Cached copy of the checked files, kept in sync via _on_item_changed
        # and populate(). Other UI files should read this through the
        # `checked_files` property (or by listening to `files_checked`)
        # rather than reaching into list_widget directly.
        self._checked_files: list[Path] = []

    # ------------------------------------------------------------------
    # Population
    # ------------------------------------------------------------------

    def populate(self, files: list[Path]) -> None:
        self.list_widget.blockSignals(True)
        self.list_widget.clear()

        for index, file_path in enumerate(files):
            if index == 0:
                self._add_section_header("The Essentials")
            if index == 4:
                self._add_section_header("Botox")
            if index == 8:
                self._add_section_header("Filler")

            self.list_widget.addItem(self._make_file_item(file_path))

        self.list_widget.blockSignals(False)

        if files:
            self.list_widget.setCurrentRow(0)
        else:
            self.file_selected.emit(None)

        self._checked_files = []
        self.files_checked.emit(self._checked_files)

    # ------------------------------------------------------------------
    # Row builders — each returns/adds exactly one kind of row.
    # Keeping these separate from populate() means populate() only
    # has to describe *order*, not construction detail.
    # ------------------------------------------------------------------

    def _add_section_header(self, text: str) -> None:
        """Adds a single row combining a section title and a divider line beneath it."""
        header_item = QListWidgetItem()
        header_item.setFlags(Qt.NoItemFlags)  # not selectable/checkable/clickable
        self.list_widget.addItem(header_item)

        header_widget = self._make_section_header_widget(text)
        header_item.setSizeHint(header_widget.sizeHint())
        self.list_widget.setItemWidget(header_item, header_widget)

    def _make_section_header_widget(self, text: str) -> QWidget:
        """A bold title with a divider line beneath it, used to mark the start of a group."""
        container = QWidget()
        container.setAutoFillBackground(True)
        container.setStyleSheet("background-color: palette(base);")  # blocks hover highlight showing through

        layout = QVBoxLayout(container)
        layout.setContentsMargins(4, 10, 4, 5)  # left, top, right, bottom
        layout.setSpacing(4)

        label = QLabel(text)
        label.setStyleSheet("font-weight: 600; font-size: 16px;")
        layout.addWidget(label)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line)

        return container

    def _make_file_item(self, file_path: Path) -> QListWidgetItem:
        """Builds a single checkable list item for a file."""
        item = QListWidgetItem(file_path.name)
        item.setData(Qt.UserRole, file_path)
        item.setFlags(item.flags() | Qt.ItemIsUserCheckable)  # makes the checkbox appear
        item.setCheckState(Qt.Unchecked)
        # Increase font size
        font = QFont()
        font.setPointSize(15)
        item.setFont(font)
        return item

    
    # is slighty redundant but can use if you want to add divider with no title
    def _add_divider(self) -> None:
        """Adds a padded horizontal divider row to the list widget."""
        divider_item = QListWidgetItem()
        divider_item.setFlags(Qt.NoItemFlags)  # not selectable/checkable/clickable
        self.list_widget.addItem(divider_item)

        divider_widget = self._make_divider_widget()
        divider_item.setSizeHint(divider_widget.sizeHint())
        self.list_widget.setItemWidget(divider_item, divider_widget)

    def _make_divider_widget(self) -> QWidget:
        """A horizontal line with padding above and below, for use as a list separator."""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 10, 0, 5)  # left, top, right, bottom
        layout.setSpacing(0)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line)

        return container

    # ------------------------------------------------------------------
    # Checked-files tracking
    # ------------------------------------------------------------------

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

    def _refresh_checked_files(self) -> list[Path]:
        """Recomputes the checked list from the widget state and caches it."""
        result = []
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            # Title/divider rows have no Path in UserRole — skip them so they
            # can never end up in the checked-files list.
            if item.data(Qt.UserRole) is not None and item.checkState() == Qt.Checked:
                result.append(item.data(Qt.UserRole))
        self._checked_files = result
        return result

    # ------------------------------------------------------------------
    # Signal handlers
    # ------------------------------------------------------------------

    def _on_selection_changed(self) -> None:
        """Fires when the highlighted row changes; emits the Path of that row (or None)."""
        current_item = self.list_widget.currentItem()
        path = current_item.data(Qt.UserRole) if current_item else None
        self.file_selected.emit(path)

    def _on_item_changed(self, item: QListWidgetItem) -> None:
        """
        Fires when an item's checkbox is toggled; updates the stored list and
        emits the updated checked list.
        (itemChanged also fires on text edits, but items here aren't editable,
        so in practice this only fires on check-state changes.)
        """
        self.files_checked.emit(self._refresh_checked_files())

    def _on_item_clicked(self, item: QListWidgetItem) -> None:
        """Fires when a row is clicked anywhere (not just the checkbox) — toggles its check state."""
        if item.data(Qt.UserRole) is None:
            return  # title/divider rows aren't clickable files
        if item.checkState() == Qt.Checked:
            item.setCheckState(Qt.Unchecked)
        else:
            item.setCheckState(Qt.Checked)