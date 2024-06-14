from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QLineEdit
from PySide6.QtCore import Qt, Signal
from environment import BIG_FONT_SIZE, TEXT_MARGIN, MINIMUM_WIDTH
from utils.verify_buttons import isEmpty


class Display(QLineEdit):
  eqTriggered = Signal() 
  delTriggered = Signal() 
  clearTriggered = Signal() 
  
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.configStyle()
    
  def configStyle(self):
    margins = [TEXT_MARGIN for _ in range(4)]
    self.setStyleSheet(f'font-size: {BIG_FONT_SIZE}px;')
    self.setMinimumHeight(BIG_FONT_SIZE * 2)
    self.setMinimumWidth(MINIMUM_WIDTH)
    self.setAlignment(Qt.AlignmentFlag.AlignRight)
    self.setTextMargins(*margins)
    
  def keyPressEvent(self, e: QKeyEvent) -> None:
    text = e.text().strip()
    key = e.key()
    KEYS = Qt.Key
    
    isEnter = key in [KEYS.Key_Enter, KEYS.Key_Return]
    isDelete = key in [KEYS.Key_Backspace, KEYS.Key_Delete]
    isEsc = key == KEYS.Key_Escape
    
    if isEnter:
      self.eqTriggered.emit()
      return super().keyPressEvent(e)
    
    if isDelete:
      self.delTriggered.emit()
      return super().keyPressEvent(e)
    
    if isEsc:
      self.clearTriggered.emit()
      return super().keyPressEvent(e)
    
    if isEmpty(text):
      return e.ignore()