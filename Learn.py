from msilib.schema import SelfReg
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
import sys
from PyQt5.QtGui import QIcon

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("First Window") #Set the title of the frame
        self.setGeometry(200,200,400,400) #Initial position of frame
        self.setFixedHeight(800) # Set frame height
        self.setFixedWidth(800) # Set frame width
        self.setStyleSheet('background-color:white') # Set frame background color
        self.create_buttons()

    def create_buttons(self):
        btn1 = QPushButton("Click Me", self)
app = QApplication(sys.argv)
frame = Window() # Create instance of clss frame
frame.show()
sys.exit(app.exec_())