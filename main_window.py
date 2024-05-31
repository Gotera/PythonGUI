from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout

class MainWindow(QMainWindow):
  def __init__(self, *args, **kwargs) -> None:
    super().__init__(*args, **kwargs)
    
    self.cw = QWidget()
    self.vLayout = QVBoxLayout()
    self.cw.setLayout(self.vLayout)
    self.setCentralWidget(self.cw)
    
    self.setWindowTitle('Calculadora')
    
  def adjustFixedSize(self):
    self.adjustSize()
    self.setFixedSize(self.width(), self.height())
      
  def addWidgetToVLayout(self, widget: QWidget):
    self.vLayout.addWidget(widget)