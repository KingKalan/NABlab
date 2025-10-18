"""
NABlab Core: App Manager (v3)
-----------------------------
Initializes Qt, Paths, Config, Theme, Plugins, and PluginState.
"""

import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication
from core.window_main import MainWindow
from core.theme_manager import ThemeManager
from core.config_manager import ConfigManager
from core.plugin_manager import PluginManager
from core.plugin_state import PluginState


# ------------------------------------------------------------
# Path management
# ------------------------------------------------------------
class Paths:
    """Container for NABlab directory paths (v1.3 final)."""

    def __init__(self, base_dir: str):
        base = Path(base_dir)

        # Root-level structure
        self.base = base
        self.root = base
        self.config = base / "config"
        self.themes = base / "themes"
        self.plugins = base / "plugins"
        self.projects = base / "projects"
        self.project_dir = self.projects
        self.fonts = base / "fonts"
        self.assets_dir = base / "assets"
        self.macros = base / "macros"

        # Project-scoped directories (set dynamically)
        self.project = None
        self.source_audio = None
        self.encoded_narr = None
        self.project_file = None
        self.project_config = None

    def set_project(self, project_name: str):
        """Resolve and prepare per-project directories."""
        self.project = self.projects / project_name
        self.source_audio = self.project / "source_audio"
        self.encoded_narr = self.project / "encoded_narr"
        self.project_file = self.project / "project.nab"
        self.project_config = self.project / "project_config.json"

        for p in [self.project, self.source_audio, self.encoded_narr]:
            p.mkdir(parents=True, exist_ok=True)

    def __repr__(self):
        return f"<Paths base={self.base}, project={self.project}>"


# ------------------------------------------------------------
# Main Application Manager
# ------------------------------------------------------------
class AppManager:
    """Main NABlab application manager."""

    def __init__(self):
        # --- Qt app ---
        self.qt_app = QApplication(sys.argv)

        # --- Paths ---
        self.paths = Paths(Path.cwd())

        # --- Managers ---
        config_path = self.paths.config / "config.json"
        self.config = ConfigManager(str(config_path))
        self.theme = ThemeManager(str(self.paths.themes))
        self.plugins = PluginManager(str(self.paths.plugins))
        self.plugins.load_plugins()
        self.plugin_state = PluginState(self.plugins)

        # --- Theme load ---
        selected_theme = self.config.data.get("theme", "dark_retro")
        self.theme.load_theme(selected_theme)
        self.theme.apply_to_app(self.qt_app)
        self.qt_app.setStyleSheet(self.theme.get_stylesheet())

        # --- Main window ---
        self.window = MainWindow(self.config, self.theme, self.plugins, self.paths, self.plugin_state)
        # give window access to plugin_state for preferences UI
        self.window.plugin_state = self.plugin_state
        self.window.show()

    def run(self):
        sys.exit(self.qt_app.exec())


if __name__ == "__main__":
    manager = AppManager()
    manager.run()
