import sys
from main_window import MainWindow
from display import Display
from info import Info
from environment import WINDOW_ICON_PATH
from PySide6.QtWidgets import QApplication, QLabel
from PySide6.QtGui import QIcon
from styles import setupTheme

if __name__ == "__main__":
  app = QApplication(sys.argv)
  setupTheme()
  window = MainWindow()
  
  icon = QIcon(str(WINDOW_ICON_PATH))
  window.setWindowIcon(icon)
  app.setWindowIcon(icon)
  
  info = Info('Testeee')
  window.addWidgetToVLayout(info)
  
  display = Display()
  window.addWidgetToVLayout(display)
  
  window.adjustFixedSize()
  window.show()
  app.exec()