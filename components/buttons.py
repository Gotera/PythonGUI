from PySide6.QtWidgets import QPushButton, QGridLayout
from PySide6.QtCore import Slot
from environment import MEDIUM_FONT_SIZE
from utils.verify_buttons import isValidNumber, isNumOrDot, isEmpty
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from display import Display
    from info import Info

class Button(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configStyle()

    def configStyle(self):
        self.setStyleSheet(f'font-size: {MEDIUM_FONT_SIZE}px;')


class ButtonsGrid(QGridLayout):
    def __init__(self, display: 'Display', info: 'Info', *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._gridMask = [
            ['C', '◀', '^', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['',  '0', '.', '='],
        ]
        self.display = display
        self.info = info
        self._equation = ''
        self._makeGrid()
        
    @property
    def equation(self):
        return self._equation
    
    @equation.setter
    def equation(self, value):
        self._equation = value
        self.info.setText(value)

    def _makeGrid(self):
        for i, row in enumerate(self._gridMask):
            for j, button_text in enumerate(row):
                button = Button(button_text)
                
                if not isNumOrDot(button_text) and not isEmpty(button_text):
                  self._configSpecialButton(button)
                  
                self.addWidget(button, i, j)
                buttonSlot = self._makeSlot(
                    self._insertButtonValueInDisplay,
                    button
                )
                self._connectButtonClicked(button, buttonSlot)
                
    def _connectButtonClicked(self, button, slot):
        button.clicked.connect(slot)
                
    def _configSpecialButton(self, button):
        button.setProperty('cssClass', 'specialButton')   
        
        text = button.text()
        if text == "C":
            slot = self._makeSlot(self._clear)
            self._connectButtonClicked(button, slot)
                
    def _makeSlot(self, func, *args, **kwargs):
        @Slot(bool)
        def realSlot(_):
            func(*args, **kwargs)
        return realSlot
    
    def _insertButtonValueInDisplay(self, button):
        buttonText = button.text()
        newDisplayValue = self.display.text() + buttonText
        
        if not isValidNumber(newDisplayValue):
            return
        
        self.display.insert(buttonText)
        
    def _clear(self):
        self.display.clear()