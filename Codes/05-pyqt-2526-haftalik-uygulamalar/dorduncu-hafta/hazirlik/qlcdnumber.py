import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget,
    QVBoxLayout, QHBoxLayout,
    QLCDNumber, QPushButton, QLabel, QSlider
)
from PyQt5.QtCore import Qt, QTimer, QTime


class LCDOrnek(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QLCDNumber Örneği")
        self.setGeometry(200, 200, 480, 420)
        self.setStyleSheet("background:#0f172a; color:#e2e8f0; font-family:'Segoe UI';")
        self._arayuz()
        self._saatTimerKur()

    def _arayuz(self):
        ana = QVBoxLayout(self)
        ana.setContentsMargins(25, 20, 25, 20)
        ana.setSpacing(16)

        # ── Dijital Saat ──────────────────
        ana.addWidget(QLabel("Dijital Saat:"))
        self.saatLCD = QLCDNumber(8)               # 8 hane
        self.saatLCD.setSegmentStyle(QLCDNumber.Flat)  # Flat/Outline/Filled
        self.saatLCD.setStyleSheet("""
            QLCDNumber {
                background: #1e293b;
                color: #22d3ee;
                border: 2px solid #334155;
                border-radius: 8px;
            }
        """)
        self.saatLCD.setMinimumHeight(70)
        ana.addWidget(self.saatLCD)

        # ── Geri Sayım Sayacı ─────────────
        ana.addWidget(QLabel("Geri Sayım (saniye):"))
        self.sayacLCD = QLCDNumber(4)
        self.sayacLCD.setSegmentStyle(QLCDNumber.Flat)
        self.sayacLCD.setStyleSheet("""
            QLCDNumber { background:#1e293b; color:#f59e0b;
                         border:2px solid #334155; border-radius:8px; }
        """)
        self.sayacLCD.setMinimumHeight(60)
        self.sayacLCD.display(60)
        self.sayacDeger = 60
        ana.addWidget(self.sayacLCD)

        # Süre kaydırıcı
        slider_layout = QHBoxLayout()
        slider_layout.addWidget(QLabel("Süre:"))
        self.sureSlider = QSlider(Qt.Horizontal)
        self.sureSlider.setRange(5, 120)
        self.sureSlider.setValue(60)
        self.sureSlider.valueChanged.connect(self._sureGuncelle)
        slider_layout.addWidget(self.sureSlider)
        self.sureDeger = QLabel("60 sn")
        slider_layout.addWidget(self.sureDeger)
        ana.addLayout(slider_layout)

        buton_layout = QHBoxLayout()
        self.baslatBtn = QPushButton("Başlat")
        self.durdurBtn = QPushButton("Durdur")
        self.sifirlaBtn = QPushButton("Sıfırla")
        self.durdurBtn.setEnabled(False)
        self.baslatBtn.clicked.connect(self._sayacBaslat)
        self.durdurBtn.clicked.connect(self._sayacDurdur)
        self.sifirlaBtn.clicked.connect(self._sayacSifirla)
        for b in [self.baslatBtn, self.durdurBtn, self.sifirlaBtn]:
            b.setStyleSheet("background:#334155;color:white;border-radius:6px;padding:7px;")
            buton_layout.addWidget(b)
        ana.addLayout(buton_layout)

    def _saatTimerKur(self):
        # Saat timer — her saniye çalışır
        self.saatTimer = QTimer()
        self.saatTimer.timeout.connect(self._saatGuncelle)
        self.saatTimer.start(1000)
        self._saatGuncelle()

        # Sayaç timer
        self.sayacTimer = QTimer()
        self.sayacTimer.timeout.connect(self._sayacTik)

    def _saatGuncelle(self):
        saat = QTime.currentTime().toString("hh:mm:ss")
        self.saatLCD.display(saat)

    def _sureGuncelle(self, deger):
        self.sureDeger.setText(f"{deger} sn")
        self.sayacDeger = deger
        self.sayacLCD.display(deger)

    def _sayacBaslat(self):
        self.sayacTimer.start(1000)
        self.baslatBtn.setEnabled(False)
        self.durdurBtn.setEnabled(True)

    def _sayacDurdur(self):
        self.sayacTimer.stop()
        self.baslatBtn.setEnabled(True)
        self.durdurBtn.setEnabled(False)

    def _sayacSifirla(self):
        self.sayacTimer.stop()
        self.sayacDeger = self.sureSlider.value()
        self.sayacLCD.display(self.sayacDeger)
        self.sayacLCD.setStyleSheet("""
            QLCDNumber { background:#1e293b; color:#f59e0b;
                         border:2px solid #334155; border-radius:8px; }
        """)
        self.baslatBtn.setEnabled(True)
        self.durdurBtn.setEnabled(False)

    def _sayacTik(self):
        self.sayacDeger -= 1
        self.sayacLCD.display(self.sayacDeger)

        # Son 10 saniyede kırmızıya dön
        if self.sayacDeger <= 10:
            self.sayacLCD.setStyleSheet("""
                QLCDNumber { background:#1e293b; color:#ef4444;
                             border:2px solid #ef4444; border-radius:8px; }
            """)

        if self.sayacDeger <= 0:
            self.sayacTimer.stop()
            self.baslatBtn.setEnabled(True)
            self.durdurBtn.setEnabled(False)


app = QApplication(sys.argv)
pencere = LCDOrnek()
pencere.show()
sys.exit(app.exec_())
