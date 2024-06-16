from PySide6.QtWidgets import QPushButton, QGridLayout
from PySide6.QtCore import Slot
from environment import MEDIUM_FONT_SIZE
from utils.verifications import isValidNumber, isNumOrDot, isEmpty, convertToNumber
from typing import TYPE_CHECKING
import math

if TYPE_CHECKING:
    from display import Display
    from info import Info
    from main_window import MainWindow


class Button(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configStyle()

    def configStyle(self):
        self.setStyleSheet(f'font-size: {MEDIUM_FONT_SIZE}px;')


class ButtonsGrid(QGridLayout):
    def __init__(self, display: 'Display', info: 'Info', window: 'MainWindow', *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._gridMask = [
            ['C', '◀', '^', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['N',  '0', '.', '='],
        ]
        self.display = display
        self.info = info
        self.window = window
        self._equation = ''
        self._equationInitialValue = 'Your Calculation'
        self._left = None
        self._right = None
        self.op = None
        self.equation = self._equationInitialValue
        self._makeGrid()

    @property
    def equation(self):
        return self._equation

    @equation.setter
    def equation(self, value):
        self._equation = value
        self.info.setText(value)

    def testString(self, *args):
        print(type(self).__name__, args)

    def _makeGrid(self):
        self.display.eqTriggered.connect(self._eq)
        self.display.delTriggered.connect(self._backspace)
        self.display.clearTriggered.connect(self._clear)
        self.display.inputTriggered.connect(self._insertToDisplay)
        self.display.operatorTriggered.connect(self._configLeftOperator)
        
        for i, row in enumerate(self._gridMask):
            for j, buttonText in enumerate(row):
                button = Button(buttonText)

                if not isNumOrDot(buttonText) and not isEmpty(buttonText):
                    button.setProperty('cssClass', 'specialButton')
                    self._configSpecialButton(button)

                self.addWidget(button, i, j)
                buttonSlot = self._makeSlot(
                    self._insertToDisplay,
                    buttonText
                )
                self._connectButtonClicked(button, buttonSlot)

    def _connectButtonClicked(self, button, slot):
        button.clicked.connect(slot)

    def _configSpecialButton(self, button):
        text = button.text()
        
        if text == "C":
            self._connectButtonClicked(button, self._clear)

        if text in "+-/*^":
            self._connectButtonClicked(
                button,
                self._makeSlot(self._configLeftOperator, text)
            )

        if text == "◀":
            self._connectButtonClicked(button, self.display.backspace)

        if text == "=":
            self._connectButtonClicked(
                button,
                self._connectButtonClicked(button, self._eq)
            )
        
        if text == "N":
            self._connectButtonClicked(
                button,
                self._connectButtonClicked(button, self._invertNumber)
            )

    def _makeSlot(self, func, *args, **kwargs):
        @Slot(bool)
        def realSlot(_):
            func(*args, **kwargs)
        return realSlot

    @Slot()
    def _invertNumber(self):
        displayText = self.display.text()
        
        if not isValidNumber(displayText):
            return
    
        number = convertToNumber(displayText) * -1
        self.display.setText(str(number))
    
    @Slot()
    def _insertToDisplay(self, text):
        newDisplayValue = self.display.text() + text

        if not isValidNumber(newDisplayValue):
            return

        self.display.insert(text)
        self.display.setFocus()

    @Slot()
    def _clear(self):
        self._left = None
        self._right = None
        self._op = None
        self.equation = self._equationInitialValue
        self.display.clear()
        self.display.setFocus()

    @Slot()
    def _configLeftOperator(self, text):
        displayText = self.display.text()
        self.display.clear()
        self.display.setFocus()

        if not isValidNumber(displayText) and self._left is None:
            return

        if self._left is None:
            self._left = convertToNumber(displayText)

        self._op = text
        self.equation = f'{self._left} {self._op} ??'

    @Slot()
    def _eq(self):
        displatText = self.display.text()

        if not isValidNumber(displatText) or self._left is None:
            self._showError('Você não digitou o outro número da conta.')
            return

        self._right = convertToNumber(displatText)
        self.equation = f'{self._left} {self._op} {self._right}'
        result = 'error'

        try:
            if '^' in self.equation and isinstance(self._left, (float, int)):
                result = math.pow(self._left, self._right)
                result = convertToNumber(str(result))
            else:
                result = eval(self.equation)
        except ZeroDivisionError:
            self._showError('Divisão por zero.')
        except OverflowError:
            self._showError('Conta não pode ser realizada.')

        self.display.clear()
        self.info.setText(f'{self.equation} = {result}')
        self._left = result
        self._right = None
        self.display.setFocus()

        if result == 'error':
            self._left = None

    @Slot()
    def _backspace(self):
        self.display.backspace()
        self.display.setFocus()

    def _showError(self, text):
        msgBox = self.window.makeMsgBox()
        msgBox.setText(text)
        msgBox.setIcon(msgBox.Icon.Critical)
        msgBox.exec()
        self.display.setFocus()

    def _showInfo(self, text):
        msgBox = self.window.makeMsgBox()
        msgBox.setText(text)
        msgBox.setIcon(msgBox.Icon.Critical)
        msgBox.exec()
        self.display.setFocus()
