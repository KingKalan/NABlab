"""
NABlab UI: Top Bar (v4.2 — Theme-Aware)
---------------------------------------
• Dynamically applies ThemeManager colors
• Retains logo + window controls + live EXPOSE label
• Uses parent's theme whenever load_theme() changes
"""

from PySide6.QtWidgets import (
    QWidget, QLabel, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPixmap


class TopBar(QWidget):
    def __init__(self, parent, plugin_state):
        super().__init__(parent)
        self.parent_window = parent
        self.plugin_state = plugin_state
        self.theme = getattr(parent, "theme", None)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 6, 12, 6)
        layout.setSpacing(10)

        # --- Left: logo + title
        self.logo_label = QLabel()
        self.logo_label.setFixedSize(28, 28)
        logo_path = getattr(parent.paths, "assets_dir", None)
        if logo_path:
            try:
                pix = QPixmap(str(logo_path / "nablab_logo.png"))
                if not pix.isNull():
                    self.logo_label.setPixmap(
                        pix.scaled(28, 28, Qt.AspectRatioMode.KeepAspectRatio, Qt.SmoothTransformation)
                    )
            except Exception as e:
                print(f"[UI] Logo load failed: {e}")

        self.title_label = QLabel("NABlab")

        left_box = QWidget()
        left_layout = QHBoxLayout(left_box)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(6)
        left_layout.addWidget(self.logo_label)
        left_layout.addWidget(self.title_label)
        layout.addWidget(left_box)

        layout.addItem(QSpacerItem(20, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        # --- Center: project buttons
        self.open_btn = QPushButton("Open Project")
        self.new_btn = QPushButton("New Project")

        expose = plugin_state.active_packager_expose or "NAB"
        self.package_btn = QPushButton(f"Package {expose}")

        self.pref_btn = QPushButton("Preferences")
        self.pref_btn.clicked.connect(self.parent_window.toggle_preferences)

        for btn in (self.open_btn, self.new_btn, self.package_btn, self.pref_btn):
            btn.setFixedHeight(28)

        plugin_state.packager_changed.connect(self._on_packager_changed)

        layout.addWidget(self.open_btn)
        layout.addWidget(self.new_btn)
        layout.addWidget(self.package_btn)
        layout.addWidget(self.pref_btn)

        layout.addItem(QSpacerItem(20, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        # --- Right: window controls
        self.min_btn = QPushButton("–")
        self.max_btn = QPushButton("⬜")
        self.close_btn = QPushButton("×")
        for b in (self.min_btn, self.max_btn, self.close_btn):
            b.setFixedSize(QSize(28, 28))
            b.clicked.connect(self._handle_window_button)

        layout.addWidget(self.min_btn)
        layout.addWidget(self.max_btn)
        layout.addWidget(self.close_btn)

        self.setLayout(layout)
        self.setFixedHeight(46)
        self.apply_theme_colors()

    # --------------------------------------------------------
    # Dynamic styling from theme manager
    # --------------------------------------------------------
    def apply_theme_colors(self):
        if not self.theme or not hasattr(self.theme, "colors"):
            return

        c = self.theme.colors
        bg = c.get("panel_bg", c.get("background", "#0a0a0a"))
        text = c.get("text", "#ffffff")
        accent = c.get("highlight", "#00ffff")
        hot = c.get("accent", "#ff00aa")

        self.setStyleSheet(f"""
            TopBar, QWidget#TopBar {{
                background-color: {bg};
                border-bottom: 1px solid {accent};
            }}
            QLabel {{
                color: {text};
                font-weight: bold;
                font-size: 14px;
            }}
            QPushButton {{
                color: {text};
                border: 1px solid {accent};
                border-radius: 4px;
                padding: 4px 10px;
                background: transparent;
            }}
            QPushButton:hover {{
                background-color: {accent};
                color: #000;
            }}
            QPushButton#WinBtn {{
                border: none;
                color: {accent};
                background: transparent;
                font-size: 14px;
            }}
            QPushButton#WinBtn:hover {{
                color: {hot};
                background-color: rgba(255,255,255,0.1);
            }}
        """)

        # assign window button object names so they get themed
        for b in (self.min_btn, self.max_btn, self.close_btn):
            b.setObjectName("WinBtn")

    # --------------------------------------------------------
    # Plugin reaction
    # --------------------------------------------------------
    def _on_packager_changed(self, _):
        expose = self.plugin_state.active_packager_expose or "NAB"
        self.package_btn.setText(f"Package {expose}")

    # --------------------------------------------------------
    # Window controls
    # --------------------------------------------------------
    def _handle_window_button(self):
        sender = self.sender()
        win = self.window()
        if sender == self.min_btn:
            win.showMinimized()
        elif sender == self.max_btn:
            win.showNormal() if win.isMaximized() else win.showMaximized()
        elif sender == self.close_btn:
            win.close()
