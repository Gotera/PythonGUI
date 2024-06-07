from PySide6.QtWidgets import QPushButton, QGridLayout
from PySide6.QtCore import Slot
from environment import MEDIUM_FONT_SIZE
from utils.verify_buttons import isNumOrDot, isEmpty

class Button(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configStyle()

    def configStyle(self):
        self.setStyleSheet(f'font-size: {MEDIUM_FONT_SIZE}px;')


class ButtonsGrid(QGridLayout):
    def __init__(self, display, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._gridMask = [
            ['C', '◀', '^', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['',  '0', '.', '='],
        ]
        self.display = display
        self._makeGrid()

    def _makeGrid(self):
        for i, row in enumerate(self._gridMask):
            for j, button_text in enumerate(row):
                button = Button(button_text)
                if not isNumOrDot(button_text) and not isEmpty(button_text):
                  button.setProperty('cssClass', 'specialButton')     
                self.addWidget(button, i, j)
                buttonSlot = self._makeButtonDisplaySlot(
                    self._insertButtonValueInDisplay,
                    button
                )
                button.clicked.connect(buttonSlot)
                
    def _makeButtonDisplaySlot(self, func, *args, **kwargs):
        @Slot
        def realSlot(self):
            func(*args, **kwargs)
        return realSlot
    
    def _insertButtonValueInDisplay(self, button):
        button_text = button.text()
        self.display.insert(button_text)