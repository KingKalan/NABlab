"""
NABlab Plug-in: WAV Importer
--------------------------------
Complies with Numen Audio Core Spec v1.4
 - Imports uncompressed PCM WAV files
 - Performs header validation
 - Extracts metadata and PCM buffer
 - Does NOT resample, normalize, or compress
 - Encoder defines compression rate; decoder defines playback rate (32 kHz)
"""

import wave
import os
import json
from dataclasses import dataclass


PLUGIN_NAME = "WAV Import"
PLUGIN_TYPE = "Importer"
SUPPORTED_EXT = [".wav", ".wave"]


@dataclass
class WAVMeta:
    """Container for WAV file metadata."""
    filename: str
    channels: int
    samplerate: int
    bitdepth: int
    frames: int
    duration: float
    path: str


class WAVImporter:
    """Handles WAV file imports for NABlab."""

    def __init__(self, paths):
        self.paths = paths
        self.source_dir = self.paths.source_audio
        self.loaded_files = {}

    # --------------------------------------------------------
    # Utility
    # --------------------------------------------------------
    def _is_supported(self, filename: str) -> bool:
        return any(filename.lower().endswith(ext) for ext in SUPPORTED_EXT)

    # --------------------------------------------------------
    # Core Import
    # --------------------------------------------------------
    def import_all(self):
        """Import all valid WAV files from <project>/source_audio/"""
        if not self.source_dir.exists():
            print(f"[WAV] No source_audio folder found: {self.source_dir}")
            return

        for fname in os.listdir(self.source_dir):
            if not self._is_supported(fname):
                continue

            fpath = self.source_dir / fname
            try:
                meta = self._read_metadata(fpath)
                self.loaded_files[fname] = meta
                print(f"[WAV] Imported: {fname} | {meta.channels}ch, {meta.samplerate}Hz, {meta.bitdepth}-bit")
            except Exception as e:
                print(f"[WAV] Failed to import {fname}: {e}")

    # --------------------------------------------------------
    # Read and parse WAV header
    # --------------------------------------------------------
    def _read_metadata(self, filepath) -> WAVMeta:
        with wave.open(str(filepath), "rb") as wf:
            channels = wf.getnchannels()
            samplerate = wf.getframerate()
            frames = wf.getnframes()
            sampwidth = wf.getsampwidth() * 8  # bytes → bits
            duration = frames / float(samplerate)
            meta = WAVMeta(
                filename=filepath.name,
                channels=channels,
                samplerate=samplerate,
                bitdepth=sampwidth,
                frames=frames,
                duration=duration,
                path=str(filepath),
            )
        return meta

    # --------------------------------------------------------
    # PCM Extraction (optional for editor use)
    # --------------------------------------------------------
    def load_pcm(self, filename: str) -> bytes:
        """Return raw PCM data (no resample)."""
        filepath = self.source_dir / filename
        with wave.open(str(filepath), "rb") as wf:
            data = wf.readframes(wf.getnframes())
        return data

    # --------------------------------------------------------
    # Metadata Persistence
    # --------------------------------------------------------
    def save_metadata(self, out_path=None):
        """Write imported file metadata to JSON for project_config."""
        if out_path is None:
            out_path = self.paths.project / "wav_import_index.json"

        index = {k: vars(v) for k, v in self.loaded_files.items()}
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(index, f, indent=4)
        print(f"[WAV] Metadata index written: {out_path}")


# ------------------------------------------------------------
# Entry Point
# ------------------------------------------------------------
def register(paths):
    """Entry function for NABlab plug-in loader."""
    importer = WAVImporter(paths)
    importer.import_all()
    importer.save_metadata()
    return importer


# Optional: direct test
if __name__ == "__main__":
    from pathlib import Path
    from core.app_manager import Paths

    paths = Paths(Path.cwd())
    paths.set_project("test_project")
    imp = WAVImporter(paths)
    imp.import_all()
    imp.save_metadata()
