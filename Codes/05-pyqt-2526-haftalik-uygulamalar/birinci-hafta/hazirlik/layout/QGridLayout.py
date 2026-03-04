import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

def window():
   app = QApplication(sys.argv)
   win = QWidget()
   grid = QGridLayout()
	
   for i in range(0,5):
      for j in range(0,5):
         grid.addWidget(QPushButton(str(i)+str(j)),i,j)
			
   win.setLayout(grid)
   win.setWindowTitle("PyQt Grid Example")
   win.setGeometry(50,50,200,200)
   win.show()
   sys.exit(app.exec_())

if __name__ == '__main__':
   window()