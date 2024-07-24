import sys
from PyQt6.QtWidgets import QApplication, QListWidget, QListWidgetItem
from PyQt6.QtCore import Qt, pyqtSignal


class DragDropList(QListWidget):
    fileReceived = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.DropAction.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.DropAction.CopyAction)
            event.accept()
            self.fileReceived.emit(str(event.mimeData().urls()[0].toLocalFile()))
        else:
            event.ignore()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    list_widget = DragDropList()
    list_widget.show()
    sys.exit(app.exec())