"""
NABlab Core: Plugin State Manager (v2)
Now exposes active_packager_expose for UI updates.
"""

from PySide6.QtCore import QObject, Signal


class PluginState(QObject):
    importer_changed = Signal(str)
    encoder_changed = Signal(str)
    packager_changed = Signal(str)

    def __init__(self, plugin_manager):
        super().__init__()
        self.plugin_manager = plugin_manager
        self.active_importer = None
        self.active_encoder = None
        self.active_packager = None
        self.set_importer()
        self.set_encoder()
        self.set_packager()

    # --------------------------------------------------------
    def set_importer(self, name=None):
        plugin = self.plugin_manager.get_importer(name)
        if plugin:
            self.active_importer = plugin
            pname = getattr(plugin, "PLUGIN_NAME", "Unnamed Importer")
            self.importer_changed.emit(pname)
            print(f"[STATE] Active importer → {pname}")

    def set_encoder(self, name=None):
        plugin = self.plugin_manager.get_encoder(name)
        if plugin:
            self.active_encoder = plugin
            pname = getattr(plugin, "PLUGIN_NAME", "Unnamed Encoder")
            self.encoder_changed.emit(pname)
            print(f"[STATE] Active encoder → {pname}")

    def set_packager(self, name=None):
        plugin = self.plugin_manager.get_packager(name)
        if plugin:
            self.active_packager = plugin
            pname = getattr(plugin, "PLUGIN_NAME", "Unnamed Packager")
            self.packager_changed.emit(pname)
            print(f"[STATE] Active packager → {pname}")

    # --------------------------------------------------------
    def get_importer(self):
        return self.active_importer

    def get_encoder(self):
        return self.active_encoder

    def get_packager(self):
        return self.active_packager

    @property
    def active_packager_expose(self):
        """Return EXPOSE tag of the active packager (e.g. NAB, SF2)."""
        if not self.active_packager:
            return None
        return getattr(self.active_packager, "EXPOSE", "NAB")
