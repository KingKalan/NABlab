"""
NABlab Core: Main Window (v3.2 – layout fix)
---------------------------------------------
Fixes top-bar alignment and overall UI geometry.

 • Proper left-aligned logo/title
 • Right-aligned buttons
 • Restored sizing of project tree + editor
 • Preferences shelf still docked right
 • Draggable, frameless glass window
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QSplitter,
    QListView, QTextEdit, QSizePolicy, QSpacerItem
)
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QIcon

from ui.topbar import TopBar
from ui.preferences_shelf import PreferencesShelf


class ProjectTree(QListView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("ProjectTree")


class EditorPanel(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("EditorPanel")
        self.setPlaceholderText("Audio editor / waveform display here.")


class MainWindow(QMainWindow):
    def __init__(self, config, theme, plugins, paths, plugin_state):
        super().__init__()
        self.setObjectName("MainWindow")

        self.config = config
        self.theme = theme
        self.plugins = plugins
        self.paths = paths
        self.plugin_state = plugin_state

        # Window setup
        self.setWindowTitle("NABlab")
        self.setWindowIcon(QIcon(str(self.paths.assets_dir / "nablab_logo.png")))
        self.resize(1280, 720)
        self.setMinimumSize(960, 540)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        # --- TOP BAR ---
        self.topbar = TopBar(self, self.plugin_state)
        self.topbar.setFixedHeight(50)
        self.topbar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        # --- PROJECT TREE + EDITOR ---
        self.project_tree = ProjectTree(self)
        self.editor_panel = EditorPanel(self)

        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.splitter.addWidget(self.project_tree)
        self.splitter.addWidget(self.editor_panel)
        self.splitter.setStretchFactor(0, 1)
        self.splitter.setStretchFactor(1, 3)

        # --- PREFERENCES SHELF ---
        self.preferences = PreferencesShelf(self, self.theme, self.config, self.plugin_state)
        self.preferences.setVisible(True)
        self.preferences.setFixedWidth(280)

        # --- CENTER LAYOUT (TOPBAR + SPLITTER) ---
        center = QWidget()
        vbox = QVBoxLayout(center)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(0)
        vbox.addWidget(self.topbar)
        vbox.addWidget(self.splitter)

        # --- ROOT CONTAINER: CENTER + PREF SHELF ---
        root = QWidget()
        root_layout = QHBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)
        root_layout.addWidget(center)
        root_layout.addWidget(self.preferences)

        self.setCentralWidget(root)

        # --- Theme ---
        self.apply_theme()

        # --- Window dragging ---
        self._drag_pos = QPoint()
        self.topbar.mousePressEvent = self._mouse_press
        self.topbar.mouseMoveEvent = self._mouse_move
        self.topbar.mouseReleaseEvent = self._mouse_release

    # --------------------------------------------------------
    # Theme application
    # --------------------------------------------------------
    def apply_theme(self):
        colors = getattr(self.theme, "colors", {})
        bg = colors.get("background", "#0a0a0a")
        text = colors.get("text", "#ffffff")
        accent = colors.get("highlight", "#00ffff")

        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {bg};
                color: {text};
            }}
            QListView {{
                background-color: #111;
                border: 1px solid #222;
            }}
            QTextEdit {{
                background-color: #111;
                color: {text};
                border: none;
            }}
            QPushButton {{
                color: {text};
                border: 1px solid {accent};
                border-radius: 4px;
                padding: 4px 10px;
            }}
            QPushButton:hover {{
                background-color: {accent};
                color: #000;
            }}
        """)

    # --------------------------------------------------------
    # Dragging support for frameless window
    # --------------------------------------------------------
    def _mouse_press(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def _mouse_move(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()

    def _mouse_release(self, event):
        self._drag_pos = QPoint()

    # --------------------------------------------------------
    # Toggle preferences shelf
    # --------------------------------------------------------
    def toggle_preferences(self):
        visible = not self.preferences.isVisible()
        self.preferences.setVisible(visible)
        print(f"[UI] Preferences shelf {'shown' if visible else 'hidden'}.")
