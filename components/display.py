from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QLineEdit
from PySide6.QtCore import Qt, Signal
from environment import BIG_FONT_SIZE, TEXT_MARGIN, MINIMUM_WIDTH
from utils.verifications import isEmpty, isNumOrDot


class Display(QLineEdit):
  eqTriggered = Signal()
  delTriggered = Signal()
  clearTriggered = Signal()
  inputTriggered = Signal(str)
  operatorTriggered = Signal(str)

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

    isEnter = key in [KEYS.Key_Enter, KEYS.Key_Return, KEYS.Key_Equal]
    isDelete = key in [KEYS.Key_Backspace, KEYS.Key_Delete, KEYS.Key_D]
    isEsc = key in [KEYS.Key_Escape, KEYS.Key_C]
    isOperator = key in [
      KEYS.Key_Plus, KEYS.Key_Minus, KEYS.Key_Slash, KEYS.Key_P
    ]

    if isEnter:
      self.eqTriggered.emit()
      return e.ignore()

    if isDelete:
      self.delTriggered.emit()
      return e.ignore()

    if isEsc:
      self.clearTriggered.emit()
      return e.ignore()

    if isOperator:
      self.clearTriggered.emit()
      return e.ignore()

    if isEmpty(text):
      if text.lower() == 'p':
        text = '^'
      return e.ignore()

    if isNumOrDot(text):
      self.inputTriggered.emit(text)
      return e.ignore()