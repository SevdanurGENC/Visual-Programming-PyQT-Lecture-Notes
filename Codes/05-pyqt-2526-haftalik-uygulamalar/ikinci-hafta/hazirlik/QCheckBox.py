import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QCheckBox

class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        cb = QCheckBox('Movie', self)
        cb.move(20, 20)

        cb2 = QCheckBox('Music', self)
        cb2.move(20, 40)
        cb2.toggle()

        self.setGeometry(50,50,320,200)
        self.setWindowTitle("Checkbox Example")
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())