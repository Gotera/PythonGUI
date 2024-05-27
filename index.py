import sys
from PySide6.QtWidgets import QApplication, QPushButton

app = QApplication(sys.argv)
button = QPushButton('Texto do botão')
button.show()

app.exec()