import os
import xml.etree.ElementTree as ET
from PySide6.QtGui import QPalette, QColor
from pathlib import Path

class ThemeManager:
    """
    ThemeManager
    -------------
    • Loads theme XML files
    • Applies Qt palette colours
    • Generates QSS from theme palette
    """

    def __init__(self, theme_dir):
        self.theme_dir = Path(theme_dir)
        self.current_theme = None
        self.palette = {}
        self.colors = {}

    @property
    def current_theme_name(self):
        """Alias for UI components expecting 'current_theme_name'."""
        return getattr(self, "current_theme", "unknown")

    # ----------------------------------------------------------
    # Load / Parse
    # ----------------------------------------------------------
    def load_theme(self, theme_name):
        theme_path = self.theme_dir / f"{theme_name}.xml"
        if not theme_path.exists():
            print(f"[THEME] Theme file not found: {theme_path}")
            return

        import xml.etree.ElementTree as ET
        tree = ET.parse(theme_path)
        root = tree.getroot()

        self.colors = {}
        for color in root.findall("color"):
            key = color.get("name")
            val = color.text.strip() if color.text else None
            if key and val:
                self.colors[key] = val
                print(f"[DEBUG] Theme colors = {self.colors}")

        self.current_theme = theme_name
        print(f"[THEME] Loaded {theme_name}")

        # --------------------------------------------------------
    # Convenience listings for UI
    # --------------------------------------------------------
    def list_themes(self):
        """Return a list of available theme filenames (without extension)."""
        if not self.theme_dir.exists():
            return []
        return [f.stem for f in self.theme_dir.glob("*.xml")]

    def list_fonts(self):
        """Return a list of font files available in the fonts folder."""
        fonts_dir = self.theme_dir.parent / "fonts"
        if not fonts_dir.exists():
            return []
        return [f.name for f in fonts_dir.glob("*.ttf")]


    # ----------------------------------------------------------
    # Apply to QApplication
    # ----------------------------------------------------------
    def apply_to_app(self, app):
        """Apply basic palette colours to QApplication."""
        if not self.palette or app is None:
            return

        qpal = QPalette()
        bg = QColor(self.palette.get("background", "#081122"))
        text = QColor(self.palette.get("text", "#FFFFFF"))

        qpal.setColor(QPalette.Window, bg)
        qpal.setColor(QPalette.Base, bg)
        qpal.setColor(QPalette.AlternateBase, bg.darker(120))
        qpal.setColor(QPalette.WindowText, text)
        qpal.setColor(QPalette.Text, text)
        qpal.setColor(QPalette.ButtonText, text)
        qpal.setColor(QPalette.Highlight, QColor(self.palette.get("highlight_magenta", "#FF1E9B")))
        qpal.setColor(QPalette.HighlightedText, QColor("#FFFFFF"))

        app.setPalette(qpal)

    # ----------------------------------------------------------
    # QSS Stylesheet Generator
    # ----------------------------------------------------------
    def get_stylesheet(self):
        """Return a stylesheet string built dynamically from current theme."""
        bg = self.palette.get("background", "#081122")
        cyan = self.palette.get("highlight_cyan", "#00FFFF")
        pink = self.palette.get("highlight_magenta", "#FF1E9B")
        text = self.palette.get("text", "#FFFFFF")

        return f"""
        /* === NABlab Dynamic Theme === */

        QMainWindow {{
            background-color: {bg};
            color: {text};
        }}

        QWidget {{
            background-color: {bg};
            color: {text};
        }}

        QPushButton {{
            background-color: rgba(0, 255, 255, 0.15);
            color: {text};
            border: 1px solid {cyan};
            border-radius: 6px;
            padding: 6px 12px;
        }}
        QPushButton:hover {{
            background-color: rgba(255, 30, 155, 0.25);
            border-color: {pink};
        }}

        QLabel {{
            color: {text};
        }}

        QTreeView {{
            background-color: rgba(0, 0, 0, 0.15);
            color: {text};
            alternate-background-color: rgba(255, 255, 255, 0.05);
            border-right: 1px solid {cyan};
        }}

        QComboBox {{
            background-color: {bg};
            color: {text};
            border: 1px solid {cyan};
            border-radius: 6px;
            padding: 4px 8px;
        }}
        QComboBox:hover {{
            border-color: {pink};
        }}
        QComboBox QAbstractItemView {{
            background-color: {bg};
            color: {text};
            selection-background-color: rgba(255,30,155,0.4);
            selection-color: {pink};
            border: 1px solid {cyan};
        }}

        QListWidget {{
            background-color: rgba(8, 17, 34, 0.7);
            color: {text};
            border: 1px solid {cyan};
        }}
        QListWidget::item:selected {{
            background-color: rgba(255,30,155,0.4);
            color: {pink};
        }}

        #TopBar {{
            background-color: rgba(8, 17, 34, 0.9);
            border-bottom: 1px solid {cyan};
        }}

        QScrollBar:vertical {{
            background: {bg};
            width: 12px;
            margin: 0px;
        }}
        QScrollBar::handle:vertical {{
            background: {cyan};
            min-height: 20px;
            border-radius: 4px;
        }}
        QScrollBar::handle:vertical:hover {{
            background: {pink};
        }}
        """
