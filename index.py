import sys
from components.main_window import MainWindow
from components.display import Display
from components.info import Info
from components.buttons import ButtonsGrid
from environment import WINDOW_ICON_PATH
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from styles.styles import setupTheme

if __name__ == "__main__":
  app = QApplication(sys.argv)
  setupTheme()
  window = MainWindow()
  
  icon = QIcon(str(WINDOW_ICON_PATH))
  window.setWindowIcon(icon)
  app.setWindowIcon(icon)
  
  info = Info('Sua conta')
  window.addWidgetToVLayout(info)
  
  display = Display()
  window.addWidgetToVLayout(display)
  
  buttonsGrid = ButtonsGrid(display, info, window)
  window.vLayout.addLayout(buttonsGrid)
  
  window.adjustFixedSize()
  window.show()
  app.exec()