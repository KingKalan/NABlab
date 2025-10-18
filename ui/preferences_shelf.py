"""
NABlab UI: Preferences Shelf (v3)
---------------------------------
Exposes:
 • Theme selection
 • Font selection
 • Active Importer / Encoder / Packager selection
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QComboBox, QScrollArea, QPushButton
)
from PySide6.QtCore import Qt


class PreferencesShelf(QWidget):
    def __init__(self, parent, theme_manager, config, plugin_state):
        super().__init__(parent)
        self.theme = theme_manager
        self.config = config
        self.plugin_state = plugin_state
        self.setObjectName("PreferencesShelf")
        self.setMinimumWidth(300)

        # Layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        # ---- Theme selection ----
        layout.addWidget(QLabel("Theme"))
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(self.theme.list_themes())
        current_theme = self.theme.current_theme_name
        if current_theme in [self.theme_combo.itemText(i) for i in range(self.theme_combo.count())]:
            self.theme_combo.setCurrentText(current_theme)
        self.theme_combo.currentTextChanged.connect(self.on_theme_change)
        layout.addWidget(self.theme_combo)
        self.theme_combo.currentIndexChanged.connect(self.on_theme_change)


        # ---- Font selection ----
        layout.addWidget(QLabel("Font"))
        self.font_combo = QComboBox()
        self.font_combo.addItems(self.theme.list_fonts())
        layout.addWidget(self.font_combo)

        # ---- Importer selection ----
        layout.addWidget(QLabel("Importer"))
        self.importer_combo = QComboBox()
        self._populate_plugins(self.importer_combo, plugin_state.plugin_manager.importers)
        self.importer_combo.currentTextChanged.connect(self.on_importer_change)
        layout.addWidget(self.importer_combo)

        # ---- Encoder selection ----
        layout.addWidget(QLabel("Encoder"))
        self.encoder_combo = QComboBox()
        self._populate_plugins(self.encoder_combo, plugin_state.plugin_manager.encoders)
        self.encoder_combo.currentTextChanged.connect(self.on_encoder_change)
        layout.addWidget(self.encoder_combo)

        # ---- Packager selection ----
        layout.addWidget(QLabel("Packager"))
        self.packager_combo = QComboBox()
        self._populate_plugins(self.packager_combo, plugin_state.plugin_manager.packagers)
        self.packager_combo.currentTextChanged.connect(self.on_packager_change)
        layout.addWidget(self.packager_combo)

        # ---- Close button ----
        layout.addStretch()
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)

        # ---- Scroll area container ----
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        inner = QWidget()
        inner.setLayout(layout)
        scroll.setWidget(inner)

        main = QVBoxLayout()
        main.addWidget(scroll)
        self.setLayout(main)

        self.apply_theme_colors()

    # --------------------------------------------------------
    def _populate_plugins(self, combo, plugin_list):
        combo.clear()
        for mod in plugin_list:
            name = getattr(mod, "PLUGIN_NAME", "Unnamed")
            combo.addItem(name)

    # --------------------------------------------------------
    # Theme handling
    # --------------------------------------------------------




    def apply_theme_colors(self):
        bg = self.theme.colors.get("background", "#111111")
        self.setStyleSheet(f"""
            QComboBox {{
                background-color: {bg};
                color: white;
                border: 1px solid #555;
                padding: 4px;
            }}
            QComboBox::drop-down {{
                border: none;
            }}
            QLabel {{
                color: white;
                font-weight: bold;
            }}
            QPushButton {{
                background-color: #222;
                color: white;
                border: 1px solid #555;
                border-radius: 4px;
                padding: 4px 8px;
            }}
            QPushButton:hover {{
                background-color: #333;
            }}
        """)

    # --------------------------------------------------------
    # Plugin switching
    # --------------------------------------------------------
    def on_importer_change(self, name):
        self.plugin_state.set_importer(name)

    def on_encoder_change(self, name):
        self.plugin_state.set_encoder(name)

    def on_packager_change(self, name):
        self.plugin_state.set_packager(name)

            # --------------------------------------------------------
    # Theme switching
    # --------------------------------------------------------
    def on_theme_change(self):
        """
        Triggered when user selects a new theme from dropdown.
        Reloads theme and reapplies to MainWindow and TopBar.
        """
        theme_name = self.theme_combo.currentText()
        print(f"[DEBUG] on_theme_change triggered → {theme_name}")
        self.theme.load_theme(theme_name)

        # Get top-level window
        main_window = self.window()

        if hasattr(main_window, "apply_theme"):
            print("[DEBUG] Reapplying theme to MainWindow")
            main_window.apply_theme()

        if hasattr(main_window, "topbar") and hasattr(main_window.topbar, "apply_theme_colors"):
            print("[DEBUG] Reapplying theme to TopBar")
            main_window.topbar.apply_theme_colors()


