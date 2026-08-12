from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QMainWindow, QMessageBox, QSplitter, QWidget

from config import PDF_DIR
from detailsPannel import DetailsPanel #had widgets. infrom 
from fileListPannel import FileListPanel #same as above


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Sage File Editor")
        self.resize(1100, 700)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QHBoxLayout(central_widget)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(12)

        splitter = QSplitter(Qt.Horizontal)
        layout.addWidget(splitter)

        self.file_list_panel = FileListPanel()
        self.details_panel = DetailsPanel()

        splitter.addWidget(self.file_list_panel)
        splitter.addWidget(self.details_panel)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        splitter.setSizes([320, 780])

        self.file_list_panel.file_selected.connect(self.details_panel.show_file)

        self.load_pdf_files()

    def load_pdf_files(self) -> None:
        if not PDF_DIR.exists():
            QMessageBox.warning(
                self,
                "Missing folder",
                f"Could not find the folder:\n{PDF_DIR}",
            )
            return

        pdf_files = sorted(
            (p for p in PDF_DIR.iterdir() if p.is_file() and p.suffix.lower() == ".pdf"),
            key=lambda p: p.name.lower(),
        )

        self.file_list_panel.populate(pdf_files)

        if not pdf_files:
            self.details_panel.show_message("No PDF files were found in PDF_DIR.")