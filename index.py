import sys
from main_window import MainWindow
from environment import WINDOW_ICON_PATH
from PySide6.QtWidgets import QApplication, QLabel
from PySide6.QtGui import QIcon


if __name__ == "__main__":
  app = QApplication(sys.argv)
  window = MainWindow()
  
  label1 = QLabel('Hello World')
  label1.setStyleSheet('font-size: 12px; font-weight: bold')
  window.addWidgetToVLayout(label1)
  window.adjustFixedSize()
  
  icon = QIcon(str(WINDOW_ICON_PATH))
  window.setWindowIcon(icon)
  app.setWindowIcon(icon)
  
  window.adjustFixedSize()
  window.show()
  app.exec()