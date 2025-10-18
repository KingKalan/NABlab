import json
import os


class ConfigManager:
    """Manages persistent user configuration (theme, font, recent project)."""

    def __init__(self, config_path):
        self.config_path = config_path
        self.data = self._load()

    def _load(self):
        """Load or initialize default config."""
        if not os.path.exists(self.config_path):
            data = {
                "theme": "dark_retro",
                "font": "default.ttf",
                "recent_project": ""
            }
            self._save(data)
            return data
        with open(self.config_path, "r") as f:
            return json.load(f)

    def _save(self, data=None):
        """Write configuration back to disk."""
        if data is not None:
            self.data = data
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, "w") as f:
            json.dump(self.data, f, indent=2)

    def set(self, key, value):
        """Set and persist a config key."""
        self.data[key] = value
        self._save()

    def get(self, key, default=None):
        return self.data.get(key, default)
