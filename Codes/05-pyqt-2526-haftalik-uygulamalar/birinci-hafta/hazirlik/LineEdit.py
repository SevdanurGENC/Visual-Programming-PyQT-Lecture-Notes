import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton

class Example(QMainWindow):
    
    def __init__(self):
        super().__init__()
                
        self.lineEntry = QLineEdit(self)
        self.lineEntry.move(16,16)
        self.lineEntry.resize(200,100)

        self.qlabel = QLabel(self)
        self.qlabel.move(16,120)

        self.lineEntry.textChanged.connect(self.onChanged)
        
        self.setGeometry(50,50,320,200)
        self.setWindowTitle("QLineEdit Example")
        self.show()

    def onChanged(self, text):
        self.qlabel.setText(text)
        self.qlabel.adjustSize()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())