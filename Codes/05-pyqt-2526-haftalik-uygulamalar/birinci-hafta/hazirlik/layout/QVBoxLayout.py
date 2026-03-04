from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout

app = QApplication([])
window = QWidget()
layout = QVBoxLayout()
layout.addWidget(QPushButton('1'))
layout.addWidget(QPushButton('2'))
layout.addWidget(QPushButton('3'))

window.setLayout(layout)
window.show()
app.exec_()