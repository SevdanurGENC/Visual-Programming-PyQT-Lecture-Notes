"""
 Konu : Yüzer/sabitlenebilir panel
"""
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QDockWidget,
    QListWidget, QTextEdit, QLabel, QWidget, QVBoxLayout
)
from PyQt5.QtCore import Qt


class DockOrnek(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QDockWidget Örneği")
        self.setGeometry(150, 150, 700, 450)

        # ── Merkez alan ───────────────────
        self.editor = QTextEdit()
        self.editor.setPlaceholderText("Merkez alan — sol panelden bir konu seçin...")
        self.setCentralWidget(self.editor)

        self._solDockEkle()
        self._sagDockEkle()

    def _solDockEkle(self):
        # Sol dock — konu listesi
        dock = QDockWidget("📋Konuar", self)
        dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)

        liste = QListWidget()
        for konu in ["QMenuBar", "QToolBar", "QStatusBar",
                     "QDockWidget", "QDialog", "Dosya Dialogları"]:
            liste.addItem(konu)

        liste.currentTextChanged.connect(
            lambda metin: self.editor.setText(
                f"Seçilen konu: {metin}\n\nBuraya konu açıklaması gelecek..."
            )
        )

        dock.setWidget(liste)
        self.addDockWidget(Qt.LeftDockWidgetArea, dock)   # Sola yerleştir

    def _sagDockEkle(self):
        # Sağ dock — bilgi paneli
        dock = QDockWidget("Bilgi", self)
        dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        dock.setFeatures(
            QDockWidget.DockWidgetMovable |
            QDockWidget.DockWidgetFloatable   # Yüzebilir
            # DockWidgetClosable çıkarıldı — kapatılamaz
        )

        panel = QWidget()
        vbox  = QVBoxLayout(panel)
        vbox.addWidget(QLabel("Dock sürüklenebilir\n Yüzer moda alınabilir\n Kapatılamaz"))
        dock.setWidget(panel)
        self.addDockWidget(Qt.RightDockWidgetArea, dock)   # Sağa yerleştir


app = QApplication(sys.argv)
pencere = DockOrnek()
pencere.show()
sys.exit(app.exec_())
