"""
NABlab Plug-in: NARR Encoder
----------------------------
Spec-compliant stub for the Numen Audio Core v1.4

Responsibilities
 • Receives processed PCM data from importer + macro stack
 • Defines compression parameters and performs rate conversion
 • Writes encoded .narr binary to <project>/encoded_narr/
 • Generates encode metadata for project_config.json
"""

import os
import json
import struct
from dataclasses import dataclass
from datetime import datetime


PLUGIN_NAME = "NARR Encoder"
PLUGIN_TYPE = "Encoder"
SUPPORTED_INPUT = [".wav"]

# ------------------------------------------------------------
# Data container
# ------------------------------------------------------------
@dataclass
class NARRMeta:
    filename: str
    source_rate: int
    encode_rate: int
    channels: int
    bitdepth: int
    duration: float
    compression_ratio: float
    path: str


# ------------------------------------------------------------
# Encoder core
# ------------------------------------------------------------
class NARREncoder:
    """Handles encoding from PCM buffer → NARR binary."""

    def __init__(self, paths):
        self.paths = paths
        self.output_dir = self.paths.encoded_narr
        self.encode_rate = 48000        # default compression rate; adjustable
        self.compression_ratio = 4.0    # placeholder value
        self.encoded_files = {}

    # --------------------------------------------------------
    # Entry point
    # --------------------------------------------------------
    def encode_file(self, wav_meta, pcm_data: bytes):
        """
        Perform compression + rate conversion → NARR.
        This stub simulates encoding; replace with real algorithm.
        """
        out_name = os.path.splitext(wav_meta.filename)[0] + ".narr"
        out_path = self.output_dir / out_name

        # --- Simulated encode process ---
        encoded_blob = self._fake_encode(pcm_data)

        # --- Write encoded file ---
        with open(out_path, "wb") as f:
            f.write(encoded_blob)

        meta = NARRMeta(
            filename=out_name,
            source_rate=wav_meta.samplerate,
            encode_rate=self.encode_rate,
            channels=wav_meta.channels,
            bitdepth=wav_meta.bitdepth,
            duration=wav_meta.duration,
            compression_ratio=self.compression_ratio,
            path=str(out_path),
        )
        self.encoded_files[out_name] = meta
        print(f"[ENCODE] {out_name} | src={meta.source_rate}Hz → enc={meta.encode_rate}Hz")

    # --------------------------------------------------------
    # Fake encode implementation
    # --------------------------------------------------------
    def _fake_encode(self, pcm: bytes) -> bytes:
        """
        Placeholder: compress header + truncated data to simulate output.
        In a real encoder, this would:
         • resample PCM to encode_rate
         • quantize & compress
         • package with header for NARR format
        """
        header = struct.pack(
            "<4sIIf", b"NARR", self.encode_rate, len(pcm), self.compression_ratio
        )
        # simple truncation to simulate compression
        compressed = pcm[:: int(self.compression_ratio)] if pcm else b""
        return header + compressed

    # --------------------------------------------------------
    # Metadata persistence
    # --------------------------------------------------------
    def save_metadata(self):
        """Write encoding metadata to project_config.json"""
        out_path = self.paths.project / "narr_encode_index.json"
        index = {k: vars(v) for k, v in self.encoded_files.items()}
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(index, f, indent=4)
        print(f"[ENCODE] Metadata written: {out_path}")


# ------------------------------------------------------------
# Plugin entry function
# ------------------------------------------------------------
def register(paths):
    """Entry function for NABlab plugin loader."""
    encoder = NARREncoder(paths)
    print(f"[PLUGIN] {PLUGIN_NAME} ready at {datetime.now().strftime('%H:%M:%S')}")
    return encoder


# ------------------------------------------------------------
# Optional standalone test
# ------------------------------------------------------------
if __name__ == "__main__":
    from pathlib import Path
    from core.app_manager import Paths
    from plugins.wav_import import WAVImporter

    paths = Paths(Path.cwd())
    paths.set_project("test_project")

    importer = WAVImporter(paths)
    importer.import_all()

    encoder = NARREncoder(paths)
    for name, meta in importer.loaded_files.items():
        pcm = importer.load_pcm(name)
        encoder.encode_file(meta, pcm)
    encoder.save_metadata()
