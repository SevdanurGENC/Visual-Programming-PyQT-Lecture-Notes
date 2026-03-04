"""
╔══════════════════════════════════════════════════════════════════════╗
║           PyQt5 - İkinci Hafta Uygulama Örneği                       ║
║  Konular: QComboBox, QCheckBox, QRadioButton,                        ║
║           QSlider, QSpinBox, QTableWidget                            ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QMainWindow,
    QLabel, QPushButton, QLineEdit,
    QComboBox,          # Açılır seçim listesi
    QCheckBox,          # Çoklu seçim kutusu
    QRadioButton,       # Tek seçimli radyo butonu
    QSlider,            # Kaydırma çubuğu
    QSpinBox,           # Sayısal artış/azalış kutusu
    QTableWidget,       # Tablo widget'ı
    QTableWidgetItem,   # Tablo hücresi
    QVBoxLayout, QHBoxLayout, QGridLayout,
    QGroupBox,          # Çerçeveli grup kutusu
    QMessageBox, QTabWidget  # Sekmeli panel
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont


# ══════════════════════════════════════════════════════════
#  Ana Pencere — QTabWidget ile sekmeli yapı
# ══════════════════════════════════════════════════════════
class AnaPencere(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("🎓 PyQt5 — İkinci Hafta Widget'ları")
        self.setGeometry(150, 100, 750, 580)
        self.setMinimumSize(700, 530)
        self.setStyleSheet(self._stil())
        self._arayuzKur()

    # ── Genel Stil (QSS) ──────────────────────
    def _stil(self):
        return """
        QMainWindow, QWidget {
            background-color: #1a1d2e;
            color: #e2e8f0;
            font-family: 'Segoe UI';
            font-size: 13px;
        }
        QTabWidget::pane {
            border: 1px solid #2d3561;
            background: #1e2235;
        }
        QTabBar::tab {
            background: #252840;
            color: #94a3b8;
            padding: 8px 18px;
            margin-right: 2px;
            font-weight: bold;
        }
        QTabBar::tab:selected {
            background: #3b4fd8;
            color: white;
        }
        QGroupBox {
            border: 1px solid #2d3561;
            border-radius: 8px;
            margin-top: 14px;
            padding-top: 10px;
            font-weight: bold;
            color: #7c8cf8;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top left;
            padding: 0 8px;
        }
        QComboBox {
            background: #252840;
            border: 1px solid #3b4fd8;
            border-radius: 6px;
            padding: 5px 10px;
            color: #e2e8f0;
        }
        QComboBox::drop-down { border: none; }
        QComboBox QAbstractItemView {
            background: #252840;
            selection-background-color: #3b4fd8;
        }
        QCheckBox, QRadioButton {
            spacing: 8px;
            padding: 4px;
        }
        QCheckBox::indicator, QRadioButton::indicator {
            width: 18px; height: 18px;
        }
        QCheckBox::indicator:unchecked {
            border: 2px solid #3b4fd8;
            border-radius: 4px;
            background: transparent;
        }
        QCheckBox::indicator:checked {
            background: #3b4fd8;
            border: 2px solid #3b4fd8;
            border-radius: 4px;
        }
        QRadioButton::indicator:unchecked {
            border: 2px solid #7c8cf8;
            border-radius: 9px;
            background: transparent;
        }
        QRadioButton::indicator:checked {
            background: #7c8cf8;
            border: 2px solid #7c8cf8;
            border-radius: 9px;
        }
        QSlider::groove:horizontal {
            height: 6px;
            background: #2d3561;
            border-radius: 3px;
        }
        QSlider::handle:horizontal {
            background: #3b4fd8;
            width: 18px; height: 18px;
            margin: -6px 0;
            border-radius: 9px;
        }
        QSlider::sub-page:horizontal {
            background: #3b4fd8;
            border-radius: 3px;
        }
        QSpinBox {
            background: #252840;
            border: 1px solid #3b4fd8;
            border-radius: 6px;
            padding: 5px 10px;
            color: #e2e8f0;
        }
        QTableWidget {
            background: #1e2235;
            border: 1px solid #2d3561;
            gridline-color: #2d3561;
            color: #e2e8f0;
        }
        QTableWidget::item:selected {
            background: #3b4fd8;
        }
        QHeaderView::section {
            background: #252840;
            color: #7c8cf8;
            padding: 6px;
            border: 1px solid #2d3561;
            font-weight: bold;
        }
        QPushButton {
            background: #3b4fd8;
            color: white;
            border: none;
            border-radius: 7px;
            padding: 8px 18px;
            font-weight: bold;
        }
        QPushButton:hover { background: #4c5fe8; }
        QPushButton#silBtn { background: #dc2626; }
        QPushButton#silBtn:hover { background: #ef4444; }
        QPushButton#ekleBtn { background: #059669; }
        QPushButton#ekleBtn:hover { background: #10b981; }
        QLineEdit {
            background: #252840;
            border: 1px solid #3b4fd8;
            border-radius: 6px;
            padding: 6px 10px;
            color: #e2e8f0;
        }
        QLabel#sonuc {
            background: #252840;
            border-radius: 8px;
            padding: 10px;
            color: #7c8cf8;
            font-weight: bold;
        }
        """

    def _arayuzKur(self):
        merkez = QWidget()
        self.setCentralWidget(merkez)
        anaLayout = QVBoxLayout(merkez)
        anaLayout.setContentsMargins(10, 10, 10, 10)

        # Sekmeli panel
        self.sekmeler = QTabWidget()
        anaLayout.addWidget(self.sekmeler)

        # Her sekme ayrı bir widget
        self.sekmeler.addTab(self._comboRadioSekme(),  "🔽 Seçim Widget'ları")
        self.sekmeler.addTab(self._sliderSpinSekme(),  "🎚️ Sayısal Widget'lar")
        self.sekmeler.addTab(self._tableSekme(),       "📋 Tablo Widget'ı")

    # ══════════════════════════════════════════
    #  SEKME 1 — QComboBox, QCheckBox, QRadioButton
    # ══════════════════════════════════════════
    def _comboRadioSekme(self):
        sekme = QWidget()
        ana = QVBoxLayout(sekme)
        ana.setSpacing(12)

        # ── QComboBox ──
        comboGrup = QGroupBox("QComboBox — Açılır Liste")
        comboLayout = QGridLayout(comboGrup)

        comboLayout.addWidget(QLabel("Şehir seçin:"), 0, 0)
        self.sehirCombo = QComboBox()
        self.sehirCombo.addItems(["İstanbul", "Ankara", "İzmir", "Bursa", "Antalya", "Trabzon"])
        comboLayout.addWidget(self.sehirCombo, 0, 1)

        comboLayout.addWidget(QLabel("Dil seçin:"), 1, 0)
        self.dilCombo = QComboBox()
        self.dilCombo.addItems(["Python 🐍", "Java ☕", "C++ ⚙️", "JavaScript 🌐", "Rust 🦀"])
        comboLayout.addWidget(self.dilCombo, 1, 1)

        comboSonucBtn = QPushButton("Seçimleri Göster")
        comboSonucBtn.clicked.connect(self._comboSonuc)
        comboLayout.addWidget(comboSonucBtn, 2, 0, 1, 2)

        self.comboSonucLabel = QLabel("Henüz seçim yapılmadı.")
        self.comboSonucLabel.setObjectName("sonuc")
        comboLayout.addWidget(self.comboSonucLabel, 3, 0, 1, 2)
        ana.addWidget(comboGrup)

        # ── QCheckBox & QRadioButton ──
        altLayout = QHBoxLayout()

        # QCheckBox
        checkGrup = QGroupBox("QCheckBox — Çoklu Seçim")
        checkLayout = QVBoxLayout(checkGrup)
        self.checkBoxlar = []
        for konu in ["PyQt5", "NumPy", "Pandas", "Matplotlib", "Django"]:
            cb = QCheckBox(konu)
            self.checkBoxlar.append(cb)
            checkLayout.addWidget(cb)
        checkBtn = QPushButton("Seçilenleri Listele")
        checkBtn.clicked.connect(self._checkSonuc)
        checkLayout.addWidget(checkBtn)
        self.checkSonucLabel = QLabel("")
        self.checkSonucLabel.setObjectName("sonuc")
        self.checkSonucLabel.setWordWrap(True)
        checkLayout.addWidget(self.checkSonucLabel)
        altLayout.addWidget(checkGrup)

        # QRadioButton
        radioGrup = QGroupBox("QRadioButton — Tek Seçim")
        radioLayout = QVBoxLayout(radioGrup)
        radioLayout.addWidget(QLabel("Deneyim seviyeniz:"))
        self.radioButonlar = []
        for seviye in ["🌱 Başlangıç", "📘 Orta", "🚀 İleri", "🏆 Uzman"]:
            rb = QRadioButton(seviye)
            self.radioButonlar.append(rb)
            radioLayout.addWidget(rb)
        self.radioButonlar[0].setChecked(True)   # Varsayılan seçim
        radioBtn = QPushButton("Seviyeyi Onayla")
        radioBtn.clicked.connect(self._radioSonuc)
        radioLayout.addWidget(radioBtn)
        self.radioSonucLabel = QLabel("")
        self.radioSonucLabel.setObjectName("sonuc")
        radioLayout.addWidget(self.radioSonucLabel)
        altLayout.addWidget(radioGrup)

        ana.addLayout(altLayout)
        return sekme

    def _comboSonuc(self):
        sehir = self.sehirCombo.currentText()
        dil   = self.dilCombo.currentText()
        self.comboSonucLabel.setText(f"📍 Şehir: {sehir}   |   💻 Dil: {dil}")

    def _checkSonuc(self):
        secili = [cb.text() for cb in self.checkBoxlar if cb.isChecked()]
        if secili:
            self.checkSonucLabel.setText("✅ " + ", ".join(secili))
        else:
            self.checkSonucLabel.setText("⚠️ Hiçbir şey seçilmedi!")

    def _radioSonuc(self):
        for rb in self.radioButonlar:
            if rb.isChecked():
                self.radioSonucLabel.setText(f"Seviyeniz: {rb.text()}")
                break

    # ══════════════════════════════════════════
    #  SEKME 2 — QSlider, QSpinBox
    # ══════════════════════════════════════════
    def _sliderSpinSekme(self):
        sekme = QWidget()
        ana = QVBoxLayout(sekme)
        ana.setSpacing(14)

        # ── QSlider ──
        sliderGrup = QGroupBox("QSlider — Kaydırma Çubuğu")
        sliderLayout = QVBoxLayout(sliderGrup)

        # Ses seviyesi slider
        sesLayout = QHBoxLayout()
        sesLayout.addWidget(QLabel("🔊 Ses Seviyesi:"))
        self.sesSlider = QSlider(Qt.Horizontal)
        self.sesSlider.setRange(0, 100)
        self.sesSlider.setValue(50)
        self.sesSlider.setTickInterval(10)
        self.sesSlider.setTickPosition(QSlider.TicksBelow)
        sesLayout.addWidget(self.sesSlider)
        self.sesLabel = QLabel("50")
        self.sesLabel.setFixedWidth(35)
        sesLayout.addWidget(self.sesLabel)
        self.sesSlider.valueChanged.connect(lambda v: self.sesLabel.setText(str(v)))
        sliderLayout.addLayout(sesLayout)

        # Parlaklık slider
        parlaklıkLayout = QHBoxLayout()
        parlaklıkLayout.addWidget(QLabel("☀️ Parlaklık:  "))
        self.parlakSlider = QSlider(Qt.Horizontal)
        self.parlakSlider.setRange(0, 100)
        self.parlakSlider.setValue(75)
        parlaklıkLayout.addWidget(self.parlakSlider)
        self.parlakLabel = QLabel("75")
        self.parlakLabel.setFixedWidth(35)
        parlaklıkLayout.addWidget(self.parlakLabel)
        self.parlakSlider.valueChanged.connect(lambda v: self.parlakLabel.setText(str(v)))
        sliderLayout.addLayout(parlaklıkLayout)

        # Renk slider (önizleme)
        renkLayout = QHBoxLayout()
        renkLayout.addWidget(QLabel("🎨 Kırmızı:    "))
        self.renkSlider = QSlider(Qt.Horizontal)
        self.renkSlider.setRange(0, 255)
        self.renkSlider.setValue(128)
        renkLayout.addWidget(self.renkSlider)
        self.renkLabel = QLabel("128")
        self.renkLabel.setFixedWidth(35)
        renkLayout.addWidget(self.renkLabel)
        self.renkOnizleme = QLabel()
        self.renkOnizleme.setFixedSize(60, 28)
        renkLayout.addWidget(self.renkOnizleme)
        self.renkSlider.valueChanged.connect(self._renkGuncelle)
        sliderLayout.addLayout(renkLayout)
        self._renkGuncelle(128)

        ana.addWidget(sliderGrup)

        # ── QSpinBox ──
        spinGrup = QGroupBox("QSpinBox — Sayısal Giriş")
        spinLayout = QGridLayout(spinGrup)

        spinLayout.addWidget(QLabel("Yaş:"), 0, 0)
        self.yasSpinBox = QSpinBox()
        self.yasSpinBox.setRange(1, 120)
        self.yasSpinBox.setValue(20)
        self.yasSpinBox.setSuffix(" yaş")
        spinLayout.addWidget(self.yasSpinBox, 0, 1)

        spinLayout.addWidget(QLabel("Not (0-100):"), 1, 0)
        self.notSpinBox = QSpinBox()
        self.notSpinBox.setRange(0, 100)
        self.notSpinBox.setValue(75)
        self.notSpinBox.setSingleStep(5)   # Her tıkta 5 artır/azalt
        spinLayout.addWidget(self.notSpinBox, 1, 1)

        spinLayout.addWidget(QLabel("Adet:"), 2, 0)
        self.adetSpinBox = QSpinBox()
        self.adetSpinBox.setRange(1, 99)
        self.adetSpinBox.setValue(1)
        self.adetSpinBox.setPrefix("x")
        spinLayout.addWidget(self.adetSpinBox, 2, 1)

        spinBtn = QPushButton("Değerleri Hesapla")
        spinBtn.clicked.connect(self._spinSonuc)
        spinLayout.addWidget(spinBtn, 3, 0, 1, 2)

        self.spinSonucLabel = QLabel("")
        self.spinSonucLabel.setObjectName("sonuc")
        self.spinSonucLabel.setWordWrap(True)
        spinLayout.addWidget(self.spinSonucLabel, 4, 0, 1, 2)

        ana.addWidget(spinGrup)
        return sekme

    def _renkGuncelle(self, deger):
        self.renkLabel.setText(str(deger))
        self.renkOnizleme.setStyleSheet(f"background-color: rgb({deger}, 50, 100); border-radius:4px;")

    def _spinSonuc(self):
        yas  = self.yasSpinBox.value()
        not_ = self.notSpinBox.value()
        adet = self.adetSpinBox.value()
        harf = "AA" if not_>=90 else ("BA" if not_>=80 else ("BB" if not_>=70 else ("CB" if not_>=60 else "FF")))
        self.spinSonucLabel.setText(
            f"👤 Yaş: {yas}  |  📝 Not: {not_} ({harf})  |  📦 Adet: {adet}"
        )

    # ══════════════════════════════════════════
    #  SEKME 3 — QTableWidget
    # ══════════════════════════════════════════
    def _tableSekme(self):
        sekme = QWidget()
        ana = QVBoxLayout(sekme)
        ana.setSpacing(10)

        # Giriş formu
        formLayout = QHBoxLayout()
        self.adInput    = QLineEdit(); self.adInput.setPlaceholderText("Ad Soyad")
        self.dersInput  = QLineEdit(); self.dersInput.setPlaceholderText("Ders")
        self.notInput   = QSpinBox();  self.notInput.setRange(0, 100); self.notInput.setValue(70)
        ekleBtn = QPushButton("➕ Satır Ekle"); ekleBtn.setObjectName("ekleBtn")
        silBtn  = QPushButton("🗑️ Seçili Sil"); silBtn.setObjectName("silBtn")
        ekleBtn.clicked.connect(self._satirEkle)
        silBtn.clicked.connect(self._satirSil)

        for w in [self.adInput, self.dersInput, self.notInput, ekleBtn, silBtn]:
            formLayout.addWidget(w)
        ana.addLayout(formLayout)

        # QTableWidget
        self.tablo = QTableWidget()
        self.tablo.setColumnCount(4)
        self.tablo.setHorizontalHeaderLabels(["Ad Soyad", "Ders", "Not", "Durum"])
        self.tablo.horizontalHeader().setStretchLastSection(True)
        self.tablo.setColumnWidth(0, 180)
        self.tablo.setColumnWidth(1, 180)
        self.tablo.setColumnWidth(2, 80)
        self.tablo.setEditTriggers(QTableWidget.NoEditTriggers)  # Salt okunur
        self.tablo.setSelectionBehavior(QTableWidget.SelectRows)
        ana.addWidget(self.tablo)

        # Örnek verilerle başlat
        ornekler = [
            ("Ahmet Yılmaz", "Görsel Programlama", 88),
            ("Zeynep Kaya",  "Veri Yapıları",      72),
            ("Mehmet Demir", "Algoritma",           55),
            ("Elif Çelik",   "Görsel Programlama",  95),
        ]
        for ad, ders, not_ in ornekler:
            self._tabloyaEkle(ad, ders, not_)

        # İstatistik çubuğu
        self.istatLabel = QLabel()
        self.istatLabel.setObjectName("sonuc")
        ana.addWidget(self.istatLabel)
        self._istatGuncelle()
        return sekme

    def _satirEkle(self):
        ad   = self.adInput.text().strip()
        ders = self.dersInput.text().strip()
        not_ = self.notInput.value()
        if not ad or not ders:
            QMessageBox.warning(self, "Eksik Bilgi", "Ad ve Ders alanları boş olamaz!")
            return
        self._tabloyaEkle(ad, ders, not_)
        self.adInput.clear(); self.dersInput.clear()
        self._istatGuncelle()

    def _tabloyaEkle(self, ad, ders, not_):
        satir = self.tablo.rowCount()
        self.tablo.insertRow(satir)
        durum = "✅ Geçti" if not_ >= 60 else "❌ Kaldı"
        for sut, deger in enumerate([ad, ders, str(not_), durum]):
            item = QTableWidgetItem(deger)
            item.setTextAlignment(Qt.AlignCenter)
            if sut == 3:
                item.setForeground(QColor("#22c55e" if not_ >= 60 else "#ef4444"))
            self.tablo.setItem(satir, sut, item)

    def _satirSil(self):
        secili = self.tablo.currentRow()
        if secili >= 0:
            self.tablo.removeRow(secili)
            self._istatGuncelle()
        else:
            QMessageBox.information(self, "Bilgi", "Silmek için bir satır seçin.")

    def _istatGuncelle(self):
        satir = self.tablo.rowCount()
        if satir == 0:
            self.istatLabel.setText("Tabloda veri yok.")
            return
        notlar = []
        for i in range(satir):
            item = self.tablo.item(i, 2)
            if item:
                notlar.append(int(item.text()))
        ort = sum(notlar) / len(notlar)
        gecti = sum(1 for n in notlar if n >= 60)
        self.istatLabel.setText(
            f"📊  Toplam: {satir} öğrenci  |  "
            f"Ortalama: {ort:.1f}  |  "
            f"Geçti: {gecti}  |  "
            f"Kaldı: {satir - gecti}"
        )


# ── Başlat ────────────────────────────────────
if __name__ == "__main__":
    app = QApplication(sys.argv)
    pencere = AnaPencere()
    pencere.show()
    sys.exit(app.exec_())