"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 PyQt5 Mini Örnek — CSV Dışa Aktarma
 Konu : SQLite → CSV ve QFileDialog entegrasyonu
 Hafta: 6
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
import sys, sqlite3, csv, os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem,
    QPushButton, QLabel, QFileDialog, QMessageBox
)
from PyQt5.QtCore import Qt


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
    ])
    db.commit()
    return db


class CSVExport(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SQLite → CSV Dışa Aktarma")
        self.setGeometry(200, 200, 680, 420)
        self.db = db_hazirla()
        self._arayuz()
        self._tabloYukle()

    def _arayuz(self):
        merkez = QWidget()
        self.setCentralWidget(merkez)
        ana = QVBoxLayout(merkez)
        ana.setContentsMargins(12, 12, 12, 12)
        ana.setSpacing(8)

        # Tablo
        self.tablo = QTableWidget()
        self.tablo.setColumnCount(6)
        self.tablo.setHorizontalHeaderLabels(["ID","Ad","Soyad","Bölüm","GPA","Şehir"])
        self.tablo.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tablo.setSelectionBehavior(QTableWidget.SelectRows)
        self.tablo.setAlternatingRowColors(True)
        self.tablo.horizontalHeader().setStretchLastSection(True)
        ana.addWidget(self.tablo)

        # Butonlar
        btn_layout = QHBoxLayout()

        self.csvBtn = QPushButton("📥  CSV Olarak Dışa Aktar")
        self.csvBtn.setStyleSheet("background:#22c55e;color:white;padding:9px 18px;font-weight:bold;border-radius:7px;")
        self.csvBtn.clicked.connect(self._csvExport)

        self.tumCsvBtn = QPushButton("📊  Tüm Tabloyu CSV'ye Aktar")
        self.tumCsvBtn.setStyleSheet("background:#3b82f6;color:white;padding:9px 18px;font-weight:bold;border-radius:7px;")
        self.tumCsvBtn.clicked.connect(lambda: self._csvExport(tum=True))

        for btn in [self.csvBtn, self.tumCsvBtn]:
            btn_layout.addWidget(btn)
        ana.addLayout(btn_layout)

        self.durumLabel = QLabel("CSV export için butona tıklayın.")
        self.durumLabel.setStyleSheet("color:#64748b; padding:4px;")
        ana.addWidget(self.durumLabel)

    def _tabloYukle(self):
        cur = self.db.cursor()
        cur.execute("SELECT * FROM ogrenciler")
        satirlar = cur.fetchall()
        self.tablo.setRowCount(len(satirlar))
        for ri, satir in enumerate(satirlar):
            for ci, deger in enumerate(satir):
                item = QTableWidgetItem(str(deger))
                item.setTextAlignment(Qt.AlignCenter)
                self.tablo.setItem(ri, ci, item)

    def _csvExport(self, tum=False):
        # Kayıt konumu seç
        dosya_yolu, _ = QFileDialog.getSaveFileName(
            self, "CSV Dosyasını Kaydet", "ogrenciler.csv",
            "CSV Dosyaları (*.csv);;Tüm Dosyalar (*)"
        )
        if not dosya_yolu:
            return

        try:
            cur = self.db.cursor()
            cur.execute("SELECT * FROM ogrenciler")
            satirlar = cur.fetchall()

            # Sütun başlıklarını al
            basliklar = [desc[0] for desc in cur.description]

            with open(dosya_yolu, "w", newline="", encoding="utf-8-sig") as f:
                # utf-8-sig → Excel'de Türkçe karakterler için
                yazar = csv.writer(f)
                yazar.writerow(basliklar)   # Başlık satırı
                yazar.writerows(satirlar)   # Veri satırları

            boyut = os.path.getsize(dosya_yolu)
            self.durumLabel.setText(
                f"✅ {len(satirlar)} satır → {dosya_yolu}  ({boyut} byte)"
            )
            QMessageBox.information(self, "Başarılı",
                f"✅ {len(satirlar)} kayıt dışa aktarıldı!\n\n"
                f"📄 Dosya: {dosya_yolu}\n"
                f"📦 Boyut: {boyut} byte"
            )
            self.statusBar().showMessage(f"CSV kaydedildi: {dosya_yolu}", 5000)

        except Exception as e:
            QMessageBox.critical(self, "Hata", f"CSV yazılamadı:\n{str(e)}")


app = QApplication(sys.argv)
pencere = CSVExport()
pencere.show()
sys.exit(app.exec_())
