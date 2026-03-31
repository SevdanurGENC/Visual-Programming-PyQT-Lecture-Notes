"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 PyQt5 Mini Örnek — QTableWidget + SQLite
 Konu : Veritabanı verilerini tabloya aktarma
 Hafta: 6
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
import sys, sqlite3
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QPushButton, QLabel
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor


# ── Veritabanı yardımcısı ─────────────────────────────
def db_hazirla():
    """Bellek içi test veritabanı oluşturur."""
    db = sqlite3.connect(":memory:")
    cur = db.cursor()
    cur.execute("""
        CREATE TABLE ogrenciler (
            id INTEGER PRIMARY KEY, ad TEXT, soyad TEXT,
            bolum TEXT, gpa REAL, aktif INTEGER DEFAULT 1
        )
    """)
    cur.executemany("INSERT INTO ogrenciler (ad,soyad,bolum,gpa,aktif) VALUES (?,?,?,?,?)", [
        ("Ahmet","Yılmaz","Bilgisayar",3.45,1),
        ("Zeynep","Kaya","Elektrik",3.80,1),
        ("Mehmet","Demir","Makine",2.50,0),
        ("Elif","Çelik","Bilgisayar",3.92,1),
        ("Can","Arslan","Endüstri",1.80,0),
        ("Selin","Öztürk","Bilgisayar",3.67,1),
        ("Burak","Şahin","Elektrik",3.10,1),
    ])
    db.commit()
    return db


class TabloGosterimi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QTableWidget + SQLite")
        self.setGeometry(150, 150, 680, 440)
        self.db = db_hazirla()
        self._arayuz()
        self.verileriYukle()

    def _arayuz(self):
        merkez = QWidget()
        self.setCentralWidget(merkez)
        ana = QVBoxLayout(merkez)
        ana.setContentsMargins(12, 12, 12, 12)
        ana.setSpacing(8)

        # Üst buton satırı
        ust = QHBoxLayout()
        self.tumBtn  = QPushButton("🔄 Tümünü Göster")
        self.aktifBtn = QPushButton("✅ Aktif Öğrenciler")
        self.bilBtn  = QPushButton("💻 Bilgisayar Böl.")
        for btn in [self.tumBtn, self.aktifBtn, self.bilBtn]:
            btn.setStyleSheet("padding:7px 14px; font-weight:bold;")
            ust.addWidget(btn)
        ana.addLayout(ust)

        # Tablo
        self.tablo = QTableWidget()
        self.tablo.setColumnCount(6)
        self.tablo.setHorizontalHeaderLabels(["ID", "Ad", "Soyad", "Bölüm", "GPA", "Durum"])
        self.tablo.setColumnWidth(0, 45)
        self.tablo.setColumnWidth(1, 90)
        self.tablo.setColumnWidth(2, 100)
        self.tablo.setColumnWidth(3, 140)
        self.tablo.setColumnWidth(4, 65)
        self.tablo.setColumnWidth(5, 85)
        self.tablo.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tablo.setSelectionBehavior(QTableWidget.SelectRows)
        self.tablo.setAlternatingRowColors(True)   # ← Alternatif satır rengi
        self.tablo.horizontalHeader().setStretchLastSection(True)
        ana.addWidget(self.tablo)

        # Alt istatistik
        self.istatLabel = QLabel()
        self.istatLabel.setStyleSheet("color:#64748b; padding:4px;")
        ana.addWidget(self.istatLabel)

        # Sinyal bağlantıları
        self.tumBtn.clicked.connect(self.verileriYukle)
        self.aktifBtn.clicked.connect(lambda: self.verileriYukle("WHERE aktif=1"))
        self.bilBtn.clicked.connect(lambda: self.verileriYukle("WHERE bolum='Bilgisayar'"))

    def verileriYukle(self, where_clause=""):
        """SQLite'dan veri çekip tabloya yazar."""
        sql = f"SELECT id, ad, soyad, bolum, gpa, aktif FROM ogrenciler {where_clause} ORDER BY id"
        cur = self.db.cursor()
        cur.execute(sql)
        satirlar = cur.fetchall()

        # Tabloyu doldur
        self.tablo.setRowCount(len(satirlar))
        for satir_idx, satir in enumerate(satirlar):
            for col_idx, deger in enumerate(satir):
                if col_idx == 5:          # Durum sütunu
                    metin = "✅ Aktif" if deger else "❌ Pasif"
                    item = QTableWidgetItem(metin)
                    item.setForeground(QColor("#22c55e" if deger else "#ef4444"))
                elif col_idx == 4:        # GPA sütunu — renklendir
                    item = QTableWidgetItem(f"{deger:.2f}")
                    if deger >= 3.5:
                        item.setForeground(QColor("#22c55e"))
                    elif deger >= 2.5:
                        item.setForeground(QColor("#f59e0b"))
                    else:
                        item.setForeground(QColor("#ef4444"))
                else:
                    item = QTableWidgetItem(str(deger))
                item.setTextAlignment(Qt.AlignCenter)
                self.tablo.setItem(satir_idx, col_idx, item)

        # İstatistik
        gpalar = [s[4] for s in satirlar]
        ort = sum(gpalar) / len(gpalar) if gpalar else 0
        self.istatLabel.setText(
            f"📊 {len(satirlar)} kayıt  |  GPA Ort: {ort:.2f}  |  "
            f"Aktif: {sum(1 for s in satirlar if s[5])}  |  "
            f"Pasif: {sum(1 for s in satirlar if not s[5])}"
        )
        self.statusBar().showMessage(f"{len(satirlar)} kayıt yüklendi.", 3000)


app = QApplication(sys.argv)
pencere = TabloGosterimi()
pencere.show()
sys.exit(app.exec_())
