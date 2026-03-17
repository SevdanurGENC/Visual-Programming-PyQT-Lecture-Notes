import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QAction,
    QTextEdit, QToolBar, QLabel, QFontComboBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class ToolbarOrnek(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QToolBar Örneği")
        self.setGeometry(200, 200, 600, 380)

        self.editor = QTextEdit()
        self.setCentralWidget(self.editor)

        self._toolbarOlustur()

    def _toolbarOlustur(self):
        toolbar = QToolBar("Ana Araç Çubuğu")
        toolbar.setMovable(True)           # Sürüklenebilir yap
        toolbar.setFloatable(False)        # Yüzer moda izin verme
        self.addToolBar(toolbar)           # Pencereye ekle

        # ── Eylemler ──────────────────────
        kalinAct = QAction("𝐁  Kalın", self)
        kalinAct.setCheckable(True)        # Açma/kapama durumu
        kalinAct.setShortcut("Ctrl+B")
        kalinAct.toggled.connect(self._kalinToggle)
        toolbar.addAction(kalinAct)

        italikAct = QAction("𝐼  İtalik", self)
        italikAct.setCheckable(True)
        italikAct.setShortcut("Ctrl+I")
        italikAct.toggled.connect(self._italikToggle)
        toolbar.addAction(italikAct)

        altCizgiAct = QAction("U̲  Alt Çizgi", self)
        altCizgiAct.setCheckable(True)
        altCizgiAct.toggled.connect(self._altCizgiToggle)
        toolbar.addAction(altCizgiAct)

        toolbar.addSeparator()             # Ayırıcı

        # Yazı tipi seçici — toolbar içine widget de eklenebilir
        fontCombo = QFontComboBox()
        fontCombo.setFixedWidth(160)
        fontCombo.currentFontChanged.connect(
            lambda f: self.editor.setCurrentFont(f)
        )
        toolbar.addWidget(QLabel("Font: "))
        toolbar.addWidget(fontCombo)

        toolbar.addSeparator()

        temizleAct = QAction("Temizle", self)
        temizleAct.triggered.connect(self.editor.clear)
        toolbar.addAction(temizleAct)

    def _kalinToggle(self, durum):
        w = self.editor.fontWeight()
        self.editor.setFontWeight(QFont.Bold if durum else QFont.Normal)

    def _italikToggle(self, durum):
        self.editor.setFontItalic(durum)

    def _altCizgiToggle(self, durum):
        self.editor.setFontUnderline(durum)


app = QApplication(sys.argv)
pencere = ToolbarOrnek()
pencere.show()
sys.exit(app.exec_())
