from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt
from environment import SMALL_FONT_SIZE

class Info(QLabel):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.confiStyle()
    
  def confiStyle(self):
    self.setStyleSheet(f'font-size: {SMALL_FONT_SIZE}px;')
    self.setAlignment(Qt.AlignmentFlag.AlignRight)