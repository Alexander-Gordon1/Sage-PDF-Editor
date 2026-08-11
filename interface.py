from pathlib import Path
import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QSplitter,
    QVBoxLayout,
    QWidget,
)


BASE_DIR = Path(__file__).resolve().parent
PDF_DIR = BASE_DIR / "origonalPDFs"


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

        left_panel = QFrame()
        left_panel.setFrameShape(QFrame.StyledPanel)
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(12, 12, 12, 12)
        left_layout.setSpacing(8)

        title = QLabel("PDF Files")
        title.setStyleSheet("font-size: 18px; font-weight: 600;")
        left_layout.addWidget(title)

        self.file_list = QListWidget()
        self.file_list.itemSelectionChanged.connect(self.show_selected_file)
        left_layout.addWidget(self.file_list)

        right_panel = QFrame()
        right_panel.setFrameShape(QFrame.StyledPanel)
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(20, 20, 20, 20)
        right_layout.setSpacing(12)

        self.details_label = QLabel("Select a file from the list on the left.")
        self.details_label.setWordWrap(True)
        self.details_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        right_layout.addWidget(self.details_label)
        right_layout.addStretch(1)

        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        splitter.setSizes([320, 780])

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
            [path for path in PDF_DIR.iterdir() if path.is_file() and path.suffix.lower() == ".pdf"],
            key=lambda path: path.name.lower(),
        )

        for pdf_file in pdf_files:
            item = QListWidgetItem(pdf_file.name)
            item.setData(Qt.UserRole, pdf_file)
            self.file_list.addItem(item)

        if pdf_files:
            self.file_list.setCurrentRow(0)
        else:
            self.details_label.setText("No PDF files were found in origonalPDFs.")

    def show_selected_file(self) -> None:
        current_item = self.file_list.currentItem()
        if current_item is None:
            self.details_label.setText("Select a file from the list on the left.")
            return

        pdf_path = current_item.data(Qt.UserRole)
        self.details_label.setText(
            f"Selected file:\n\n{pdf_path.name}\n\nFull path:\n{pdf_path}"
        )


def main() -> int:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())