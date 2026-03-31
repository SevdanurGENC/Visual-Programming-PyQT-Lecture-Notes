"""
╔══════════════════════════════════════════════════════════════════════════╗
║   KÜTÜPHANE TAKİP SİSTEMİ                                               ║
║   PyQt5 + SQLite Mini Otomasyon Uygulaması                              ║
║   Görsel Programlama Dersi — Dr. Öğr. Üyesi Sevdanur GENÇ              ║
╠══════════════════════════════════════════════════════════════════════════╣
║  Pencereler:                                                             ║
║   1. Ana Pencere    — Dashboard & istatistikler                          ║
║   2. Kitap Yönetimi — Kitap ekleme / listeleme / silme                  ║
║   3. Üye Yönetimi   — Üye ekleme / güncelleme / arama                  ║
║   4. Ödünç İşlemi   — Kitap ödünç verme / iade alma                    ║
║   5. Raporlar       — İstatistikler & CSV dışa aktarma                  ║
╚══════════════════════════════════════════════════════════════════════════╝
"""

import sys, sqlite3, csv, os
from datetime import datetime, date, timedelta
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QDialog,
    QVBoxLayout, QHBoxLayout, QGridLayout, QFormLayout,
    QLabel, QLineEdit, QPushButton, QComboBox,
    QTableWidget, QTableWidgetItem, QTextEdit,
    QGroupBox, QTabWidget, QMessageBox, QFileDialog,
    QDateEdit, QSpinBox, QFrame, QScrollArea
)
from PyQt5.QtCore import Qt, QDate, QTimer
from PyQt5.QtGui import QColor, QFont, QIcon

# ── Renk sabitleri ────────────────────────────────────────
KOYU   = "#0F172A"
PANEL  = "#1E293B"
KART   = "#1E3A5F"
SINIR  = "#334155"
METIN  = "#E2E8F0"
SOLUK  = "#64748B"
MAVI   = "#3B82F6"
YESIL  = "#22C55E"
SARI   = "#F59E0B"
KIRMIZI= "#EF4444"
MOR    = "#8B5CF6"
CAMASI = "#06B6D4"

STIL = f"""
QMainWindow, QDialog, QWidget {{
    background-color: {KOYU};
    color: {METIN};
    font-family: 'Segoe UI';
    font-size: 13px;
}}
QGroupBox {{
    border: 1px solid {SINIR};
    border-radius: 8px;
    margin-top: 14px;
    padding-top: 8px;
    font-weight: bold;
    color: {MAVI};
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 8px;
}}
QLineEdit, QComboBox, QSpinBox, QDateEdit {{
    background: {PANEL};
    border: 1px solid {SINIR};
    border-radius: 6px;
    padding: 7px 10px;
    color: {METIN};
}}
QLineEdit:focus, QComboBox:focus {{
    border: 1px solid {MAVI};
}}
QComboBox QAbstractItemView {{
    background: {PANEL};
    selection-background-color: {MAVI};
    color: {METIN};
}}
QTableWidget {{
    background: {PANEL};
    border: 1px solid {SINIR};
    gridline-color: {SINIR};
    color: {METIN};
    border-radius: 6px;
}}
QTableWidget::item:selected {{ background: {MAVI}; }}
QHeaderView::section {{
    background: {KART};
    color: {CAMASI};
    padding: 7px;
    border: 1px solid {SINIR};
    font-weight: bold;
}}
QTableWidget::item {{ padding: 4px; }}
QPushButton {{
    border-radius: 7px;
    padding: 9px 18px;
    font-weight: bold;
    color: white;
    border: none;
}}
QPushButton:hover {{ opacity: 0.85; }}
QScrollBar:vertical {{ background: {PANEL}; width: 8px; border-radius: 4px; }}
QScrollBar::handle:vertical {{ background: {SINIR}; border-radius: 4px; }}
"""

def btn(metin, renk, hover=None):
    h = hover or renk
    b = QPushButton(metin)
    b.setStyleSheet(f"background:{renk};color:white;border-radius:7px;padding:9px 18px;font-weight:bold;")
    return b


# ══════════════════════════════════════════════════════════
#  VERİTABANI YÖNETİCİSİ
# ══════════════════════════════════════════════════════════
class DB:
    DOSYA = "kutuphane.db"

    def __init__(self):
        self._kur()

    def _baglan(self):
        db = sqlite3.connect(self.DOSYA)
        db.row_factory = sqlite3.Row
        db.execute("PRAGMA foreign_keys = ON")
        return db

    def _kur(self):
        with self._baglan() as db:
            db.executescript("""
                CREATE TABLE IF NOT EXISTS kitaplar (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    isbn        TEXT UNIQUE NOT NULL,
                    baslik      TEXT NOT NULL,
                    yazar       TEXT NOT NULL,
                    kategori    TEXT DEFAULT 'Genel',
                    yil         INTEGER,
                    adet        INTEGER DEFAULT 1,
                    musait_adet INTEGER DEFAULT 1,
                    ekleme_tarihi TEXT DEFAULT CURRENT_DATE
                );
                CREATE TABLE IF NOT EXISTS uyeler (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    ad          TEXT NOT NULL,
                    soyad       TEXT NOT NULL,
                    email       TEXT UNIQUE NOT NULL,
                    telefon     TEXT,
                    uyelik_turu TEXT DEFAULT 'Standart',
                    aktif       INTEGER DEFAULT 1,
                    kayit_tarihi TEXT DEFAULT CURRENT_DATE
                );
                CREATE TABLE IF NOT EXISTS oduncler (
                    id            INTEGER PRIMARY KEY AUTOINCREMENT,
                    kitap_id      INTEGER NOT NULL,
                    uye_id        INTEGER NOT NULL,
                    odunc_tarihi  TEXT NOT NULL,
                    iade_tarihi   TEXT,
                    geri_donus    TEXT,
                    durum         TEXT DEFAULT 'Ödünçte',
                    FOREIGN KEY (kitap_id) REFERENCES kitaplar(id),
                    FOREIGN KEY (uye_id)   REFERENCES uyeler(id)
                );
            """)
            # Demo veri
            if db.execute("SELECT COUNT(*) FROM kitaplar").fetchone()[0] == 0:
                db.executemany("INSERT INTO kitaplar (isbn,baslik,yazar,kategori,yil,adet,musait_adet) VALUES (?,?,?,?,?,?,?)", [
                    ("978-975-001","Python ile Programlama","Guido van Rossum","Bilişim",2022,3,3),
                    ("978-975-002","Veri Yapıları ve Algoritmalar","Thomas Cormen","Bilişim",2021,2,2),
                    ("978-975-003","Yapay Zeka Temelleri","Stuart Russell","Bilişim",2023,2,2),
                    ("978-975-004","Türk Edebiyatı Tarihi","Ahmet Kabaklı","Edebiyat",2019,1,1),
                    ("978-975-005","Matematik Analiz","Walter Rudin","Matematik",2020,2,2),
                    ("978-975-006","Fizik Bilimine Giriş","Richard Feynman","Fen",2018,1,1),
                    ("978-975-007","Web Geliştirme Temelleri","Jon Duckett","Bilişim",2022,2,2),
                    ("978-975-008","Makine Öğrenmesi","Andrew Ng","Bilişim",2023,1,1),
                ])
                db.executemany("INSERT INTO uyeler (ad,soyad,email,telefon,uyelik_turu) VALUES (?,?,?,?,?)", [
                    ("Ahmet","Yılmaz","ahmet@mail.com","0532-111-1111","Öğrenci"),
                    ("Zeynep","Kaya","zeynep@mail.com","0533-222-2222","Öğrenci"),
                    ("Mehmet","Demir","mehmet@mail.com","0534-333-3333","Akademisyen"),
                    ("Elif","Çelik","elif@mail.com","0535-444-4444","Öğrenci"),
                    ("Prof. Dr. Can","Arslan","can.prof@mail.com","0536-555-5555","Akademisyen"),
                ])

    # Kitap işlemleri
    def kitap_ekle(self, v):
        with self._baglan() as db:
            db.execute("INSERT INTO kitaplar (isbn,baslik,yazar,kategori,yil,adet,musait_adet) VALUES (?,?,?,?,?,?,?)", v)
    def kitaplari_getir(self, arama=""):
        with self._baglan() as db:
            if arama:
                return db.execute("SELECT * FROM kitaplar WHERE baslik LIKE ? OR yazar LIKE ? OR isbn LIKE ? ORDER BY baslik",
                                  [f"%{arama}%"]*3).fetchall()
            return db.execute("SELECT * FROM kitaplar ORDER BY baslik").fetchall()
    def kitap_sil(self, id_):
        with self._baglan() as db:
            db.execute("DELETE FROM kitaplar WHERE id=?", (id_,))

    # Üye işlemleri
    def uye_ekle(self, v):
        with self._baglan() as db:
            db.execute("INSERT INTO uyeler (ad,soyad,email,telefon,uyelik_turu) VALUES (?,?,?,?,?)", v)
    def uyeleri_getir(self, arama=""):
        with self._baglan() as db:
            if arama:
                return db.execute("SELECT * FROM uyeler WHERE ad LIKE ? OR soyad LIKE ? OR email LIKE ? ORDER BY ad",
                                  [f"%{arama}%"]*3).fetchall()
            return db.execute("SELECT * FROM uyeler ORDER BY ad").fetchall()
    def uye_guncelle(self, id_, v):
        with self._baglan() as db:
            db.execute("UPDATE uyeler SET ad=?,soyad=?,email=?,telefon=?,uyelik_turu=?,aktif=? WHERE id=?", (*v, id_))

    # Ödünç işlemleri
    def odunc_ver(self, kitap_id, uye_id, iade_tarihi):
        with self._baglan() as db:
            db.execute("INSERT INTO oduncler (kitap_id,uye_id,odunc_tarihi,iade_tarihi,durum) VALUES (?,?,?,?,'Ödünçte')",
                       (kitap_id, uye_id, str(date.today()), iade_tarihi))
            db.execute("UPDATE kitaplar SET musait_adet = musait_adet - 1 WHERE id=?", (kitap_id,))
    def iade_al(self, odunc_id, kitap_id):
        with self._baglan() as db:
            db.execute("UPDATE oduncler SET durum='İade Edildi', geri_donus=? WHERE id=?",
                       (str(date.today()), odunc_id))
            db.execute("UPDATE kitaplar SET musait_adet = musait_adet + 1 WHERE id=?", (kitap_id,))
    def aktif_oduncleri_getir(self):
        with self._baglan() as db:
            return db.execute("""
                SELECT o.id, k.baslik, u.ad||' '||u.soyad as uye,
                       o.odunc_tarihi, o.iade_tarihi, o.durum,
                       o.kitap_id,
                       CASE WHEN o.iade_tarihi < date('now') AND o.durum='Ödünçte'
                            THEN 'Gecikmiş' ELSE o.durum END as gercek_durum
                FROM oduncler o
                JOIN kitaplar k ON o.kitap_id = k.id
                JOIN uyeler   u ON o.uye_id   = u.id
                WHERE o.durum = 'Ödünçte'
                ORDER BY o.iade_tarihi
            """).fetchall()
    def musait_kitaplari_getir(self):
        with self._baglan() as db:
            return db.execute("SELECT id, isbn, baslik, yazar FROM kitaplar WHERE musait_adet > 0 ORDER BY baslik").fetchall()
    def aktif_uyeleri_getir(self):
        with self._baglan() as db:
            return db.execute("SELECT id, ad||' '||soyad as tam_ad, uyelik_turu FROM uyeler WHERE aktif=1 ORDER BY ad").fetchall()

    # İstatistikler
    def istatistik(self):
        with self._baglan() as db:
            return {
                "toplam_kitap":   db.execute("SELECT COUNT(*) FROM kitaplar").fetchone()[0],
                "toplam_uye":     db.execute("SELECT COUNT(*) FROM uyeler WHERE aktif=1").fetchone()[0],
                "aktif_odunc":    db.execute("SELECT COUNT(*) FROM oduncler WHERE durum='Ödünçte'").fetchone()[0],
                "gec_kalan":      db.execute("SELECT COUNT(*) FROM oduncler WHERE durum='Ödünçte' AND iade_tarihi < date('now')").fetchone()[0],
                "bugun_iade":     db.execute("SELECT COUNT(*) FROM oduncler WHERE iade_tarihi = date('now') AND durum='Ödünçte'").fetchone()[0],
                "toplam_islem":   db.execute("SELECT COUNT(*) FROM oduncler").fetchone()[0],
                "kategori_en_cok":db.execute("SELECT kategori, COUNT(*) as n FROM kitaplar GROUP BY kategori ORDER BY n DESC LIMIT 1").fetchone(),
                "musait_kitap":   db.execute("SELECT SUM(musait_adet) FROM kitaplar").fetchone()[0] or 0,
            }
    def kategori_dagilim(self):
        with self._baglan() as db:
            return db.execute("SELECT kategori, COUNT(*) FROM kitaplar GROUP BY kategori ORDER BY COUNT(*) DESC").fetchall()
    def populer_kitaplar(self):
        with self._baglan() as db:
            return db.execute("""
                SELECT k.baslik, k.yazar, COUNT(o.id) as odunc_sayisi
                FROM kitaplar k LEFT JOIN oduncler o ON k.id = o.kitap_id
                GROUP BY k.id ORDER BY odunc_sayisi DESC LIMIT 5
            """).fetchall()
    def tum_odunc_gecmisi(self):
        with self._baglan() as db:
            return db.execute("""
                SELECT o.id, k.baslik, u.ad||' '||u.soyad, o.odunc_tarihi, o.iade_tarihi, o.geri_donus, o.durum
                FROM oduncler o JOIN kitaplar k ON o.kitap_id=k.id JOIN uyeler u ON o.uye_id=u.id
                ORDER BY o.id DESC
            """).fetchall()


# ══════════════════════════════════════════════════════════
#  PENCERE 2 — KİTAP YÖNETİMİ
# ══════════════════════════════════════════════════════════
class KitapPencere(QDialog):
    def __init__(self, db: DB, parent=None):
        super().__init__(parent)
        self.db = db
        self.setWindowTitle("📚 Kitap Yönetimi")
        self.setGeometry(160, 120, 860, 580)
        self.setStyleSheet(STIL)
        self._kur()
        self.listele()

    def _kur(self):
        ana = QHBoxLayout(self)
        ana.setContentsMargins(12, 12, 12, 12)
        ana.setSpacing(12)

        # Sol — form
        form_grup = QGroupBox("➕ Yeni Kitap Ekle")
        fg = QFormLayout(form_grup)
        fg.setSpacing(10)
        fg.setContentsMargins(14, 18, 14, 14)
        self.inp = {}
        for lbl, key, ph in [
            ("ISBN:",     "isbn",     "978-975-xxx"),
            ("Başlık:",   "baslik",   "Kitap adı"),
            ("Yazar:",    "yazar",    "Yazar adı"),
            ("Yıl:",      "yil",      "2024"),
            ("Adet:",     "adet",     "1"),
        ]:
            w = QLineEdit()
            w.setPlaceholderText(ph)
            self.inp[key] = w
            fg.addRow(lbl, w)
        self.katCombo = QComboBox()
        self.katCombo.addItems(["Bilişim","Matematik","Fen","Edebiyat","Tarih","Sosyal Bilim","Genel"])
        fg.addRow("Kategori:", self.katCombo)

        ekleBtn = btn("➕  Ekle", YESIL)
        ekleBtn.clicked.connect(self._ekle)
        temBtn  = btn("🔄  Temizle", SOLUK)
        temBtn.clicked.connect(self._temizle)
        brow = QHBoxLayout()
        brow.addWidget(ekleBtn); brow.addWidget(temBtn)
        fg.addRow(brow)

        ana.addWidget(form_grup, 35)

        # Sağ — liste
        sag = QVBoxLayout()
        sag.setSpacing(8)

        aRow = QHBoxLayout()
        self.aramaInput = QLineEdit()
        self.aramaInput.setPlaceholderText("🔍 Başlık, yazar veya ISBN ara...")
        self.aramaInput.textChanged.connect(self.listele)
        silBtn = btn("🗑️  Seçili Sil", KIRMIZI)
        silBtn.clicked.connect(self._sil)
        aRow.addWidget(self.aramaInput)
        aRow.addWidget(silBtn)
        sag.addLayout(aRow)

        self.tablo = QTableWidget()
        self.tablo.setColumnCount(8)
        self.tablo.setHorizontalHeaderLabels(["ID","ISBN","Başlık","Yazar","Kategori","Yıl","Toplam","Müsait"])
        self.tablo.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tablo.setSelectionBehavior(QTableWidget.SelectRows)
        self.tablo.setAlternatingRowColors(True)
        self.tablo.horizontalHeader().setStretchLastSection(True)
        self.tablo.verticalHeader().setVisible(False)
        for i, w in enumerate([35,110,200,140,90,50,60,60]):
            self.tablo.setColumnWidth(i, w)
        sag.addWidget(self.tablo)

        self.sayacLabel = QLabel()
        self.sayacLabel.setStyleSheet(f"color:{SOLUK}; padding:3px;")
        sag.addWidget(self.sayacLabel)
        ana.addLayout(sag, 65)

    def listele(self):
        satirlar = self.db.kitaplari_getir(self.aramaInput.text().strip())
        self.tablo.setRowCount(len(satirlar))
        for ri, r in enumerate(satirlar):
            degerler = [r["id"], r["isbn"], r["baslik"], r["yazar"],
                        r["kategori"], r["yil"] or "-", r["adet"], r["musait_adet"]]
            for ci, d in enumerate(degerler):
                item = QTableWidgetItem(str(d))
                item.setTextAlignment(Qt.AlignCenter)
                if ci == 7:  # Müsait
                    item.setForeground(QColor(YESIL if int(d) > 0 else KIRMIZI))
                self.tablo.setItem(ri, ci, item)
        self.sayacLabel.setText(f"  {len(satirlar)} kitap")

    def _ekle(self):
        isbn   = self.inp["isbn"].text().strip()
        baslik = self.inp["baslik"].text().strip()
        yazar  = self.inp["yazar"].text().strip()
        if not isbn or not baslik or not yazar:
            QMessageBox.warning(self, "Eksik", "ISBN, başlık ve yazar zorunludur!")
            return
        try:
            yil  = int(self.inp["yil"].text()) if self.inp["yil"].text() else None
            adet = int(self.inp["adet"].text() or "1")
        except ValueError:
            QMessageBox.warning(self, "Hata", "Yıl ve adet sayı olmalıdır!"); return
        try:
            self.db.kitap_ekle((isbn, baslik, yazar, self.katCombo.currentText(), yil, adet, adet))
            self._temizle()
            self.listele()
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Hata", "Bu ISBN zaten kayıtlı!")

    def _temizle(self):
        for w in self.inp.values(): w.clear()

    def _sil(self):
        satir = self.tablo.currentRow()
        if satir < 0:
            QMessageBox.information(self, "Bilgi", "Silmek için bir kitap seçin."); return
        baslik = self.tablo.item(satir, 2).text()
        id_    = int(self.tablo.item(satir, 0).text())
        if QMessageBox.question(self, "Onay", f"'{baslik}' silinsin mi?",
                                QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
            self.db.kitap_sil(id_)
            self.listele()


# ══════════════════════════════════════════════════════════
#  PENCERE 3 — ÜYE YÖNETİMİ
# ══════════════════════════════════════════════════════════
class UyePencere(QDialog):
    def __init__(self, db: DB, parent=None):
        super().__init__(parent)
        self.db = db
        self.setWindowTitle("👤 Üye Yönetimi")
        self.setGeometry(180, 130, 860, 560)
        self.setStyleSheet(STIL)
        self.aktifId = None
        self._kur()
        self.listele()

    def _kur(self):
        ana = QHBoxLayout(self)
        ana.setContentsMargins(12, 12, 12, 12)
        ana.setSpacing(12)

        # Sol form
        form_grup = QGroupBox("👤 Üye Bilgileri")
        fg = QFormLayout(form_grup)
        fg.setSpacing(10)
        fg.setContentsMargins(14, 18, 14, 14)
        self.inp = {}
        for lbl, key, ph in [
            ("Ad:",      "ad",     "Ad"),
            ("Soyad:",   "soyad",  "Soyad"),
            ("E-posta:", "email",  "ornek@mail.com"),
            ("Telefon:", "tel",    "0532-xxx-xxxx"),
        ]:
            w = QLineEdit()
            w.setPlaceholderText(ph)
            self.inp[key] = w
            fg.addRow(lbl, w)
        self.turCombo = QComboBox()
        self.turCombo.addItems(["Öğrenci", "Akademisyen", "Personel", "Misafir"])
        fg.addRow("Tür:", self.turCombo)
        self.aktifCombo = QComboBox()
        self.aktifCombo.addItems(["Aktif", "Pasif"])
        fg.addRow("Durum:", self.aktifCombo)

        btnRow = QHBoxLayout()
        ekleBtn = btn("➕  Ekle", YESIL)
        guncBtn = btn("✏️  Güncelle", SARI)
        temBtn  = btn("🔄  Temizle", SOLUK)
        ekleBtn.clicked.connect(self._ekle)
        guncBtn.clicked.connect(self._guncelle)
        temBtn.clicked.connect(self._temizle)
        for b in [ekleBtn, guncBtn, temBtn]: btnRow.addWidget(b)
        fg.addRow(btnRow)
        ana.addWidget(form_grup, 38)

        # Sağ liste
        sag = QVBoxLayout(); sag.setSpacing(8)
        self.aramaInput = QLineEdit()
        self.aramaInput.setPlaceholderText("🔍 Ad, soyad veya e-posta ara...")
        self.aramaInput.textChanged.connect(self.listele)
        sag.addWidget(self.aramaInput)

        self.tablo = QTableWidget()
        self.tablo.setColumnCount(7)
        self.tablo.setHorizontalHeaderLabels(["ID","Ad","Soyad","E-posta","Telefon","Tür","Durum"])
        self.tablo.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tablo.setSelectionBehavior(QTableWidget.SelectRows)
        self.tablo.setAlternatingRowColors(True)
        self.tablo.horizontalHeader().setStretchLastSection(True)
        self.tablo.verticalHeader().setVisible(False)
        for i, w in enumerate([35,90,100,160,120,100,70]):
            self.tablo.setColumnWidth(i, w)
        self.tablo.clicked.connect(self._satirSec)
        sag.addWidget(self.tablo)
        self.sayacLabel = QLabel()
        self.sayacLabel.setStyleSheet(f"color:{SOLUK}; padding:3px;")
        sag.addWidget(self.sayacLabel)
        ana.addLayout(sag, 62)

    def listele(self):
        satirlar = self.db.uyeleri_getir(self.aramaInput.text().strip())
        self.tablo.setRowCount(len(satirlar))
        for ri, r in enumerate(satirlar):
            degerler = [r["id"], r["ad"], r["soyad"], r["email"],
                        r["telefon"] or "-", r["uyelik_turu"], "Aktif" if r["aktif"] else "Pasif"]
            for ci, d in enumerate(degerler):
                item = QTableWidgetItem(str(d))
                item.setTextAlignment(Qt.AlignCenter)
                if ci == 6:
                    item.setForeground(QColor(YESIL if d == "Aktif" else KIRMIZI))
                self.tablo.setItem(ri, ci, item)
        self.sayacLabel.setText(f"  {len(satirlar)} üye")

    def _satirSec(self):
        satir = self.tablo.currentRow()
        if satir < 0: return
        self.aktifId = int(self.tablo.item(satir, 0).text())
        self.inp["ad"].setText(self.tablo.item(satir, 1).text())
        self.inp["soyad"].setText(self.tablo.item(satir, 2).text())
        self.inp["email"].setText(self.tablo.item(satir, 3).text())
        self.inp["tel"].setText(self.tablo.item(satir, 4).text())
        tur = self.tablo.item(satir, 5).text()
        idx = self.turCombo.findText(tur)
        if idx >= 0: self.turCombo.setCurrentIndex(idx)
        self.aktifCombo.setCurrentIndex(0 if self.tablo.item(satir, 6).text() == "Aktif" else 1)

    def _ekle(self):
        ad = self.inp["ad"].text().strip()
        soyad = self.inp["soyad"].text().strip()
        email = self.inp["email"].text().strip()
        if not ad or not soyad or not email:
            QMessageBox.warning(self, "Eksik", "Ad, soyad ve e-posta zorunludur!"); return
        try:
            self.db.uye_ekle((ad, soyad, email, self.inp["tel"].text().strip(), self.turCombo.currentText()))
            self._temizle(); self.listele()
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Hata", "Bu e-posta zaten kayıtlı!")

    def _guncelle(self):
        if not self.aktifId:
            QMessageBox.information(self, "Bilgi", "Güncellemek için tablodan bir üye seçin."); return
        ad = self.inp["ad"].text().strip()
        soyad = self.inp["soyad"].text().strip()
        email = self.inp["email"].text().strip()
        if not ad or not soyad or not email:
            QMessageBox.warning(self, "Eksik", "Ad, soyad ve e-posta zorunludur!"); return
        aktif = 1 if self.aktifCombo.currentIndex() == 0 else 0
        self.db.uye_guncelle(self.aktifId, (ad, soyad, email, self.inp["tel"].text().strip(), self.turCombo.currentText(), aktif))
        self._temizle(); self.listele()

    def _temizle(self):
        for w in self.inp.values(): w.clear()
        self.aktifId = None
        self.turCombo.setCurrentIndex(0)
        self.aktifCombo.setCurrentIndex(0)


# ══════════════════════════════════════════════════════════
#  PENCERE 4 — ÖDÜNÇ İŞLEMİ
# ══════════════════════════════════════════════════════════
class OduncPencere(QDialog):
    def __init__(self, db: DB, parent=None):
        super().__init__(parent)
        self.db = db
        self.setWindowTitle("🔄 Ödünç İşlemleri")
        self.setGeometry(200, 140, 900, 560)
        self.setStyleSheet(STIL)
        self._kur()
        self.listele()

    def _kur(self):
        ana = QVBoxLayout(self)
        ana.setContentsMargins(12, 12, 12, 12)
        ana.setSpacing(10)

        # Üst — ödünç verme formu
        form_grup = QGroupBox("📤 Kitap Ödünç Ver")
        row = QHBoxLayout(form_grup)
        row.setContentsMargins(14, 18, 14, 14)
        row.setSpacing(12)

        row.addWidget(QLabel("Kitap:"))
        self.kitapCombo = QComboBox()
        self.kitapCombo.setMinimumWidth(280)
        row.addWidget(self.kitapCombo)

        row.addWidget(QLabel("Üye:"))
        self.uyeCombo = QComboBox()
        self.uyeCombo.setMinimumWidth(200)
        row.addWidget(self.uyeCombo)

        row.addWidget(QLabel("İade Tarihi:"))
        self.iadeDateEdit = QDateEdit(QDate.currentDate().addDays(14))
        self.iadeDateEdit.setCalendarPopup(True)
        self.iadeDateEdit.setDisplayFormat("dd.MM.yyyy")
        row.addWidget(self.iadeDateEdit)

        oduncBtn = btn("📤  Ödünç Ver", MAVI)
        oduncBtn.clicked.connect(self._oduncVer)
        yenileBtn = btn("🔄", SOLUK)
        yenileBtn.setFixedWidth(44)
        yenileBtn.clicked.connect(self._comboYenile)
        row.addWidget(oduncBtn)
        row.addWidget(yenileBtn)
        ana.addWidget(form_grup)

        # Alt — aktif ödünç listesi
        list_grup = QGroupBox("📋 Aktif Ödünçler")
        list_layout = QVBoxLayout(list_grup)
        list_layout.setContentsMargins(10, 16, 10, 10)

        self.tablo = QTableWidget()
        self.tablo.setColumnCount(7)
        self.tablo.setHorizontalHeaderLabels(["Ödünç ID","Kitap","Üye","Ödünç Tarihi","Son İade","Durum","İşlem"])
        self.tablo.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tablo.setSelectionBehavior(QTableWidget.SelectRows)
        self.tablo.setAlternatingRowColors(True)
        self.tablo.verticalHeader().setVisible(False)
        self.tablo.horizontalHeader().setStretchLastSection(False)
        for i, w in enumerate([70,220,150,100,100,90,80]):
            self.tablo.setColumnWidth(i, w)
        list_layout.addWidget(self.tablo)

        self.sayacLabel = QLabel()
        self.sayacLabel.setStyleSheet(f"color:{SOLUK}; padding:3px;")
        list_layout.addWidget(self.sayacLabel)
        ana.addWidget(list_grup)

        self._comboYenile()

    def _comboYenile(self):
        self.kitapCombo.clear()
        for k in self.db.musait_kitaplari_getir():
            self.kitapCombo.addItem(f"{k['baslik']} — {k['yazar']}", k["id"])
        self.uyeCombo.clear()
        for u in self.db.aktif_uyeleri_getir():
            self.uyeCombo.addItem(f"{u['tam_ad']} ({u['uyelik_turu']})", u["id"])

    def listele(self):
        satirlar = self.db.aktif_oduncleri_getir()
        self.tablo.setRowCount(len(satirlar))
        for ri, r in enumerate(satirlar):
            degerler = [r["id"], r["baslik"], r["uye"],
                        r["odunc_tarihi"], r["iade_tarihi"], r["gercek_durum"]]
            for ci, d in enumerate(degerler):
                item = QTableWidgetItem(str(d))
                item.setTextAlignment(Qt.AlignCenter)
                if ci == 5:
                    renk = KIRMIZI if d == "Gecikmiş" else SARI
                    item.setForeground(QColor(renk))
                    item.setFont(QFont("Segoe UI", 11, QFont.Bold))
                self.tablo.setItem(ri, ci, item)
            # İade butonu
            iadeBtn = btn("✅ İade", YESIL)
            iadeBtn.setFixedHeight(30)
            odunc_id = r["id"]
            kitap_id = r["kitap_id"]
            iadeBtn.clicked.connect(lambda _, oid=odunc_id, kid=kitap_id: self._iade(oid, kid))
            self.tablo.setCellWidget(ri, 6, iadeBtn)
            self.tablo.setRowHeight(ri, 36)
        geciken = sum(1 for r in satirlar if r["gercek_durum"] == "Gecikmiş")
        self.sayacLabel.setText(f"  {len(satirlar)} aktif ödünç  |  ⚠️ {geciken} gecikmiş")

    def _oduncVer(self):
        if self.kitapCombo.count() == 0:
            QMessageBox.warning(self, "Uyarı", "Müsait kitap yok!"); return
        if self.uyeCombo.count() == 0:
            QMessageBox.warning(self, "Uyarı", "Aktif üye yok!"); return
        kitap_id = self.kitapCombo.currentData()
        uye_id   = self.uyeCombo.currentData()
        iade     = self.iadeDateEdit.date().toString("yyyy-MM-dd")
        self.db.odunc_ver(kitap_id, uye_id, iade)
        self.listele()
        self._comboYenile()
        QMessageBox.information(self, "Başarılı", "✅ Kitap ödünç verildi!")

    def _iade(self, odunc_id, kitap_id):
        if QMessageBox.question(self, "İade Onayı", "Kitap iade alınsın mı?",
                                QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
            self.db.iade_al(odunc_id, kitap_id)
            self.listele()
            self._comboYenile()


# ══════════════════════════════════════════════════════════
#  PENCERE 5 — RAPORLAR
# ══════════════════════════════════════════════════════════
class RaporPencere(QDialog):
    def __init__(self, db: DB, parent=None):
        super().__init__(parent)
        self.db = db
        self.setWindowTitle("📊 Raporlar & İstatistikler")
        self.setGeometry(220, 150, 880, 560)
        self.setStyleSheet(STIL)
        self._kur()
        self._yenile()

    def _kur(self):
        ana = QVBoxLayout(self)
        ana.setContentsMargins(12, 12, 12, 12)
        ana.setSpacing(10)

        # Üst — mini stat kartları
        self.kartRow = QHBoxLayout()
        self.kartRow.setSpacing(10)
        self.kartWidgetler = {}
        for key, renk, ikon in [
            ("toplam_kitap", MAVI, "📚"), ("toplam_uye", YESIL, "👥"),
            ("aktif_odunc", SARI, "🔄"),  ("gec_kalan", KIRMIZI, "⚠️")
        ]:
            kart = QFrame()
            kart.setStyleSheet(f"background:{PANEL}; border:1px solid {SINIR}; border-radius:10px; padding:8px;")
            kv = QVBoxLayout(kart)
            ikon_lbl = QLabel(ikon)
            ikon_lbl.setStyleSheet("font-size:24px;")
            ikon_lbl.setAlignment(Qt.AlignCenter)
            val_lbl = QLabel("—")
            val_lbl.setStyleSheet(f"font-size:26px; font-weight:bold; color:{renk};")
            val_lbl.setAlignment(Qt.AlignCenter)
            kv.addWidget(ikon_lbl)
            kv.addWidget(val_lbl)
            self.kartWidgetler[key] = val_lbl
            self.kartRow.addWidget(kart)
        ana.addLayout(self.kartRow)

        # Sekmeli içerik
        sekmeler = QTabWidget()
        sekmeler.setStyleSheet(f"""
            QTabBar::tab {{ background:{PANEL}; color:{SOLUK}; padding:8px 16px; margin-right:2px; font-weight:bold; }}
            QTabBar::tab:selected {{ background:{MAVI}; color:white; }}
            QTabWidget::pane {{ border:1px solid {SINIR}; background:{PANEL}; }}
        """)

        # Sekme 1 — Kategori Dağılımı
        kat_w = QWidget()
        kat_v = QVBoxLayout(kat_w)
        kat_v.setContentsMargins(10, 10, 10, 10)
        self.katTablo = QTableWidget()
        self.katTablo.setColumnCount(2)
        self.katTablo.setHorizontalHeaderLabels(["Kategori", "Kitap Sayısı"])
        self.katTablo.setEditTriggers(QTableWidget.NoEditTriggers)
        self.katTablo.horizontalHeader().setStretchLastSection(True)
        self.katTablo.verticalHeader().setVisible(False)
        kat_v.addWidget(self.katTablo)
        sekmeler.addTab(kat_w, "📂 Kategoriler")

        # Sekme 2 — Popüler Kitaplar
        pop_w = QWidget()
        pop_v = QVBoxLayout(pop_w)
        pop_v.setContentsMargins(10, 10, 10, 10)
        self.popTablo = QTableWidget()
        self.popTablo.setColumnCount(3)
        self.popTablo.setHorizontalHeaderLabels(["Başlık", "Yazar", "Ödünç Sayısı"])
        self.popTablo.setEditTriggers(QTableWidget.NoEditTriggers)
        self.popTablo.horizontalHeader().setStretchLastSection(True)
        self.popTablo.verticalHeader().setVisible(False)
        pop_v.addWidget(self.popTablo)
        sekmeler.addTab(pop_w, "🏆 Popüler Kitaplar")

        # Sekme 3 — Tüm Geçmiş
        gec_w = QWidget()
        gec_v = QVBoxLayout(gec_w)
        gec_v.setContentsMargins(10, 10, 10, 10)
        self.gecTablo = QTableWidget()
        self.gecTablo.setColumnCount(7)
        self.gecTablo.setHorizontalHeaderLabels(["ID","Kitap","Üye","Ödünç","Son İade","Geri Dönüş","Durum"])
        self.gecTablo.setEditTriggers(QTableWidget.NoEditTriggers)
        self.gecTablo.setAlternatingRowColors(True)
        self.gecTablo.verticalHeader().setVisible(False)
        for i, w in enumerate([40,200,140,90,90,90,90]):
            self.gecTablo.setColumnWidth(i, w)
        self.gecTablo.horizontalHeader().setStretchLastSection(True)
        gec_v.addWidget(self.gecTablo)
        sekmeler.addTab(gec_w, "📜 Tüm İşlem Geçmişi")

        ana.addWidget(sekmeler)

        # Alt butonlar
        altRow = QHBoxLayout()
        yenileBtn = btn("🔄  Yenile", MAVI)
        csvBtn    = btn("📥  CSV Dışa Aktar", YESIL)
        yenileBtn.clicked.connect(self._yenile)
        csvBtn.clicked.connect(self._csvExport)
        altRow.addStretch()
        altRow.addWidget(yenileBtn)
        altRow.addWidget(csvBtn)
        ana.addLayout(altRow)

    def _yenile(self):
        ist = self.db.istatistik()
        for key, val in ist.items():
            if key in self.kartWidgetler and not isinstance(val, tuple):
                self.kartWidgetler[key].setText(str(val))

        # Kategori tablosu
        kat = self.db.kategori_dagilim()
        self.katTablo.setRowCount(len(kat))
        for ri, r in enumerate(kat):
            for ci, d in enumerate(r):
                item = QTableWidgetItem(str(d))
                item.setTextAlignment(Qt.AlignCenter)
                self.katTablo.setItem(ri, ci, item)

        # Popüler kitaplar
        pop = self.db.populer_kitaplar()
        self.popTablo.setRowCount(len(pop))
        for ri, r in enumerate(pop):
            for ci, d in enumerate(r):
                item = QTableWidgetItem(str(d))
                item.setTextAlignment(Qt.AlignCenter)
                if ci == 2:
                    item.setForeground(QColor(SARI))
                    item.setFont(QFont("Segoe UI", 12, QFont.Bold))
                self.popTablo.setItem(ri, ci, item)

        # Geçmiş
        gec = self.db.tum_odunc_gecmisi()
        self.gecTablo.setRowCount(len(gec))
        for ri, r in enumerate(gec):
            for ci, d in enumerate(r):
                item = QTableWidgetItem(str(d) if d else "—")
                item.setTextAlignment(Qt.AlignCenter)
                if ci == 6:
                    renk = YESIL if d == "İade Edildi" else SARI
                    item.setForeground(QColor(renk))
                self.gecTablo.setItem(ri, ci, item)

    def _csvExport(self):
        yol, _ = QFileDialog.getSaveFileName(self, "CSV Kaydet", "kutuphane_rapor.csv", "CSV (*.csv)")
        if not yol: return
        try:
            with self._baglan_csv() as data:
                with open(yol, "w", newline="", encoding="utf-8-sig") as f:
                    w = csv.writer(f)
                    w.writerow(["ID","Kitap","Üye","Ödünç Tarihi","Son İade","Geri Dönüş","Durum"])
                    w.writerows(data)
            QMessageBox.information(self, "Başarılı", f"✅ Rapor kaydedildi:\n{yol}")
        except Exception as e:
            QMessageBox.critical(self, "Hata", str(e))

    def _baglan_csv(self):
        class CM:
            def __enter__(s): return self.db.tum_odunc_gecmisi()
            def __exit__(s, *a): pass
        return CM()


# ══════════════════════════════════════════════════════════
#  PENCERE 1 — ANA PENCERE (DASHBOARD)
# ══════════════════════════════════════════════════════════
class AnaPencere(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = DB()
        self.setWindowTitle("📖 Kütüphane Takip Sistemi")
        self.setGeometry(100, 80, 900, 580)
        self.setStyleSheet(STIL)
        self._kur()
        self._istatGuncelle()

        # Her 30 saniyede güncelle
        self.timer = QTimer()
        self.timer.timeout.connect(self._istatGuncelle)
        self.timer.start(30000)

    def _kur(self):
        merkez = QWidget()
        self.setCentralWidget(merkez)
        ana = QVBoxLayout(merkez)
        ana.setContentsMargins(18, 15, 18, 15)
        ana.setSpacing(16)

        # Başlık
        baslik = QLabel("📖  Kütüphane Takip Sistemi")
        baslik.setStyleSheet(f"font-size:22px; font-weight:bold; color:{METIN};")
        baslik.setAlignment(Qt.AlignCenter)
        ana.addWidget(baslik)

        # İstatistik kartları
        kart_row = QHBoxLayout()
        kart_row.setSpacing(12)
        self.kartlar = {}
        for key, baslik_k, renk, ikon in [
            ("toplam_kitap",  "Toplam Kitap",    MAVI,    "📚"),
            ("toplam_uye",    "Aktif Üye",        YESIL,   "👥"),
            ("aktif_odunc",   "Ödünçte",          SARI,    "🔄"),
            ("gec_kalan",     "Gecikmiş",         KIRMIZI, "⚠️"),
            ("musait_kitap",  "Müsait Kitap",     MOR,     "✅"),
            ("bugun_iade",    "Bugün İade",       CAMASI,  "📅"),
        ]:
            kart = QFrame()
            kart.setStyleSheet(f"""
                QFrame {{ background:{PANEL}; border:2px solid {renk}22;
                         border-radius:12px; padding:10px; }}
            """)
            kv = QVBoxLayout(kart)
            kv.setSpacing(4)
            ikon_lbl = QLabel(ikon)
            ikon_lbl.setStyleSheet("font-size:26px;")
            ikon_lbl.setAlignment(Qt.AlignCenter)
            val_lbl = QLabel("—")
            val_lbl.setStyleSheet(f"font-size:28px; font-weight:bold; color:{renk};")
            val_lbl.setAlignment(Qt.AlignCenter)
            bas_lbl = QLabel(baslik_k)
            bas_lbl.setStyleSheet(f"font-size:11px; color:{SOLUK};")
            bas_lbl.setAlignment(Qt.AlignCenter)
            kv.addWidget(ikon_lbl)
            kv.addWidget(val_lbl)
            kv.addWidget(bas_lbl)
            self.kartlar[key] = val_lbl
            kart_row.addWidget(kart)
        ana.addLayout(kart_row)

        # Ana menü butonları
        menu_grup = QGroupBox("🗂️ Modüller")
        menu_row = QHBoxLayout(menu_grup)
        menu_row.setContentsMargins(14, 18, 14, 14)
        menu_row.setSpacing(14)

        for metin, renk, slot in [
            ("📚  Kitap Yönetimi",   MAVI,    self._kitapPencere),
            ("👤  Üye Yönetimi",     YESIL,   self._uyePencere),
            ("🔄  Ödünç İşlemleri", SARI,    self._oduncPencere),
            ("📊  Raporlar",         MOR,     self._raporPencere),
        ]:
            b = QPushButton(metin)
            b.setStyleSheet(f"""
                QPushButton {{
                    background:{renk}22; color:{renk};
                    border:2px solid {renk}55;
                    border-radius:10px;
                    padding:18px 10px;
                    font-size:14px;
                    font-weight:bold;
                }}
                QPushButton:hover {{
                    background:{renk}44;
                    border:2px solid {renk};
                }}
            """)
            b.clicked.connect(slot)
            menu_row.addWidget(b)
        ana.addWidget(menu_grup)

        # Alt bilgi satırı
        self.durum_lbl = QLabel()
        self.durum_lbl.setStyleSheet(f"color:{SOLUK}; font-size:11px;")
        self.durum_lbl.setAlignment(Qt.AlignCenter)
        ana.addWidget(self.durum_lbl)

    def _istatGuncelle(self):
        ist = self.db.istatistik()
        for key, val in ist.items():
            if key in self.kartlar and not isinstance(val, tuple):
                self.kartlar[key].setText(str(val))
        now = datetime.now().strftime("%d.%m.%Y %H:%M")
        self.durum_lbl.setText(f"Son güncelleme: {now}  ·  Veritabanı: {DB.DOSYA}")
        self.statusBar().showMessage(f"Toplam işlem: {ist['toplam_islem']}", 5000)

    def _kitapPencere(self):
        pencere = KitapPencere(self.db, self)
        pencere.exec_()
        self._istatGuncelle()

    def _uyePencere(self):
        pencere = UyePencere(self.db, self)
        pencere.exec_()
        self._istatGuncelle()

    def _oduncPencere(self):
        pencere = OduncPencere(self.db, self)
        pencere.exec_()
        self._istatGuncelle()

    def _raporPencere(self):
        pencere = RaporPencere(self.db, self)
        pencere.exec_()

    def closeEvent(self, event):
        if os.path.exists(DB.DOSYA):
            os.remove(DB.DOSYA)
        event.accept()


# ── Başlat ────────────────────────────────────────────────
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    pencere = AnaPencere()
    pencere.show()
    sys.exit(app.exec_())
