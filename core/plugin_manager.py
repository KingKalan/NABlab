"""
NABlab Core: Plugin Manager (v2.1)
Adds EXPOSE attribute support for UI labelling.
"""

import importlib.util
import os
import sys
from pathlib import Path


class PluginManager:
    """Manages all NABlab plugins by type."""

    def __init__(self, plugin_dir):
        self.plugin_dir = Path(plugin_dir)
        self.plugins = {}
        self.importers = []
        self.encoders = []
        self.packagers = []
        self.others = []

    def load_plugins(self):
        """Discover and import all .py files in plugin_dir."""
        if not self.plugin_dir.exists():
            print(f"[PLUGIN] No plugin directory found at {self.plugin_dir}")
            return

        for fname in os.listdir(self.plugin_dir):
            path = self.plugin_dir / fname
            if path.is_dir() or not fname.endswith(".py") or fname.startswith("__"):
                continue

            plugin_name = path.stem
            try:
                spec = importlib.util.spec_from_file_location(plugin_name, path)
                module = importlib.util.module_from_spec(spec)
                sys.modules[plugin_name] = module
                spec.loader.exec_module(module)
                self._register_plugin(module, plugin_name)
            except Exception as e:
                print(f"[PLUGIN] Failed to load {plugin_name}: {e}")

        self._print_summary()

    # --------------------------------------------------------
    def _register_plugin(self, module, plugin_name):
        ptype = getattr(module, "PLUGIN_TYPE", "Unknown")
        pname = getattr(module, "PLUGIN_NAME", plugin_name)
        pexpose = getattr(module, "EXPOSE", None)

        module.EXPOSE = pexpose or pname  # guarantee attribute

        self.plugins[pname] = module
        if ptype.lower() == "importer":
            self.importers.append(module)
        elif ptype.lower() == "encoder":
            self.encoders.append(module)
        elif ptype.lower() == "packager":
            self.packagers.append(module)
        else:
            self.others.append(module)

        print(f"[PLUGIN] Loaded {pname} ({ptype}) → EXPOSE={module.EXPOSE}")

    # --------------------------------------------------------
    def _print_summary(self):
        print("\n[PLUGIN] --- Summary ---")
        print(f" Importers : {len(self.importers)}")
        print(f" Encoders  : {len(self.encoders)}")
        print(f" Packagers : {len(self.packagers)}")
        if self.others:
            print(f" Other     : {len(self.others)}")
        print("------------------------\n")

    # --------------------------------------------------------
    def get_importer(self, name=None):
        if not self.importers:
            return None
        if name:
            return next((p for p in self.importers if getattr(p, "PLUGIN_NAME", "") == name), None)
        return self.importers[0]

    def get_encoder(self, name=None):
        if not self.encoders:
            return None
        if name:
            return next((p for p in self.encoders if getattr(p, "PLUGIN_NAME", "") == name), None)
        return self.encoders[0]

    def get_packager(self, name=None):
        if not self.packagers:
            return None
        if name:
            return next((p for p in self.packagers if getattr(p, "PLUGIN_NAME", "") == name), None)
        return self.packagers[0]
