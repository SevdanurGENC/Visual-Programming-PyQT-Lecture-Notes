import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QPushButton,
    QTextEdit, QLabel, QFileDialog, QMessageBox
)


class DosyaDialogOrnek(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dosya Dialogları Örneği")
        self.setGeometry(150, 150, 600, 420)
        self.aktifDosya = None
        self._arayuzKur()

    def _arayuzKur(self):
        merkez = QWidget()
        self.setCentralWidget(merkez)
        ana = QVBoxLayout(merkez)
        ana.setContentsMargins(15, 15, 15, 15)
        ana.setSpacing(8)

        # Dosya yolu göstergesi
        self.yolLabel = QLabel("Dosya seçilmedi")
        self.yolLabel.setStyleSheet("color:#94a3b8; font-style:italic;")
        ana.addWidget(self.yolLabel)

        # Metin editörü
        self.editor = QTextEdit()
        self.editor.setPlaceholderText("Dosya açın veya buraya yazın...")
        ana.addWidget(self.editor)

        # Butonlar
        butonLayout = QHBoxLayout()
        for metin, renk, slot in [
            ("Dosya Aç",    "#3b82f6", self._dosyaAc),
            ("Kaydet",      "#22c55e", self._kaydet),
            ("Farklı Kaydet","#f59e0b", self._farkliKaydet),
            ("Klasör Seç",  "#8b5cf6", self._klasorSec),
        ]:
            btn = QPushButton(metin)
            btn.setStyleSheet(f"background:{renk};color:white;border-radius:6px;padding:8px 14px;font-weight:bold;")
            btn.clicked.connect(slot)
            butonLayout.addWidget(btn)
        ana.addLayout(butonLayout)

    def _dosyaAc(self):
        # getOpenFileName → tek dosya seçimi
        dosyaYolu, _ = QFileDialog.getOpenFileName(
            self,                                        # ebeveyn
            "Dosya Aç",                                  # başlık
            "",                                          # başlangıç dizini
            "Metin Dosyaları (*.txt);;Tüm Dosyalar (*)"  # filtreler
        )
        if dosyaYolu:
            try:
                with open(dosyaYolu, "r", encoding="utf-8") as f:
                    self.editor.setText(f.read())
                self.aktifDosya = dosyaYolu
                self.yolLabel.setText(f"{dosyaYolu}")
                self.statusBar().showMessage("Dosya açıldı.", 3000)
            except Exception as e:
                QMessageBox.critical(self, "Hata", str(e))

    def _kaydet(self):
        if not self.aktifDosya:
            self._farkliKaydet()
            return
        self._dosyaYaz(self.aktifDosya)

    def _farkliKaydet(self):
        # getSaveFileName → kayıt konumu seçimi
        dosyaYolu, _ = QFileDialog.getSaveFileName(
            self, "Farklı Kaydet", "",
            "Metin Dosyaları (*.txt);;Tüm Dosyalar (*)"
        )
        if dosyaYolu:
            self._dosyaYaz(dosyaYolu)
            self.aktifDosya = dosyaYolu
            self.yolLabel.setText(f"{dosyaYolu}")

    def _dosyaYaz(self, yol):
        try:
            with open(yol, "w", encoding="utf-8") as f:
                f.write(self.editor.toPlainText())
            self.statusBar().showMessage("Kaydedildi.", 3000)
        except Exception as e:
            QMessageBox.critical(self, "Hata", str(e))

    def _klasorSec(self):
        # getExistingDirectory → klasör seçimi
        klasor = QFileDialog.getExistingDirectory(self, "Klasör Seç")
        if klasor:
            self.yolLabel.setText(f"{klasor}")
            self.statusBar().showMessage(f"Klasör: {klasor}", 3000)


app = QApplication(sys.argv)
pencere = DosyaDialogOrnek()
pencere.show()
sys.exit(app.exec_())
