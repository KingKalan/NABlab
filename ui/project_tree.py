from PySide6.QtWidgets import QTreeView, QFileSystemModel


class ProjectTree(QTreeView):
    """Displays project folder structure."""

    def __init__(self, paths):
        super().__init__()
        self.model = QFileSystemModel()
        self.model.setRootPath(str(paths.project_dir))
        self.setModel(self.model)
        self.setRootIndex(self.model.index(str(paths.project_dir)))
        self.setHeaderHidden(True)
        self.setMinimumWidth(250)
        self.setStyleSheet("background-color: rgba(0,0,0,0.3); border-right: 1px solid #00FFFF;")
