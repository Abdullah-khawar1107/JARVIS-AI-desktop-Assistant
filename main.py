import sys

from PySide6.QtWidgets import QApplication

from interface.window import JarvisWindow


app = QApplication(sys.argv)

window = JarvisWindow()

window.show()

sys.exit(app.exec())