"""
╔══════════════════════════════════════════════════════════════════════════╗
║  PyQt5 + SQLite — Tam CRUD Uygulaması                                   ║
║  Konu: Öğrenci Yönetim Sistemi                                           ║
║  Hafta 6 — Dr. Öğr. Üyesi Sevdanur GENÇ                                 ║
╚══════════════════════════════════════════════════════════════════════════╝
  Özellikler:
    ✅ SQLite veritabanı (ogrenci_yonetim.db)
    ✅ CREATE / READ / UPDATE / DELETE (CRUD)
    ✅ QTableWidget ile canlı listeleme
    ✅ Anlık arama & bölüm filtresi
    ✅ CSV dışa aktarma
    ✅ Seçili kaydı forma otomatik yükleme
"""
import sys, sqlite3, csv, os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QComboBox, QPushButton,
    QTableWidget, QTableWidgetItem,
    QMessageBox, QFileDialog, QStatusBar, QGroupBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont

DB_DOSYA = "ogrenci_yonetim.db"


# ══════════════════════════════════════════════════════
#  VeritabaniYoneticisi — tüm SQL işlemleri burada
# ══════════════════════════════════════════════════════
class VeritabaniYoneticisi:

    def __init__(self, dosya=DB_DOSYA):
        self.dosya = dosya
        self._tablo_olustur()

    def _baglan(self):
        db = sqlite3.connect(self.dosya)
        db.row_factory = sqlite3.Row
        return db

    def _tablo_olustur(self):
        with self._baglan() as db:
            db.execute("""
                CREATE TABLE IF NOT EXISTS ogrenciler (
                    id       INTEGER PRIMARY KEY AUTOINCREMENT,
                    ad       TEXT    NOT NULL,
                    soyad    TEXT    NOT NULL,
                    numara   TEXT    UNIQUE NOT NULL,
                    bolum    TEXT    NOT NULL,
                    gpa      REAL    DEFAULT 0.0,
                    sehir    TEXT,
                    email    TEXT,
                    kayit_tarihi TEXT DEFAULT CURRENT_DATE
                )
            """)
            # Örnek veriler (tablo boşsa)
            if db.execute("SELECT COUNT(*) FROM ogrenciler").fetchone()[0] == 0:
                ornek = [
                    ("Ahmet","Yılmaz","23001","Bilgisayar Müh.",3.45,"Ankara","ahmet@mail.com"),
                    ("Zeynep","Kaya","23002","Elektrik Müh.",3.80,"İstanbul","zeynep@mail.com"),
                    ("Mehmet","Demir","23003","Makine Müh.",2.95,"İzmir","mehmet@mail.com"),
                    ("Elif","Çelik","23004","Bilgisayar Müh.",3.92,"Ankara","elif@mail.com"),
                    ("Can","Arslan","23005","Endüstri Müh.",3.10,"Bursa","can@mail.com"),
                    ("Selin","Öztürk","23006","Bilgisayar Müh.",3.67,"İstanbul","selin@mail.com"),
                    ("Burak","Şahin","23007","Elektrik Müh.",2.40,"Ankara","burak@mail.com"),
                    ("Ayşe","Güneş","23008","Makine Müh.",3.55,"İzmir","ayse@mail.com"),
                ]
                db.executemany(
                    "INSERT INTO ogrenciler (ad,soyad,numara,bolum,gpa,sehir,email) VALUES (?,?,?,?,?,?,?)",
                    ornek
                )

    def tumunuGetir(self, arama="", bolum="Tümü"):
        kosullar, params = [], []
        if arama:
            kosullar.append("(ad LIKE ? OR soyad LIKE ? OR numara LIKE ?)")
            params += [f"%{arama}%"] * 3
        if bolum != "Tümü":
            kosullar.append("bolum = ?")
            params.append(bolum)
        where = ("WHERE " + " AND ".join(kosullar)) if kosullar else ""
        with self._baglan() as db:
            return db.execute(
                f"SELECT id,ad,soyad,numara,bolum,gpa,sehir FROM ogrenciler {where} ORDER BY ad,soyad",
                params
            ).fetchall()

    def tekGetir(self, id_):
        with self._baglan() as db:
            return db.execute("SELECT * FROM ogrenciler WHERE id=?", (id_,)).fetchone()

    def ekle(self, veri):
        with self._baglan() as db:
            db.execute(
                "INSERT INTO ogrenciler (ad,soyad,numara,bolum,gpa,sehir,email) VALUES (?,?,?,?,?,?,?)",
                veri
            )
        return True

    def guncelle(self, id_, veri):
        with self._baglan() as db:
            db.execute(
                "UPDATE ogrenciler SET ad=?,soyad=?,numara=?,bolum=?,gpa=?,sehir=?,email=? WHERE id=?",
                (*veri, id_)
            )
        return True

    def sil(self, id_):
        with self._baglan() as db:
            db.execute("DELETE FROM ogrenciler WHERE id=?", (id_,))
        return True

    def istatistik(self):
        with self._baglan() as db:
            return db.execute("""
                SELECT COUNT(*) as toplam,
                       ROUND(AVG(gpa),2) as ort_gpa,
                       MAX(gpa) as max_gpa,
                       MIN(gpa) as min_gpa
                FROM ogrenciler
            """).fetchone()


# ══════════════════════════════════════════════════════
#  OgrenciFormu — giriş paneli
# ══════════════════════════════════════════════════════
class OgrenciFormu(QGroupBox):

    BOLUMLER = ["Bilgisayar Müh.", "Elektrik Müh.", "Makine Müh.",
                "Endüstri Müh.", "İnşaat Müh.", "Kimya Müh."]

    def __init__(self):
        super().__init__("📝 Öğrenci Bilgileri")
        self.setStyleSheet("QGroupBox { font-weight:bold; color:#6366f1; border:1px solid #334155; border-radius:8px; margin-top:10px; padding-top:10px; }")
        self.aktifId = None
        self._olustur()

    def _olustur(self):
        grid = QGridLayout(self)
        grid.setSpacing(8)
        grid.setContentsMargins(12, 16, 12, 12)

        self.alanlar = {}
        satirlar = [
            ("Ad:",     "ad",     "Öğrenci adı",     0, 0),
            ("Soyad:",  "soyad",  "Öğrenci soyadı",  0, 2),
            ("Numara:", "numara", "Örn: 23001",       1, 0),
            ("GPA:",    "gpa",    "0.0 – 4.0",        1, 2),
            ("Şehir:",  "sehir",  "Şehir adı",        2, 0),
            ("E-posta:","email",  "ornek@mail.com",   2, 2),
        ]
        for etiket, isim, ph, row, col in satirlar:
            grid.addWidget(QLabel(etiket), row, col)
            inp = QLineEdit()
            inp.setPlaceholderText(ph)
            inp.setStyleSheet("background:#1e293b; border:1px solid #334155; border-radius:6px; padding:6px; color:#e2e8f0;")
            grid.addWidget(inp, row, col + 1)
            self.alanlar[isim] = inp

        grid.addWidget(QLabel("Bölüm:"), 3, 0)
        self.bolumCombo = QComboBox()
        self.bolumCombo.addItems(self.BOLUMLER)
        self.bolumCombo.setStyleSheet("background:#1e293b; border:1px solid #334155; border-radius:6px; padding:6px; color:#e2e8f0;")
        grid.addWidget(self.bolumCombo, 3, 1, 1, 3)

        # Butonlar
        btn_layout = QHBoxLayout()
        self.ekleBtn     = QPushButton("➕  Ekle")
        self.guncelleBtn = QPushButton("✏️  Güncelle")
        self.silBtn      = QPushButton("🗑️  Sil")
        self.temizleBtn  = QPushButton("🔄  Temizle")

        stiller = [
            (self.ekleBtn,     "#059669", "#10b981"),
            (self.guncelleBtn, "#d97706", "#f59e0b"),
            (self.silBtn,      "#dc2626", "#ef4444"),
            (self.temizleBtn,  "#475569", "#64748b"),
        ]
        for btn, bg, hover in stiller:
            btn.setStyleSheet(f"background:{bg};color:white;border-radius:7px;padding:9px 16px;font-weight:bold;")
            btn_layout.addWidget(btn)

        self.guncelleBtn.setEnabled(False)
        self.silBtn.setEnabled(False)
        grid.addLayout(btn_layout, 4, 0, 1, 4)

    def degerler(self):
        """Form değerlerini tuple olarak döner."""
        return (
            self.alanlar["ad"].text().strip(),
            self.alanlar["soyad"].text().strip(),
            self.alanlar["numara"].text().strip(),
            self.bolumCombo.currentText(),
            self.alanlar["gpa"].text().strip(),
            self.alanlar["sehir"].text().strip(),
            self.alanlar["email"].text().strip(),
        )

    def yukle(self, kayit):
        """Seçili kaydı forma yükler."""
        self.alanlar["ad"].setText(kayit["ad"])
        self.alanlar["soyad"].setText(kayit["soyad"])
        self.alanlar["numara"].setText(kayit["numara"])
        self.alanlar["gpa"].setText(str(kayit["gpa"]))
        self.alanlar["sehir"].setText(kayit["sehir"] or "")
        self.alanlar["email"].setText(kayit["email"] or "")
        idx = self.bolumCombo.findText(kayit["bolum"])
        if idx >= 0:
            self.bolumCombo.setCurrentIndex(idx)
        self.aktifId = kayit["id"]
        self.guncelleBtn.setEnabled(True)
        self.silBtn.setEnabled(True)

    def temizle(self):
        for inp in self.alanlar.values():
            inp.clear()
        self.bolumCombo.setCurrentIndex(0)
        self.aktifId = None
        self.guncelleBtn.setEnabled(False)
        self.silBtn.setEnabled(False)

    def dogrula(self):
        ad, soyad, numara, bolum, gpa_str = (
            self.alanlar["ad"].text().strip(),
            self.alanlar["soyad"].text().strip(),
            self.alanlar["numara"].text().strip(),
            self.bolumCombo.currentText(),
            self.alanlar["gpa"].text().strip(),
        )
        if not ad or not soyad or not numara:
            return None, "Ad, soyad ve numara zorunludur!"
        try:
            gpa = float(gpa_str) if gpa_str else 0.0
            if not 0.0 <= gpa <= 4.0:
                return None, "GPA 0.0 ile 4.0 arasında olmalıdır!"
        except ValueError:
            return None, "GPA geçerli bir sayı olmalıdır!"
        return (ad, soyad, numara, bolum, gpa,
                self.alanlar["sehir"].text().strip(),
                self.alanlar["email"].text().strip()), None


# ══════════════════════════════════════════════════════
#  AnaUygulama — QMainWindow
# ══════════════════════════════════════════════════════
class AnaUygulama(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("🎓 Öğrenci Yönetim Sistemi — PyQt5 + SQLite")
        self.setGeometry(100, 80, 1050, 680)
        self.setStyleSheet("""
            QMainWindow, QWidget { background:#0f172a; color:#e2e8f0; font-family:'Segoe UI'; font-size:13px; }
            QTableWidget { background:#1e293b; border:1px solid #334155; gridline-color:#334155; color:#e2e8f0; }
            QTableWidget::item:selected { background:#6366f1; }
            QHeaderView::section { background:#1e293b; color:#7c8cf8; padding:6px; border:1px solid #334155; font-weight:bold; }
            QLineEdit { background:#1e293b; border:1px solid #334155; border-radius:6px; padding:6px; color:#e2e8f0; }
            QLineEdit:focus { border:1px solid #6366f1; }
            QComboBox { background:#1e293b; border:1px solid #334155; border-radius:6px; padding:6px; color:#e2e8f0; }
            QComboBox QAbstractItemView { background:#1e293b; selection-background-color:#6366f1; }
        """)
        self.db = VeritabaniYoneticisi()
        self._arayuz()
        self.listele()

    def _arayuz(self):
        merkez = QWidget()
        self.setCentralWidget(merkez)
        ana = QHBoxLayout(merkez)
        ana.setContentsMargins(10, 10, 10, 10)
        ana.setSpacing(12)

        # ── Sol panel ─────────────────────────────
        sol = QVBoxLayout()
        sol.setSpacing(10)

        # Form
        self.form = OgrenciFormu()
        self.form.ekleBtn.clicked.connect(self.ekle)
        self.form.guncelleBtn.clicked.connect(self.guncelle)
        self.form.silBtn.clicked.connect(self.sil)
        self.form.temizleBtn.clicked.connect(self._formTemizle)
        sol.addWidget(self.form)

        # İstatistik kartı
        self.istatBox = QGroupBox("📊 İstatistik")
        self.istatBox.setStyleSheet("QGroupBox{font-weight:bold;color:#22d3ee;border:1px solid #334155;border-radius:8px;margin-top:10px;padding-top:8px;}")
        istat_layout = QGridLayout(self.istatBox)
        self.istatEtiketler = {}
        for i, (key, etiket) in enumerate([("toplam","Toplam"),("ort_gpa","Ort. GPA"),("max_gpa","En Yüksek"),("min_gpa","En Düşük")]):
            lbl = QLabel(etiket + ":")
            lbl.setStyleSheet("color:#64748b;")
            val = QLabel("—")
            val.setStyleSheet("font-weight:bold; color:#22d3ee; font-size:15px;")
            istat_layout.addWidget(lbl, i//2, (i%2)*2)
            istat_layout.addWidget(val, i//2, (i%2)*2+1)
            self.istatEtiketler[key] = val
        sol.addWidget(self.istatBox)
        sol.addStretch()

        # ── Sağ panel ─────────────────────────────
        sag = QVBoxLayout()
        sag.setSpacing(8)

        # Arama & filtre
        filtre_layout = QHBoxLayout()
        self.aramaInput = QLineEdit()
        self.aramaInput.setPlaceholderText("🔍  Ad, Soyad veya Numara ara...")
        self.aramaInput.textChanged.connect(self.listele)
        filtre_layout.addWidget(self.aramaInput)

        self.bolumFiltre = QComboBox()
        self.bolumFiltre.addItems(["Tümü"] + OgrenciFormu.BOLUMLER)
        self.bolumFiltre.currentIndexChanged.connect(self.listele)
        filtre_layout.addWidget(self.bolumFiltre)

        self.csvBtn = QPushButton("📥 CSV")
        self.csvBtn.setStyleSheet("background:#059669;color:white;padding:7px 14px;border-radius:6px;font-weight:bold;")
        self.csvBtn.clicked.connect(self.csvExport)
        filtre_layout.addWidget(self.csvBtn)
        sag.addLayout(filtre_layout)

        # Tablo
        self.tablo = QTableWidget()
        self.tablo.setColumnCount(7)
        self.tablo.setHorizontalHeaderLabels(["ID","Ad","Soyad","Numara","Bölüm","GPA","Şehir"])
        self.tablo.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tablo.setSelectionBehavior(QTableWidget.SelectRows)
        self.tablo.setAlternatingRowColors(True)
        self.tablo.horizontalHeader().setStretchLastSection(True)
        self.tablo.verticalHeader().setVisible(False)
        for i, w in enumerate([40, 85, 95, 75, 150, 60, 90]):
            self.tablo.setColumnWidth(i, w)
        self.tablo.clicked.connect(self._satirSec)
        sag.addWidget(self.tablo)

        self.sonucLabel = QLabel()
        self.sonucLabel.setStyleSheet("color:#64748b; padding:3px;")
        sag.addWidget(self.sonucLabel)

        ana.addLayout(sol, 38)
        ana.addLayout(sag, 62)

    # ── CRUD İşlemleri ────────────────────────────

    def ekle(self):
        veri, hata = self.form.dogrula()
        if hata:
            QMessageBox.warning(self, "Doğrulama Hatası", hata)
            return
        try:
            self.db.ekle(veri)
            self.form.temizle()
            self.listele()
            self.statusBar().showMessage("✅ Öğrenci eklendi.", 3000)
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Hata", "Bu numara zaten kayıtlı!")

    def guncelle(self):
        if not self.form.aktifId:
            return
        veri, hata = self.form.dogrula()
        if hata:
            QMessageBox.warning(self, "Doğrulama Hatası", hata)
            return
        try:
            self.db.guncelle(self.form.aktifId, veri)
            self.form.temizle()
            self.listele()
            self.statusBar().showMessage("✅ Kayıt güncellendi.", 3000)
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Hata", "Bu numara başka kayıtta kullanılıyor!")

    def sil(self):
        if not self.form.aktifId:
            return
        cevap = QMessageBox.question(self, "Silme Onayı",
            f"Bu öğrenciyi silmek istediğinizden emin misiniz?",
            QMessageBox.Yes | QMessageBox.No)
        if cevap == QMessageBox.Yes:
            self.db.sil(self.form.aktifId)
            self.form.temizle()
            self.listele()
            self.statusBar().showMessage("🗑️ Kayıt silindi.", 3000)

    def listele(self):
        satirlar = self.db.tumunuGetir(
            arama=self.aramaInput.text().strip(),
            bolum=self.bolumFiltre.currentText()
        )
        self.tablo.setRowCount(len(satirlar))
        for ri, satir in enumerate(satirlar):
            for ci, deger in enumerate(satir):
                if ci == 5:   # GPA renklendirme
                    item = QTableWidgetItem(f"{deger:.2f}")
                    r = "#22c55e" if deger >= 3.5 else ("#f59e0b" if deger >= 2.5 else "#ef4444")
                    item.setForeground(QColor(r))
                else:
                    item = QTableWidgetItem(str(deger) if deger else "")
                item.setTextAlignment(Qt.AlignCenter)
                self.tablo.setItem(ri, ci, item)
        self.sonucLabel.setText(f"  {len(satirlar)} kayıt")
        self._istatGuncelle()

    def _satirSec(self, index):
        satir = self.tablo.currentRow()
        id_item = self.tablo.item(satir, 0)
        if id_item:
            kayit = self.db.tekGetir(int(id_item.text()))
            if kayit:
                self.form.yukle(kayit)

    def _formTemizle(self):
        self.form.temizle()
        self.statusBar().showMessage("Form temizlendi.", 2000)

    def _istatGuncelle(self):
        ist = self.db.istatistik()
        if ist:
            self.istatEtiketler["toplam"].setText(str(ist["toplam"]))
            self.istatEtiketler["ort_gpa"].setText(str(ist["ort_gpa"] or "—"))
            self.istatEtiketler["max_gpa"].setText(str(ist["max_gpa"] or "—"))
            self.istatEtiketler["min_gpa"].setText(str(ist["min_gpa"] or "—"))

    def csvExport(self):
        yol, _ = QFileDialog.getSaveFileName(self, "CSV Kaydet", "ogrenciler.csv", "CSV (*.csv)")
        if not yol:
            return
        try:
            cur = sqlite3.connect(DB_DOSYA).cursor()
            cur.execute("SELECT id,ad,soyad,numara,bolum,gpa,sehir,email FROM ogrenciler ORDER BY ad")
            satirlar = cur.fetchall()
            with open(yol, "w", newline="", encoding="utf-8-sig") as f:
                w = csv.writer(f)
                w.writerow(["ID","Ad","Soyad","Numara","Bolum","GPA","Sehir","Email"])
                w.writerows(satirlar)
            QMessageBox.information(self, "Başarılı", f"✅ {len(satirlar)} kayıt dışa aktarıldı!")
            self.statusBar().showMessage(f"CSV: {yol}", 4000)
        except Exception as e:
            QMessageBox.critical(self, "Hata", str(e))

    def closeEvent(self, event):
        if os.path.exists(DB_DOSYA):
            os.remove(DB_DOSYA)
        event.accept()


app = QApplication(sys.argv)
pencere = AnaUygulama()
pencere.show()
sys.exit(app.exec_())
