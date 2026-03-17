import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget,
    QVBoxLayout, QHBoxLayout,
    QProgressBar, QPushButton, QLabel
)
from PyQt5.QtCore import Qt, QTimer


class ProgressOrnek(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QProgressBar Örneği")
        self.setGeometry(200, 200, 480, 320)
        self._arayuz()
        self._timerKur()

    def _arayuz(self):
        ana = QVBoxLayout(self)
        ana.setContentsMargins(25, 20, 25, 20)
        ana.setSpacing(14)

        # ── Normal progress bar ───────────
        ana.addWidget(QLabel("İndirme İlerlemesi:"))
        self.bar1 = QProgressBar()
        self.bar1.setRange(0, 100)
        self.bar1.setValue(0)
        self.bar1.setFormat("%v / 100 MB (%p%)")   # Özel format
        self.bar1.setStyleSheet("""
            QProgressBar { border-radius:6px; background:#1e293b; height:22px; }
            QProgressBar::chunk { background:#6366f1; border-radius:6px; }
        """)
        ana.addWidget(self.bar1)

        # ── Renk değişen bar ─────────────
        ana.addWidget(QLabel("İşlem İlerlemesi:"))
        self.bar2 = QProgressBar()
        self.bar2.setRange(0, 100)
        self.bar2.setValue(0)
        ana.addWidget(self.bar2)

        # ── Belirsiz mod (indeterminate) ──
        ana.addWidget(QLabel("Yükleniyor... (belirsiz mod):"))
        self.bar3 = QProgressBar()
        self.bar3.setRange(0, 0)           # 0,0 = belirsiz mod (sürekli animasyon)
        self.bar3.setStyleSheet("""
            QProgressBar { border-radius:6px; background:#1e293b; height:18px; }
            QProgressBar::chunk { background:#22d3ee; border-radius:6px; }
        """)
        ana.addWidget(self.bar3)

        # ── Butonlar ─────────────────────
        buton_layout = QHBoxLayout()
        self.baslatBtn = QPushButton("Başlat")
        self.durdurBtn = QPushButton("Durdur")
        self.sifirlaBtn = QPushButton("Sıfırla")
        self.durdurBtn.setEnabled(False)
        self.baslatBtn.clicked.connect(self._baslat)
        self.durdurBtn.clicked.connect(self._durdur)
        self.sifirlaBtn.clicked.connect(self._sifirla)
        for b in [self.baslatBtn, self.durdurBtn, self.sifirlaBtn]:
            buton_layout.addWidget(b)
        ana.addLayout(buton_layout)

        self.durumLabel = QLabel("Başlatmak için butona basın.")
        self.durumLabel.setAlignment(Qt.AlignCenter)
        self.durumLabel.setStyleSheet("color:#94a3b8;")
        ana.addWidget(self.durumLabel)

    def _timerKur(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self._ilerlemeGuncelle)

    def _baslat(self):
        self.timer.start(80)               # Her 80ms'de bir güncelle
        self.baslatBtn.setEnabled(False)
        self.durdurBtn.setEnabled(True)
        self.durumLabel.setText("İşlem devam ediyor...")

    def _durdur(self):
        self.timer.stop()
        self.baslatBtn.setEnabled(True)
        self.durdurBtn.setEnabled(False)
        self.durumLabel.setText("Duraklatıldı.")

    def _sifirla(self):
        self.timer.stop()
        self.bar1.setValue(0)
        self.bar2.setValue(0)
        self.baslatBtn.setEnabled(True)
        self.durdurBtn.setEnabled(False)
        self.durumLabel.setText("Başlatmak için butona basın.")

    def _ilerlemeGuncelle(self):
        deger = self.bar1.value() + 1
        self.bar1.setValue(deger)
        self.bar2.setValue(deger)

        # Renge göre bar2'yi güncelle
        if deger < 40:
            renk = "#22c55e"
        elif deger < 75:
            renk = "#f59e0b"
        else:
            renk = "#ef4444"
        self.bar2.setStyleSheet(f"""
            QProgressBar {{ border-radius:6px; background:#1e293b; height:22px; }}
            QProgressBar::chunk {{ background:{renk}; border-radius:6px; }}
        """)

        if deger >= 100:
            self.timer.stop()
            self.durumLabel.setText("Tamamlandı!")
            self.baslatBtn.setEnabled(True)
            self.durdurBtn.setEnabled(False)


app = QApplication(sys.argv)
pencere = ProgressOrnek()
pencere.show()
sys.exit(app.exec_())
