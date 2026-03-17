import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QStackedWidget,
    QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QLineEdit
)
from PyQt5.QtCore import Qt


class SihirbazSayfasi(QWidget):
    """Her sihirbaz adımı için yeniden kullanılabilir sayfa."""
    def __init__(self, baslik, icerik_widget, renk):
        super().__init__()
        v = QVBoxLayout(self)
        v.setContentsMargins(40, 30, 40, 30)
        v.setSpacing(15)

        baslik_lbl = QLabel(baslik)
        baslik_lbl.setAlignment(Qt.AlignCenter)
        baslik_lbl.setStyleSheet(
            f"font-size:20px; font-weight:bold; color:{renk}; padding:10px;"
        )
        v.addWidget(baslik_lbl)
        v.addWidget(icerik_widget)
        v.addStretch()


class KayitSihirbazi(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QStackedWidget — Kayıt Sihirbazı")
        self.setGeometry(200, 200, 480, 340)

        ana = QVBoxLayout(self)
        ana.setContentsMargins(0, 0, 0, 0)

        # ── İlerleme göstergesi ───────────
        self.adimLabel = QLabel("Adım 1 / 3")
        self.adimLabel.setAlignment(Qt.AlignCenter)
        self.adimLabel.setStyleSheet("color:#94a3b8; padding:6px;")
        ana.addWidget(self.adimLabel)

        # ── QStackedWidget ────────────────
        self.yigin = QStackedWidget()

        # Sayfa 1 — Ad
        ad_widget = QWidget()
        QVBoxLayout(ad_widget).addWidget(QLineEdit(placeholderText="Adınız ve soyadınız"))
        self.yigin.addWidget(SihirbazSayfasi("Ad Bilgisi", ad_widget, "#6366f1"))

        # Sayfa 2 — E-posta
        mail_widget = QWidget()
        QVBoxLayout(mail_widget).addWidget(QLineEdit(placeholderText="E-posta adresiniz"))
        self.yigin.addWidget(SihirbazSayfasi("İletişim", mail_widget, "#22d3ee"))

        # Sayfa 3 — Özet
        ozet = QLabel("Kayıt tamamlandı!\nBilgileriniz kaydedildi.")
        ozet.setAlignment(Qt.AlignCenter)
        self.yigin.addWidget(SihirbazSayfasi("Tamamlandı", ozet, "#34d399"))

        ana.addWidget(self.yigin)

        # ── Gezinti butonları ─────────────
        btn_layout = QHBoxLayout()
        self.geriBtn  = QPushButton("Geri")
        self.ileriBtn = QPushButton("İleri")
        self.geriBtn.clicked.connect(self._geri)
        self.ileriBtn.clicked.connect(self._ileri)
        self.geriBtn.setEnabled(False)
        btn_layout.addWidget(self.geriBtn)
        btn_layout.addWidget(self.ileriBtn)
        ana.addLayout(btn_layout)

        self._butonGuncelle()

    def _ileri(self):
        mevcut = self.yigin.currentIndex()
        if mevcut < self.yigin.count() - 1:
            self.yigin.setCurrentIndex(mevcut + 1)   # Sonraki sayfaya geç
        self._butonGuncelle()

    def _geri(self):
        mevcut = self.yigin.currentIndex()
        if mevcut > 0:
            self.yigin.setCurrentIndex(mevcut - 1)   # Önceki sayfaya geç
        self._butonGuncelle()

    def _butonGuncelle(self):
        idx = self.yigin.currentIndex()
        self.geriBtn.setEnabled(idx > 0)
        self.ileriBtn.setText("Bitir" if idx == self.yigin.count() - 1 else "İleri")
        self.adimLabel.setText(f"Adım {idx + 1} / {self.yigin.count()}")


app = QApplication(sys.argv)
pencere = KayitSihirbazi()
pencere.show()
sys.exit(app.exec_())
