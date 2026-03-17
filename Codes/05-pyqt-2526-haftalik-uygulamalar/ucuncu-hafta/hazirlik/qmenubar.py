import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QAction,
    QTextEdit, QMessageBox
)
from PyQt5.QtGui import QKeySequence


class MenuOrnek(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QMenuBar Örneği")
        self.setGeometry(200, 200, 500, 350)

        # Merkez widget
        self.editor = QTextEdit()
        self.editor.setPlaceholderText("Buraya yazın...")
        self.setCentralWidget(self.editor)

        self._menuOlustur()

    def _menuOlustur(self):
        menubar = self.menuBar()          # Ana menü çubuğunu al

        # ── Dosya Menüsü ──────────────────
        dosyaMenu = menubar.addMenu("&Dosya")

        yeniAct = QAction("Yeni", self)
        yeniAct.setShortcut(QKeySequence("Ctrl+N"))   # Klavye kısayolu
        yeniAct.triggered.connect(self._yeni)
        dosyaMenu.addAction(yeniAct)

        dosyaMenu.addSeparator()          # Ayırıcı çizgi

        cikisAct = QAction("Çıkış", self)
        cikisAct.setShortcut(QKeySequence("Ctrl+Q"))
        cikisAct.triggered.connect(self.close)
        dosyaMenu.addAction(cikisAct)

        # ── Düzen Menüsü ──────────────────
        duzenMenu = menubar.addMenu("&Düzen")

        temizleAct = QAction("Temizle", self)
        temizleAct.triggered.connect(lambda: self.editor.clear())
        duzenMenu.addAction(temizleAct)

        # ── Yardım Menüsü ─────────────────
        yardimMenu = menubar.addMenu("&Yardım")
        hakkindaAct = QAction("Hakkında", self)
        hakkindaAct.triggered.connect(self._hakkinda)
        yardimMenu.addAction(hakkindaAct)

    def _yeni(self):
        self.editor.clear()
        self.statusBar().showMessage("Yeni dosya oluşturuldu.", 3000)

    def _hakkinda(self):
        QMessageBox.information(self, "Hakkında",
            "QMenuBar Mini Örnek\nPyQt5 — Hafta 3")


app = QApplication(sys.argv)
pencere = MenuOrnek()
pencere.show()
sys.exit(app.exec_())
