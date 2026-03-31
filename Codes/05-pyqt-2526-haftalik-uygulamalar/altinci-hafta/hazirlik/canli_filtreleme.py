"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 PyQt5 Mini Örnek — Canlı Arama & Filtreleme
 Konu : textChanged sinyali ile anlık SQL filtresi
 Hafta: 6
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
import sys, sqlite3
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QGridLayout,
    QTableWidget, QTableWidgetItem,
    QLineEdit, QComboBox, QLabel, QPushButton
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor


def db_hazirla():
    db = sqlite3.connect(":memory:")
    cur = db.cursor()
    cur.execute("CREATE TABLE ogrenciler (id INTEGER PRIMARY KEY, ad TEXT, soyad TEXT, bolum TEXT, gpa REAL, sehir TEXT)")
    cur.executemany("INSERT INTO ogrenciler VALUES (?,?,?,?,?,?)", [
        (1,"Ahmet","Yılmaz","Bilgisayar",3.45,"Ankara"),
        (2,"Zeynep","Kaya","Elektrik",3.80,"İstanbul"),
        (3,"Mehmet","Demir","Makine",2.95,"İzmir"),
        (4,"Elif","Çelik","Bilgisayar",3.92,"Ankara"),
        (5,"Can","Arslan","Endüstri",3.10,"Bursa"),
        (6,"Selin","Öztürk","Bilgisayar",3.67,"İstanbul"),
        (7,"Burak","Şahin","Elektrik",2.40,"Ankara"),
        (8,"Ayşe","Güneş","Makine",3.55,"İzmir"),
        (9,"Kemal","Yıldız","Endüstri",2.80,"Bursa"),
        (10,"Deniz","Aktaş","Bilgisayar",4.00,"İstanbul"),
    ])
    db.commit()
    return db


class CanliArama(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Canlı Arama & Filtreleme")
        self.setGeometry(150, 130, 720, 500)
        self.db = db_hazirla()
        self._arayuz()
        self.filtrele()   # Başlangıçta tümünü göster

    def _arayuz(self):
        merkez = QWidget()
        self.setCentralWidget(merkez)
        ana = QVBoxLayout(merkez)
        ana.setContentsMargins(12, 12, 12, 12)
        ana.setSpacing(8)

        # ── Filtre satırı ─────────────────────────
        filtre_layout = QGridLayout()

        filtre_layout.addWidget(QLabel("🔍 Ad/Soyad Ara:"), 0, 0)
        self.aramaInput = QLineEdit()
        self.aramaInput.setPlaceholderText("yazın... (anlık filtreler)")
        self.aramaInput.setStyleSheet("padding:7px; border-radius:6px; border:1px solid #3b82f6;")
        filtre_layout.addWidget(self.aramaInput, 0, 1)

        filtre_layout.addWidget(QLabel("📚 Bölüm:"), 0, 2)
        self.bolumCombo = QComboBox()
        self.bolumCombo.addItems(["Tümü", "Bilgisayar", "Elektrik", "Makine", "Endüstri"])
        filtre_layout.addWidget(self.bolumCombo, 0, 3)

        filtre_layout.addWidget(QLabel("📊 Min GPA:"), 1, 0)
        self.minGpaInput = QLineEdit()
        self.minGpaInput.setPlaceholderText("örn: 3.0")
        filtre_layout.addWidget(self.minGpaInput, 1, 1)

        filtre_layout.addWidget(QLabel("🏙 Şehir:"), 1, 2)
        self.sehirCombo = QComboBox()
        self.sehirCombo.addItems(["Tümü", "Ankara", "İstanbul", "İzmir", "Bursa"])
        filtre_layout.addWidget(self.sehirCombo, 1, 3)

        self.temizleBtn = QPushButton("🗑 Filtreleri Temizle")
        self.temizleBtn.clicked.connect(self._temizle)
        filtre_layout.addWidget(self.temizleBtn, 1, 4)

        ana.addLayout(filtre_layout)

        # ── Tablo ─────────────────────────────────
        self.tablo = QTableWidget()
        self.tablo.setColumnCount(6)
        self.tablo.setHorizontalHeaderLabels(["ID","Ad","Soyad","Bölüm","GPA","Şehir"])
        self.tablo.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tablo.setSelectionBehavior(QTableWidget.SelectRows)
        self.tablo.setAlternatingRowColors(True)
        self.tablo.horizontalHeader().setStretchLastSection(True)
        for i, w in enumerate([45, 90, 100, 130, 65, 100]):
            self.tablo.setColumnWidth(i, w)
        ana.addWidget(self.tablo)

        self.sonucLabel = QLabel()
        self.sonucLabel.setStyleSheet("color:#64748b; padding:3px;")
        ana.addWidget(self.sonucLabel)

        # ── Canlı filtre sinyalleri ───────────────
        # textChanged → her tuş vuruşunda tetiklenir
        self.aramaInput.textChanged.connect(self.filtrele)
        self.minGpaInput.textChanged.connect(self.filtrele)
        # currentIndexChanged → combo değişince tetiklenir
        self.bolumCombo.currentIndexChanged.connect(self.filtrele)
        self.sehirCombo.currentIndexChanged.connect(self.filtrele)

    def filtrele(self):
        """Filtre değerlerine göre dinamik SQL oluşturur."""
        arama  = self.aramaInput.text().strip()
        bolum  = self.bolumCombo.currentText()
        sehir  = self.sehirCombo.currentText()
        min_gpa_str = self.minGpaInput.text().strip()

        # Dinamik WHERE koşulları
        kosullar = []
        params   = []

        if arama:
            kosullar.append("(ad LIKE ? OR soyad LIKE ?)")
            params += [f"%{arama}%", f"%{arama}%"]

        if bolum != "Tümü":
            kosullar.append("bolum = ?")
            params.append(bolum)

        if sehir != "Tümü":
            kosullar.append("sehir = ?")
            params.append(sehir)

        try:
            min_gpa = float(min_gpa_str) if min_gpa_str else None
            if min_gpa is not None:
                kosullar.append("gpa >= ?")
                params.append(min_gpa)
        except ValueError:
            pass

        where = "WHERE " + " AND ".join(kosullar) if kosullar else ""
        sql = f"SELECT id, ad, soyad, bolum, gpa, sehir FROM ogrenciler {where} ORDER BY ad"

        cur = self.db.cursor()
        cur.execute(sql, params)
        satirlar = cur.fetchall()

        self.tablo.setRowCount(len(satirlar))
        for ri, satir in enumerate(satirlar):
            for ci, deger in enumerate(satir):
                if ci == 4:
                    item = QTableWidgetItem(f"{deger:.2f}")
                    renk = "#22c55e" if deger >= 3.5 else ("#f59e0b" if deger >= 2.5 else "#ef4444")
                    item.setForeground(QColor(renk))
                else:
                    item = QTableWidgetItem(str(deger))
                item.setTextAlignment(Qt.AlignCenter)
                self.tablo.setItem(ri, ci, item)

        self.sonucLabel.setText(f"🔎 {len(satirlar)} sonuç bulundu  |  SQL: {sql[:80]}...")

    def _temizle(self):
        self.aramaInput.clear()
        self.minGpaInput.clear()
        self.bolumCombo.setCurrentIndex(0)
        self.sehirCombo.setCurrentIndex(0)


app = QApplication(sys.argv)
pencere = CanliArama()
pencere.show()
sys.exit(app.exec_())
