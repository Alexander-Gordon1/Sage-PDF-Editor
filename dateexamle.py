import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton
)
from PySide6.QtGui import QIntValidator
from PySide6.QtCore import Qt


class SegmentedDateEntry(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Segmented Date Entry Demo")

        outer_layout = QVBoxLayout()
        outer_layout.addWidget(QLabel("Date of Appointment:"))

        row = QHBoxLayout()
        row.setSpacing(6)

        box_style = """
            QLineEdit {
                border: 2px solid black;
                font-size: 18px;
                min-width: 40px;
                max-width: 50px;
                min-height: 40px;
                padding: 0px;
                qproperty-alignment: AlignCenter;
            }
        """

        # Day box
        self.day_box = QLineEdit()
        self.day_box.setMaxLength(2)
        self.day_box.setValidator(QIntValidator(1, 31))
        self.day_box.setAlignment(Qt.AlignCenter)
        self.day_box.setStyleSheet(box_style)
        self.day_box.setPlaceholderText("DD")

        slash1 = QLabel("/")
        slash1.setStyleSheet("font-size: 20px;")

        # Month box
        self.month_box = QLineEdit()
        self.month_box.setMaxLength(2)
        self.month_box.setValidator(QIntValidator(1, 12))
        self.month_box.setAlignment(Qt.AlignCenter)
        self.month_box.setStyleSheet(box_style)
        self.month_box.setPlaceholderText("MM")

        slash2 = QLabel("/")
        slash2.setStyleSheet("font-size: 20px;")

        # Year box
        self.year_box = QLineEdit()
        self.year_box.setMaxLength(4)
        self.year_box.setValidator(QIntValidator(1900, 2100))
        self.year_box.setAlignment(Qt.AlignCenter)
        self.year_box.setStyleSheet(box_style)
        self.year_box.setPlaceholderText("YYYY")

        row.addWidget(self.day_box)
        row.addWidget(slash1)
        row.addWidget(self.month_box)
        row.addWidget(slash2)
        row.addWidget(self.year_box)
        row.addStretch()

        outer_layout.addLayout(row)

        # Auto-advance focus once a box is full
        self.day_box.textChanged.connect(
            lambda text: self._maybe_advance(text, self.day_box, self.month_box, 2)
        )
        self.month_box.textChanged.connect(
            lambda text: self._maybe_advance(text, self.month_box, self.year_box, 2)
        )

        self.result_label = QLabel("")
        outer_layout.addWidget(self.result_label)

        confirm_button = QPushButton("Confirm Date")
        confirm_button.clicked.connect(self.show_selected_date)
        outer_layout.addWidget(confirm_button)

        self.setLayout(outer_layout)

    def _maybe_advance(self, text, current_box, next_box, full_length):
        """Move focus to the next box once current box reaches full_length chars."""
        if len(text) >= full_length:
            next_box.setFocus()
            next_box.selectAll()

    def show_selected_date(self):
        day = self.day_box.text()
        month = self.month_box.text()
        year = self.year_box.text()

        if not (day and month and year):
            self.result_label.setText("Please fill in all fields.")
            return

        formatted = f"{day.zfill(2)}/{month.zfill(2)}/{year}"
        self.result_label.setText(f"Selected date: {formatted}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SegmentedDateEntry()
    window.resize(350, 150)
    window.show()
    sys.exit(app.exec())