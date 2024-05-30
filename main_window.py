from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout

class MainWindow(QMainWindow):
  def __init__(self, *args, **kwargs) -> None:
    super().__init__(*args, **kwargs)
    
    self.cw = QWidget()
    self.v_layout = QVBoxLayout()
    self.cw.setLayout(self.v_layout)
    self.setCentralWidget(self.cw)
    
    self.setWindowTitle('Calculadora')
    
  def adjustFixedSize(self):
    self.adjustSize()
    self.setFixedSize(self.width(), self.height())
      
  def addWidgetToVLayout(self, widget: QWidget):
    self.v_layout.addWidget(widget)