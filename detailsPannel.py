from __future__ import annotations

import csv
from pathlib import Path
from typing import Optional
import datetime 

from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QScrollArea,
    QPushButton,
    QMessageBox,
    QWidget,
    QSpacerItem,
    QSizePolicy,
)
from PySide6.QtGui import QIntValidator, QFont

from inputWriteToPDF import open_and_write, colGREEN


class DetailsPanel(QFrame):
    def __init__(self, file_list_panel=None) -> None:
        super().__init__()
        self.setFrameShape(QFrame.StyledPanel)
        
        # Store reference to FileListPanel
        self.file_list_panel = file_list_panel
        
        # Initialize patient data dictionary with common fields
        self.patient_data: dict[str, str] = {
            "NAME": "",
            "DOB": "",
            "ADDRESS1": "",
            "ADDRESS2": "",
            "ADDRESS3": "",
            "POSTCODE": "",
            "PHONE_NUMBER": "",
            "EMAIL_ADDRESS": "",
            "GENDER": "",
            "AGE": "",
            "DATE_OF_APPOINTMENT": datetime.date.today().strftime("%d %m %y"),
            "PREFERRED_GP": "",
            "SURGERY": "",
            "BOTOX_BATCH": "",
            "BOTOX_EXPIRY_DATE": "",
            "IN_NORMAL_SALINE": "",
            "NOK_NAME": "",
            "NOK_RELATIONSHIP": "",
            "NOK_PHONE": "",
            "CONTACT_DETAILS": "",
        }
        
        # Store text box references
        self.text_boxes: dict[str, QLineEdit] = {}
        
        # Store checked files for submit
        self.checked_files: list[Path] = []
        
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(8)
        
        # Title label (will be hidden when no files checked)
        self.title_label = QLabel("Patient Details")
        self.title_label.setStyleSheet("font-size: 18px; font-weight: 600;")
        self.title_label.setVisible(False)
        main_layout.addWidget(self.title_label)
        
        # Scroll area for dynamic text boxes
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        
        # Container widget inside scroll area
        self.scroll_container = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_container)
        self.scroll_layout.setContentsMargins(10, 10, 10, 10)
        self.scroll_layout.setSpacing(8)
        
        self.scroll_area.setWidget(self.scroll_container)
        main_layout.addWidget(self.scroll_area, 1)  # Give scroll area stretch
        
        # Submit button (added to main layout, OUTSIDE scroll area so it doesn't get deleted)
        self.submit_button = QPushButton("Submit")
        self._style_submit_button()
        self.submit_button.clicked.connect(self.on_submit)
        self.submit_button.setVisible(False)
        main_layout.addWidget(self.submit_button)
    
    def _style_submit_button(self) -> None:
        """Style the submit button with green color."""
        # Convert colGREEN tuple to RGB values
        r, g, b = int(colGREEN[0] * 255), int(colGREEN[1] * 255), int(colGREEN[2] * 255)
        self.submit_button.setStyleSheet(
            f"QPushButton {{"
            f"    background-color: rgb({r}, {g}, {b});"
            f"    color: white;"
            f"    font-weight: 600;"
            f"    border: none;"
            f"    border-radius: 4px;"
            f"    padding: 8px 16px;"
            f"}}"
            f"QPushButton:hover {{"
            f"    background-color: rgb({int(r*0.9)}, {int(g*0.9)}, {int(b*0.9)});"
            f"}}"
        )

    
    
    def _load_csv_fields(self, checked_files: list[Path]) -> list[str]:
        """
        Read fileRecordsRequired.csv and extract field names for the given files.
        
        Returns a deduplicated, ordered list of field names from matching rows.
        """
        if not checked_files:
            return []
        
        field_list: list[str] = []
        csv_path = Path("fileRecordsRequired.csv")
        
        if not csv_path.exists():
            print(f"Warning: {csv_path} not found")
            return []
        
        try:
            with open(csv_path, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                for row in reader:
                    if not row:
                        continue
                    
                    # First column is the file name
                    csv_filename = row[0].strip()
                    
                    # Check if this row matches any of the checked files
                    for checked_file in checked_files:
                        if checked_file.name == csv_filename:
                            # Extract fields (columns 2+)
                            fields = [field.strip() for field in row[1:] if field.strip()]
                            field_list.extend(fields)
                            break
            
            # Deduplicate while preserving order
            deduplicated = list(dict.fromkeys(field_list))
            return deduplicated
        
        except Exception as e:
            print(f"Error reading CSV: {e}")
            return []





    #########################
    #blow is elements being created

    #      ---------text boxes being created ------

    def _create_text_boxes(self, field_names: list[str]) -> None:
        """
        Create text boxes for the given field names.
        Clears existing text boxes first.
        """
        # Clear existing widgets from scroll layout
        self._clear_layout(self.scroll_layout)
        
        # Clear text box references
        self.text_boxes.clear()
        
        # Create text boxes for each field
        for field_name in field_names:
            # Create label
            label = QLabel(field_name)
            label.setStyleSheet("font-weight: 600; color: rgb(122, 121, 121);")
            self.scroll_layout.addWidget(label)
            
            # Create text box
            if field_name == "DOB":
                date_row = self.create_date_entry()
                self.scroll_layout.addLayout(date_row)
                self.text_boxes[field_name] = (self.day_box, self.month_box, self.year_box)


            else:

                text_box = QLineEdit()
                text_box.setPlaceholderText(f"Enter {field_name}")
                self.text_boxes[field_name] = text_box
                self.scroll_layout.addWidget(text_box)
        
        # Add vertical spacer at bottom to push content to top
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.scroll_layout.addSpacing(8)
        self.scroll_layout.addItem(spacer)






    # ------- date input boxes ---------

    def create_date_entry(self):
        """Builds a segmented DD/MM/YYYY date entry widget and returns it as a layout."""
        row = QHBoxLayout()
        row.setSpacing(6)

        box_style = """
            QLineEdit {
                border: 2px solid black;
                font-size: 16px;
                max-width: 35px;
                max-height: 30px;
                padding: 5px;
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
        #self.year_box.setStyleSheet(box_style)
        self.year_box.setPlaceholderText("YYYY")
        self.year_box.setStyleSheet(
            """
            QLineEdit {
                    border: 2px solid black;
                    font-size: 16px;
                    max-width: 45px;
                    max-height: 30px;
                    padding: 5px;
                    qproperty-alignment: AlignCenter;
                }
            """)

        row.addWidget(self.day_box)
        row.addWidget(slash1)
        row.addWidget(self.month_box)
        row.addWidget(slash2)
        row.addWidget(self.year_box)
        row.addStretch()

        # Auto-advance focus once a box is full
        self.day_box.textChanged.connect(
            lambda text: self._maybe_advance(text, self.month_box, 2)
        )
        self.month_box.textChanged.connect(
            lambda text: self._maybe_advance(text, self.year_box, 2)
        )

        return row


    def _maybe_advance(self, text, next_box, full_length):
        """Move focus to the next box once the current box reaches full_length chars."""
        if len(text) >= full_length:
            next_box.setFocus()
            next_box.selectAll()

    def get_date_of_appointment(self):
        day = self.day_box.text().zfill(2)
        month = self.month_box.text().zfill(2)
        year = self.year_box.text()
        return f"{day} {month} {year}"


    def _clear_layout(self, layout) -> None:
        """Recursively remove and delete all widgets/sub-layouts from a layout."""
        while layout.count() > 0:
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
            else:
                sub_layout = item.layout()
                if sub_layout:
                    self._clear_layout(sub_layout)



    # -------- end of date input boxes ----------


        
    

    # fetching data from text boxes and date ui to the data dictionary 

    def _sync_data_from_ui(self) -> None:
        
        for field_name, text_box in self.text_boxes.items():
            if field_name != "DOB" :
                self.patient_data[field_name] = text_box.text()

        self.patient_data["DOB"] = self.get_date_of_appointment()


    #checks if all values are empty or not for submission
    def _all_fields_filled(self) -> bool:
        for field_name, text_box in self.text_boxes.items():
            if field_name != "DOB" and text_box.text().strip() == "":
                return False

        # Check DOB as well
        if not self.patient_data.get("DOB"):
            return False

        return True

        


    
    def _handle_empty_state(self) -> None:
        """
        Handle the empty state when no files are checked.
        """
        self._clear_layout(self.scroll_layout)
        
        self.text_boxes.clear()
        self.title_label.setVisible(False)
        self.submit_button.setVisible(False)  # Safe now - button is in main layout, not scroll layout
    
    @Slot(list)
    def on_files_checked(self, checked_files: list[Path]) -> None:
        """
        Called when files are checked/unchecked in FileListPanel.
        Refreshes the form with fields required for the checked files.
        """
        self.checked_files = checked_files
        
        if not checked_files:
            self._handle_empty_state()
            return
        
        # Show title and button
        self.title_label.setVisible(True)
        self.submit_button.setVisible(True)
        
        # Load required fields from CSV
        field_names = self._load_csv_fields(checked_files)
        
        # Create text boxes
        self._create_text_boxes(field_names)
        
        # Reset patient data
        for key in self.patient_data:
            if key != "DATE_OF_APPOINTMENT":  # Keep the default date
                self.patient_data[key] = ""
            
    
    @Slot()
    def on_submit(self) -> None:
        """
        Submit button handler. Syncs data and writes to PDFs.
        """

        # Sync text box values to patient_data
        self._sync_data_from_ui()

        if self._all_fields_filled() != False:
            

            
            
            # Print for debugging
            print(f"Submitting patient data: {self.patient_data}")
            
            # Call open_and_write for each checked file
            try:
                for file_path in self.checked_files:
                    print(f"Writing to {file_path.name}...")
                    open_and_write(file_path.name, self.patient_data)
                
                # Show success message
                QMessageBox.information(
                    self,
                    "Success",
                    f"Successfully wrote data to {len(self.checked_files)} PDF(s)."
                )
                
                # Reset form
                self.on_files_checked(self.checked_files)
            
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Error",
                    f"Error writing to PDFs: {e}"
                )
                print(f"Error: {e}")

        else:
            QMessageBox.critical(
                self,
                "Error",
                "All fields must be filled"
            )
            
    
    @Slot(Path)
    def show_file(self, file_path: Optional[Path]) -> None:
        """
        Legacy method for file selection. Kept for backward compatibility.
        The new form is now driven by the files_checked signal instead.
        """
        # This is now handled by on_files_checked via the files_checked signal
        pass
    
    def show_message(self, message: str) -> None:
        """
        Display a message in the details panel.
        """
        # Clear existing widgets
        self._handle_empty_state()
        
        # Show message
        message_label = QLabel(message)
        message_label.setWordWrap(True)
        message_label.setStyleSheet("color: rgb(122, 121, 121);")
        self.scroll_layout.addWidget(message_label)
        self.scroll_layout.addStretch()
    