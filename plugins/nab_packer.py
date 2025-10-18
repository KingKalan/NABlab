"""
NABlab Plug-in: NAB Packager
----------------------------
Reference implementation for Numen Audio Core v1.4
"""

import os
import json
import zipfile
from datetime import datetime

PLUGIN_NAME = "NAB Packager"
PLUGIN_TYPE = "Packager"
SUPPORTED_ENCODERS = [".narr"]
EXPOSE = "NAB"


class NABPackager:
    def __init__(self, paths):
        self.paths = paths
        self.output_file = self.paths.project / "project.nab"

    def package_project(self):
        """Bundle encoded files + metadata into .nab archive."""
        encoded_dir = self.paths.encoded_narr
        if not encoded_dir.exists():
            print(f"[PACKAGER] No encoded_narr folder found: {encoded_dir}")
            return None

        files = [f for f in encoded_dir.iterdir() if f.suffix == ".narr"]
        if not files:
            print("[PACKAGER] No encoded files to package.")
            return None

        manifest = self._build_manifest(files)

        # create archive
        with zipfile.ZipFile(self.output_file, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            # add encoded files
            for f in files:
                zf.write(f, arcname=f"encoded_narr/{f.name}")
            # add manifest
            zf.writestr("manifest.json", json.dumps(manifest, indent=4))

        print(f"[PACKAGER] Created {self.output_file.name} ({len(files)} files)")
        return manifest

    def _build_manifest(self, files):
        """Collect metadata for manifest.json."""
        manifest = {
            "project": self.paths.project.name,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "file_count": len(files),
            "encoded_files": [],
        }

        # merge encoder + importer metadata if present
        for meta_file in ("narr_encode_index.json", "wav_import_index.json"):
            path = self.paths.project / meta_file
            if path.exists():
                with open(path, "r", encoding="utf-8") as f:
                    manifest[meta_file] = json.load(f)

        for f in files:
            manifest["encoded_files"].append(f.name)
        return manifest


# ------------------------------------------------------------
# Plugin entry point
# ------------------------------------------------------------
def register(paths):
    print(f"[PLUGIN] {PLUGIN_NAME} initialized")
    return NABPackager(paths)


if __name__ == "__main__":
    from pathlib import Path
    from core.app_manager import Paths
    paths = Paths(Path.cwd())
    paths.set_project("test_project")
    pkg = NABPackager(paths)
    pkg.package_project()
