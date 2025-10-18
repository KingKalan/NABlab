from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout


class EditorPanel(QWidget):
    """Placeholder editor panel (future: waveform display)."""

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("Editor Panel — Waveform View Coming Soon")
        self.label.setStyleSheet("font-size: 14px; color: #CCCCCC;")
        layout.addWidget(self.label)
        layout.addStretch(1)
        self.setLayout(layout)
        self.setStyleSheet("background-color: rgba(255,255,255,0.05);")
