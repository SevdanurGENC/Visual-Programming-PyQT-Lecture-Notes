import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QPushButton, QLabel, QStatusBar
)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont
import datetime


class StatusBarOrnek(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QStatusBar Örneği")
        self.setGeometry(200, 200, 500, 300)

        self._merkez()
        self._statusBarKur()

    def _merkez(self):
        merkez = QWidget()
        self.setCentralWidget(merkez)
        layout = QVBoxLayout(merkez)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)

        layout.addWidget(QLabel("Aşağıdaki butonlarla durum çubuğunu test edin:"))

        for metin, renk, mesaj in [
            ("Başarı Mesajı",  "#22c55e", "İşlem başarıyla tamamlandı!"),
            ("Uyarı Mesajı",  "#f59e0b", "Dikkat: Kaydedilmemiş değişiklik var."),
            ("Hata Mesajı",    "#ef4444", "Hata: Dosya bulunamadı!"),
            ("Bilgi Mesajı",  "#3b82f6", "Bilgi: Uygulama güncellendi."),
        ]:
            btn = QPushButton(metin)
            btn.setStyleSheet(f"background:{renk}; color:white; border-radius:6px; padding:7px;")
            # lambda varsayılan argüman tuzağına dikkat — m=mesaj kullan
            btn.clicked.connect(lambda _, m=mesaj: self.statusBar().showMessage(m, 4000))
            layout.addWidget(btn)

    def _statusBarKur(self):
        sb = self.statusBar()             # QMainWindow'dan gelir

        # ── Kalıcı widget'lar (sağda) ─────
        self.saatLabel = QLabel()
        self.saatLabel.setStyleSheet("color: #94a3b8; padding-right: 8px;")
        sb.addPermanentWidget(self.saatLabel)

        self.bilgiLabel = QLabel("Hazır")
        self.bilgiLabel.setStyleSheet("color: #22c55e; padding-right: 8px;")
        sb.addPermanentWidget(self.bilgiLabel)

        # Saati her saniye güncelle
        self.timer = QTimer()
        self.timer.timeout.connect(self._saatGuncelle)
        self.timer.start(1000)
        self._saatGuncelle()

        sb.showMessage("Hoş geldiniz! Bir butona tıklayın.", 3000)

    def _saatGuncelle(self):
        saat = datetime.datetime.now().strftime("%H:%M:%S")
        self.saatLabel.setText(f"{saat}")


app = QApplication(sys.argv)
pencere = StatusBarOrnek()
pencere.show()
sys.exit(app.exec_())
