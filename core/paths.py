import os
from pathlib import Path


class Paths:
    """Ensures all critical NABlab folders exist."""

    def __init__(self):
        self.root = Path(__file__).resolve().parent.parent
        self.project_dir = self.root / "projects"
        self.theme_dir = self.root / "themes"
        self.plugin_dir = self.root / "plugins"
        self.font_dir = self.root / "fonts"
        self.assets_dir = self.root / "assets"
        self.config_path = self.root / "config.json"
        self.ensure_dirs()

    def ensure_dirs(self):
        """Create missing directories."""
        for folder in [self.project_dir, self.theme_dir, self.plugin_dir,
                       self.font_dir, self.assets_dir]:
            folder.mkdir(exist_ok=True)
