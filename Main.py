import sys
import platform
from pathlib import Path

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

from mainWindow import MainWindow


def main() -> int:
    app = QApplication(sys.argv)
    
    # Set application icon at the app level for Windows taskbar
    assets_dir = Path(__file__).resolve().parent / "assets"
    
    # Choose icon based on OS
    if platform.system() == "Darwin":  # macOS
        icon_path = assets_dir / "sage_logo.icns"
    else:  # Windows and Linux
        icon_path = assets_dir / "sage_logo.ico"
    
    # Fallback to PNG if OS-specific icon not found
    if not icon_path.exists():
        icon_path = assets_dir / "sage_logo.png"
    
    if icon_path.exists():
        app.setApplicationDisplayName("Sage File Editor")
        app.setWindowIcon(QIcon(str(icon_path)))
    
    # Ignore OS styling (dark mode) and use a light theme
    app.setStyle('Fusion')
    
    # Set a light color palette
    from PySide6.QtGui import QPalette, QColor
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(255, 255, 255))
    palette.setColor(QPalette.WindowText, QColor(0, 0, 0))
    palette.setColor(QPalette.Base, QColor(255, 255, 255))
    palette.setColor(QPalette.AlternateBase, QColor(240, 240, 240))
    palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
    palette.setColor(QPalette.ToolTipText, QColor(0, 0, 0))
    palette.setColor(QPalette.Text, QColor(0, 0, 0))
    palette.setColor(QPalette.Button, QColor(240, 240, 240))
    palette.setColor(QPalette.ButtonText, QColor(0, 0, 0))
    palette.setColor(QPalette.BrightText, QColor(255, 255, 255))
    palette.setColor(QPalette.Link, QColor(0, 0, 255))
    palette.setColor(QPalette.Highlight, QColor(0, 120, 215))
    palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
    app.setPalette(palette)
    
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())