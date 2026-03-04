"""
╔══════════════════════════════════════════════════════════════╗
║           PyQt5 - İlk Hafta Uygulama Örneği                  ║
║  Konular: QLabel, QLineEdit, QPushButton, QMessageBox        ║
║           Layout Yönetimi, Sinyal-Slot, OOP yapısı           ║
╚══════════════════════════════════════════════════════════════╝
"""

import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget,       # Temel pencere sınıfları
    QLabel, QLineEdit,           # Metin gösterme ve girişi
    QPushButton,                 # Buton
    QVBoxLayout, QHBoxLayout,    # Dikey ve yatay layout
    QMessageBox                  # Diyalog / popup penceresi
)
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtCore import Qt


# ─────────────────────────────────────────────
#  Ana pencere sınıfı — QWidget'tan türetildi
# ─────────────────────────────────────────────
class AnaPencere(QWidget):

    def __init__(self):
        super().__init__()           # Üst sınıfın __init__'ini çağır
        self.pencereAyarla()         # Pencere özelliklerini ayarla
        self.widgetleriOlustur()     # Widget'ları oluştur
        self.layoutDuzenle()         # Layout'u düzenle
        self.sinyalleriBasla()       # Sinyal-Slot bağlantıları

    # ── Pencere Ayarları ──────────────────────
    def pencereAyarla(self):
        self.setWindowTitle("PyQt5 - Temel Widget'lar")
        self.setGeometry(200, 200, 420, 380)
        self.setMinimumSize(380, 340)

         
    # ── Widget'ları Oluştur ───────────────────
    def widgetleriOlustur(self):

        # QLabel — Başlık
        self.baslikLabel = QLabel("Hoş Geldiniz!")
        self.baslikLabel.setObjectName("baslik")
        self.baslikLabel.setAlignment(Qt.AlignCenter)

        # QLabel — Açıklama yazısı
        self.aciklamaLabel = QLabel("Adınızı ve soyadınızı girerek başlayın.")
        self.aciklamaLabel.setObjectName("altYazi")
        self.aciklamaLabel.setAlignment(Qt.AlignCenter)

        # QLineEdit — Ad girişi
        self.adInput = QLineEdit()
        self.adInput.setPlaceholderText("Adınızı girin...")

        # QLineEdit — Soyad girişi
        self.soyadInput = QLineEdit()
        self.soyadInput.setPlaceholderText("Soyadınızı girin...")

        # QPushButton — Selamlama butonu
        self.selamBtn = QPushButton("Merhaba De!")
        self.selamBtn.setObjectName("selamBtn")

        # QPushButton — Temizle butonu
        self.temizleBtn = QPushButton("Temizle")
        self.temizleBtn.setObjectName("temizleBtn")

        # QPushButton — Bilgi butonu
        self.bilgiBtn = QPushButton("Hakkında")
        self.bilgiBtn.setObjectName("bilgiBtn")

        # QLabel — Sonuç alanı (başlangıçta boş)
        self.sonucLabel = QLabel("")
        self.sonucLabel.setAlignment(Qt.AlignCenter)
        self.sonucLabel.setStyleSheet("""
            font-size: 15px;
            color: #2c3e50;
            font-weight: bold;
            padding: 12px;
            background: white;
            border-radius: 10px;
            border: 2px solid #dfe6e9;
        """)
        self.sonucLabel.setMinimumHeight(50)

    # ── Layout Düzenleme ──────────────────────
    def layoutDuzenle(self):

        # Ana dikey layout
        anaLayout = QVBoxLayout()
        anaLayout.setSpacing(12)
        anaLayout.setContentsMargins(25, 20, 25, 20)

        # Başlık ve açıklama ekle
        anaLayout.addWidget(self.baslikLabel)
        anaLayout.addWidget(self.aciklamaLabel)

        # Giriş alanlarını ekle
        anaLayout.addWidget(self.adInput)
        anaLayout.addWidget(self.soyadInput)

        # Butonları yan yana koy (HBoxLayout)
        butonLayout = QHBoxLayout()
        butonLayout.setSpacing(10)
        butonLayout.addWidget(self.selamBtn)
        butonLayout.addWidget(self.temizleBtn)
        butonLayout.addWidget(self.bilgiBtn)

        anaLayout.addLayout(butonLayout)    # Buton layout'unu ana layout'a ekle
        anaLayout.addWidget(self.sonucLabel)

        self.setLayout(anaLayout)           # Pencereye uygula

    # ── Sinyal - Slot Bağlantıları ────────────
    def sinyalleriBasla(self):
        # Her butonun clicked sinyali ilgili slot fonksiyonuna bağlanır
        self.selamBtn.clicked.connect(self.selamVer)
        self.temizleBtn.clicked.connect(self.temizle)
        self.bilgiBtn.clicked.connect(self.hakkinda)

        # Enter tuşuna basınca da selamlasın
        self.adInput.returnPressed.connect(self.selamVer)
        self.soyadInput.returnPressed.connect(self.selamVer)

    # ── Slot Fonksiyonları ────────────────────

    def selamVer(self):
        """Selamlama butonu tıklandığında çalışır."""
        ad    = self.adInput.text().strip()
        soyad = self.soyadInput.text().strip()

        if not ad and not soyad:
            # QMessageBox.warning — Uyarı diyaloğu
            QMessageBox.warning(
                self,                       # Ebeveyn pencere
                "Eksik Bilgi",              # Başlık
                "Lütfen en az adınızı girin!"  # Mesaj
            )
            return

        tam_ad = f"{ad} {soyad}".strip()
        self.sonucLabel.setText(f"Merhaba, {tam_ad}!")
        self.sonucLabel.setStyleSheet("""
            font-size: 15px;
            color: #27ae60;
            font-weight: bold;
            padding: 12px;
            background: #eafaf1;
            border-radius: 10px;
            border: 2px solid #a9dfbf;
        """)

    def temizle(self):
        """Temizle butonu — tüm alanları sıfırlar."""
        self.adInput.clear()
        self.soyadInput.clear()
        self.sonucLabel.setText("")
        self.sonucLabel.setStyleSheet("""
            font-size: 15px;
            color: #2c3e50;
            font-weight: bold;
            padding: 12px;
            background: white;
            border-radius: 10px;
            border: 2px solid #dfe6e9;
        """)
        self.adInput.setFocus()     # Odağı ad alanına gönder

    def hakkinda(self):
        """QMessageBox.information — Bilgi diyaloğu."""
        QMessageBox.information(
            self,
            "Uygulama Hakkında",
            "PyQt5 - İlk Hafta Örneği\n\n"
            "Bu uygulamada şunları öğrendik:\n"
            "  • QLabel  → metin gösterme\n"
            "  • QLineEdit  → metin girişi\n"
            "  • QPushButton  → buton\n"
            "  • QMessageBox  → diyalog penceresi\n"
            "  • VBoxLayout / HBoxLayout  → düzen\n"
            "  • Sinyal & Slot  → olay yönetimi\n\n"
            "İyi dersler!"
        )


# ─────────────────────────────────────────────
#  Uygulamayı Başlat
# ─────────────────────────────────────────────
if __name__ == "__main__":
    app = QApplication(sys.argv)    # Her PyQt5 uygulaması bununla başlar
    pencere = AnaPencere()          # Ana penceremizi oluştur
    pencere.show()                  # Göster
    sys.exit(app.exec_())           # Olay döngüsünü başlat