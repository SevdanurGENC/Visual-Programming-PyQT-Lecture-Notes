import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QTabWidget,
    QLabel, QLineEdit, QPushButton, QTextEdit
)
from PyQt5.QtCore import Qt


class TabOrnek(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QTabWidget Örneği")
        self.setGeometry(200, 150, 550, 380)

        sekmeler = QTabWidget()
        sekmeler.setTabPosition(QTabWidget.North)   # Üstte (North/South/East/West)
        sekmeler.setMovable(True)                   # Sekmeler sürüklenebilir

        sekmeler.addTab(self._profil(),  "Profil")
        sekmeler.addTab(self._notlar(),  "Notlar")
        sekmeler.addTab(self._ayarlar(), "Ayarlar")

        # Sekme değişince sinyal
        sekmeler.currentChanged.connect(
            lambda idx: self.statusBar().showMessage(
                f"Sekme {idx + 1} seçildi.", 2000
            )
        )

        self.setCentralWidget(sekmeler)

    def _profil(self):
        w = QWidget()
        v = QVBoxLayout(w)
        v.setContentsMargins(20, 15, 20, 15)
        v.setSpacing(10)
        for etiket, ph in [("Ad:", "Adınız"), ("Soyad:", "Soyadınız"), ("E-posta:", "ornek@mail.com")]:
            satir = QHBoxLayout()
            lbl = QLabel(etiket); lbl.setFixedWidth(70)
            satir.addWidget(lbl)
            satir.addWidget(QLineEdit(placeholderText=ph))
            v.addLayout(satir)
        v.addWidget(QPushButton("Kaydet"))
        v.addStretch()
        return w

    def _notlar(self):
        w = QWidget()
        v = QVBoxLayout(w)
        v.setContentsMargins(15, 15, 15, 15)
        te = QTextEdit(placeholderText="Notlarınızı buraya yazın...")
        v.addWidget(te)
        v.addWidget(QPushButton("Notu Kopyala"))
        return w

    def _ayarlar(self):
        w = QWidget()
        v = QVBoxLayout(w)
        v.setContentsMargins(20, 15, 20, 15)
        v.addWidget(QLabel("Uygulama ayarları burada gösterilir."))
        v.addWidget(QPushButton("Varsayılana Sıfırla"))
        v.addStretch()
        return w


app = QApplication(sys.argv)
pencere = TabOrnek()
pencere.show()
sys.exit(app.exec_())
