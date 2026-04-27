"""
╔══════════════════════════════════════════════════════════════════════════╗
║  Kişi Rehberi — Qt Designer + PyQt5 Örnek Uygulaması                   ║
║  Görsel Programlama Dersi — Dr. Öğr. Üyesi Sevdanur GENÇ               ║
╠══════════════════════════════════════════════════════════════════════════╣
║  Kullanım:                                                               ║
║    1) kisi_rehberi.ui ile aynı klasöre koyun                            ║
║    2) python kisi_rehberi.py                                             ║
║                                                                          ║
║  Gereksinimler:                                                          ║
║    pip install pyqt5                                                     ║
║                                                                          ║
║  Qt Designer'dan Python'a bağlama yöntemi: uic.loadUi()                 ║
╚══════════════════════════════════════════════════════════════════════════╝

ÖNEMLI NOT — iki farklı kullanım yöntemi:

  Yöntem 1 — Çalışma zamanında yükle (önerilen geliştirme için):
      uic.loadUi("kisi_rehberi.ui", self)

  Yöntem 2 — Python koduna dönüştür (dağıtım için):
      Terminalde: pyuic5 kisi_rehberi.ui -o kisi_rehberi_ui.py
      Sonra kodda: from kisi_rehberi_ui import Ui_MainWindow
"""

import sys
import sqlite3
import csv
import os
from PyQt5 import uic                          # ← .ui dosyasını yükleyen modül
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTableWidgetItem,
    QMessageBox, QFileDialog, QAbstractItemView
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

# .ui dosyasının yolu — bu script ile aynı klasörde olmalı
UI_DOSYA = os.path.join(os.path.dirname(__file__), "kisi_rehberi.ui")
DB_DOSYA = os.path.join(os.path.dirname(__file__), "rehber.db")


# ══════════════════════════════════════════════════════════════════════════
#  VERİTABANI
# ══════════════════════════════════════════════════════════════════════════
class DB:
    def __init__(self):
        self._kur()

    def _baglan(self):
        db = sqlite3.connect(DB_DOSYA)
        db.row_factory = sqlite3.Row
        return db

    def _kur(self):
        with self._baglan() as db:
            db.execute("""
                CREATE TABLE IF NOT EXISTS kisiler (
                    id       INTEGER PRIMARY KEY AUTOINCREMENT,
                    ad       TEXT NOT NULL,
                    soyad    TEXT NOT NULL,
                    telefon  TEXT,
                    email    TEXT,
                    grup     TEXT DEFAULT 'Diğer',
                    not_     TEXT,
                    favori   INTEGER DEFAULT 0,
                    eklenme  TEXT DEFAULT CURRENT_DATE
                )
            """)
            # Demo veriler (boşsa)
            if db.execute("SELECT COUNT(*) FROM kisiler").fetchone()[0] == 0:
                db.executemany(
                    "INSERT INTO kisiler (ad,soyad,telefon,email,grup,favori) VALUES (?,?,?,?,?,?)", [
                    ("Ahmet",   "Yılmaz", "0532-111-1111", "ahmet@mail.com",   "👨‍👩‍👧  Aile",    1),
                    ("Zeynep",  "Kaya",   "0533-222-2222", "zeynep@mail.com",  "👥  Arkadaş",  0),
                    ("Prof. Can","Arslan", "0534-333-3333", "can@uni.edu",      "💼  İş",       1),
                    ("Elif",    "Çelik",  "0535-444-4444", "elif@mail.com",    "🎓  Okul",     0),
                    ("Mehmet",  "Demir",  "0536-555-5555", "mehmet@work.com",  "💼  İş",       0),
                    ("Selin",   "Öztürk", "0537-666-6666", "selin@mail.com",   "👥  Arkadaş",  1),
                ])

    def getir(self, arama="", grup_filtre=""):
        with self._baglan() as db:
            kosullar, params = [], []
            if arama:
                kosullar.append("(ad LIKE ? OR soyad LIKE ? OR telefon LIKE ?)")
                params += [f"%{arama}%"] * 3
            if grup_filtre == "⭐ Favori":
                kosullar.append("favori = 1")
            elif grup_filtre:
                kosullar.append("grup = ?")
                params.append(grup_filtre)
            where = ("WHERE " + " AND ".join(kosullar)) if kosullar else ""
            return db.execute(
                f"SELECT * FROM kisiler {where} ORDER BY ad, soyad", params
            ).fetchall()

    def ekle(self, v):
        with self._baglan() as db:
            db.execute(
                "INSERT INTO kisiler (ad,soyad,telefon,email,grup,not_,favori) VALUES (?,?,?,?,?,?,?)", v
            )
    def guncelle(self, id_, v):
        with self._baglan() as db:
            db.execute(
                "UPDATE kisiler SET ad=?,soyad=?,telefon=?,email=?,grup=?,not_=?,favori=? WHERE id=?",
                (*v, id_)
            )
    def sil(self, id_):
        with self._baglan() as db:
            db.execute("DELETE FROM kisiler WHERE id=?", (id_,))

    def istatistik(self):
        with self._baglan() as db:
            return {
                "toplam":   db.execute("SELECT COUNT(*) FROM kisiler").fetchone()[0],
                "aile":     db.execute("SELECT COUNT(*) FROM kisiler WHERE grup LIKE '%Aile%'").fetchone()[0],
                "arkadaslar":db.execute("SELECT COUNT(*) FROM kisiler WHERE grup LIKE '%Arkadaş%'").fetchone()[0],
                "is":       db.execute("SELECT COUNT(*) FROM kisiler WHERE grup LIKE '%İş%'").fetchone()[0],
                "favori":   db.execute("SELECT COUNT(*) FROM kisiler WHERE favori=1").fetchone()[0],
            }


# ══════════════════════════════════════════════════════════════════════════
#  ANA PENCERE — Qt Designer .ui dosyasından yüklenir
# ══════════════════════════════════════════════════════════════════════════
class KisiRehberi(QMainWindow):

    def __init__(self):
        super().__init__()

        # ════════════════════════════════════════════════
        #  .ui DOSYASINI YÜKLE — Qt Designer bağlantısı
        # ════════════════════════════════════════════════
        uic.loadUi(UI_DOSYA, self)
        # Bu tek satır tüm widget'ları self.'isim' olarak erişilebilir kılar.
        # Örnek: self.adInput, self.kisilerTablosu, self.ekleBtn vs.

        self.db = DB()
        self.aktifId = None          # Seçili kaydın id'si

        self._stilUygula()
        self._sinyalleriBagla()
        self.listele()

    # ── Stil ────────────────────────────────────────────
    def _stilUygula(self):
        self.setStyleSheet("""
        QMainWindow, QWidget {
            background-color: #0F172A;
            color: #E2E8F0;
            font-family: 'Segoe UI';
            font-size: 13px;
        }
        QGroupBox {
            border: 1px solid #334155;
            border-radius: 8px;
            margin-top: 14px;
            padding-top: 8px;
            font-weight: bold;
            color: #6366F1;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top left;
            padding: 0 8px;
        }
        QLineEdit, QComboBox, QTextEdit {
            background: #1E293B;
            border: 1px solid #334155;
            border-radius: 6px;
            padding: 6px 10px;
            color: #E2E8F0;
        }
        QLineEdit:focus, QTextEdit:focus { border: 1px solid #6366F1; }
        QComboBox QAbstractItemView {
            background: #1E293B;
            selection-background-color: #6366F1;
        }
        QTableWidget {
            background: #1E293B;
            border: 1px solid #334155;
            gridline-color: #334155;
            color: #E2E8F0;
            border-radius: 6px;
        }
        QTableWidget::item:selected { background: #6366F1; }
        QTableWidget::item:alternate { background: #162032; }
        QHeaderView::section {
            background: #1E3A5F;
            color: #06B6D4;
            padding: 7px;
            border: 1px solid #334155;
            font-weight: bold;
        }
        QPushButton {
            border-radius: 6px;
            padding: 8px 16px;
            font-weight: bold;
            color: white;
            border: none;
            background: #475569;
        }
        QPushButton:hover { background: #64748B; }
        QPushButton:disabled { background: #1E293B; color: #475569; }
        QPushButton#ekleBtn    { background: #22C55E; }
        QPushButton#ekleBtn:hover { background: #16A34A; }
        QPushButton#guncelleBtn { background: #F59E0B; }
        QPushButton#guncelleBtn:hover { background: #D97706; }
        QPushButton#silBtn     { background: #EF4444; }
        QPushButton#silBtn:hover { background: #DC2626; }
        QPushButton#csvExportBtn { background: #3B82F6; }
        QPushButton#csvExportBtn:hover { background: #2563EB; }
        QPushButton[checkable="true"]:checked { background: #6366F1; }
        QCheckBox { spacing: 8px; }
        QCheckBox::indicator:checked { background: #6366F1; border-radius: 3px; }
        QLabel#baslikLabel { color: #E2E8F0; }
        QLabel#durumLabel  { color: #6366F1; font-style: italic; }
        QMenuBar { background: #1E293B; color: #E2E8F0; }
        QMenuBar::item:selected { background: #6366F1; }
        QMenu { background: #1E293B; border: 1px solid #334155; }
        QMenu::item:selected { background: #6366F1; }
        QStatusBar { background: #0F172A; color: #64748B; }
        """)

    # ── Sinyal - Slot Bağlantıları ───────────────────────
    def _sinyalleriBagla(self):
        # Butonlar
        self.ekleBtn.clicked.connect(self._ekle)
        self.guncelleBtn.clicked.connect(self._guncelle)
        self.silBtn.clicked.connect(self._sil)
        self.temizleBtn.clicked.connect(self._formTemizle)

        # Arama
        self.aramaInput.textChanged.connect(self.listele)
        self.aramaTemizleBtn.clicked.connect(self.aramaInput.clear)

        # Filtre butonları
        self.filtreHepsiBtn.clicked.connect(lambda: self._filtreUygula(""))
        self.filtreAileBtn.clicked.connect(lambda: self._filtreUygula("👨‍👩‍👧  Aile"))
        self.filtreArkadasBtn.clicked.connect(lambda: self._filtreUygula("👥  Arkadaş"))
        self.filtreIsBtn.clicked.connect(lambda: self._filtreUygula("💼  İş"))
        self.filtreFavoriBtn.clicked.connect(lambda: self._filtreUygula("⭐ Favori"))

        # Tablo tıklama → formu doldur
        self.kisilerTablosu.clicked.connect(self._satirSec)

        # CSV export
        self.csvExportBtn.clicked.connect(self._csvExport)

        # Menü aksiyonları
        self.actionCikis.triggered.connect(self.close)
        self.actionAra.triggered.connect(lambda: self.aramaInput.setFocus())
        self.actionHakkinda.triggered.connect(self._hakkinda)

        # Klavye kısayolu: Enter → ekle
        self.adInput.returnPressed.connect(self._ekle)

        # Tablo sütun genişliği ayarla
        self.kisilerTablosu.verticalHeader().setVisible(False)

    # ── Veri işlemleri ────────────────────────────────────

    def listele(self):
        arama = self.aramaInput.text().strip()
        grup  = getattr(self, "_aktifFiltre", "")
        satirlar = self.db.getir(arama, grup)

        self.kisilerTablosu.setSortingEnabled(False)
        self.kisilerTablosu.setRowCount(len(satirlar))
        for ri, r in enumerate(satirlar):
            degerler = [r["id"], r["ad"], r["soyad"], r["telefon"] or "—",
                        r["grup"], "⭐" if r["favori"] else ""]
            for ci, d in enumerate(degerler):
                item = QTableWidgetItem(str(d) if d else "")
                item.setTextAlignment(Qt.AlignCenter)
                if ci == 5 and d == "⭐":
                    item.setForeground(QColor("#F59E0B"))
                self.kisilerTablosu.setItem(ri, ci, item)

        # Sütun genişlikleri
        for i, w in enumerate([0, 110, 120, 130, 130, 40]):
            self.kisilerTablosu.setColumnWidth(i, w)
        self.kisilerTablosu.setColumnHidden(0, True)   # ID sütununu gizle
        self.kisilerTablosu.horizontalHeader().setStretchLastSection(True)
        self.kisilerTablosu.setSortingEnabled(True)

        self.sayacLabel.setText(f"{len(satirlar)} kişi")
        self._istatGuncelle()

    def _satirSec(self):
        satir = self.kisilerTablosu.currentRow()
        if satir < 0:
            return
        # Gizli ID sütunundan id oku
        id_item = self.kisilerTablosu.item(satir, 0)
        if not id_item:
            return
        self.aktifId = int(id_item.text())
        with sqlite3.connect(DB_DOSYA) as db:
            db.row_factory = sqlite3.Row
            kayit = db.execute("SELECT * FROM kisiler WHERE id=?", (self.aktifId,)).fetchone()
        if not kayit:
            return
        self.adInput.setText(kayit["ad"])
        self.soyadInput.setText(kayit["soyad"])
        self.telefonInput.setText(kayit["telefon"] or "")
        self.emailInput.setText(kayit["email"] or "")
        self.notInput.setPlainText(kayit["not_"] or "")
        self.favoriCheck.setChecked(bool(kayit["favori"]))
        idx = self.grupCombo.findText(kayit["grup"])
        if idx >= 0:
            self.grupCombo.setCurrentIndex(idx)
        self.guncelleBtn.setEnabled(True)
        self.silBtn.setEnabled(True)
        self._durumGoster(f"Seçili: {kayit['ad']} {kayit['soyad']}", "#06B6D4")

    def _formVerileri(self):
        ad    = self.adInput.text().strip()
        soyad = self.soyadInput.text().strip()
        if not ad or not soyad:
            return None, "Ad ve soyad zorunludur!"
        return (
            ad, soyad,
            self.telefonInput.text().strip(),
            self.emailInput.text().strip(),
            self.grupCombo.currentText(),
            self.notInput.toPlainText().strip(),
            1 if self.favoriCheck.isChecked() else 0
        ), None

    def _ekle(self):
        veri, hata = self._formVerileri()
        if hata:
            QMessageBox.warning(self, "Eksik Bilgi", hata)
            return
        self.db.ekle(veri)
        self._formTemizle()
        self.listele()
        self._durumGoster("✅ Kişi başarıyla eklendi!", "#22C55E")
        self.statusBar().showMessage("Yeni kişi eklendi.", 3000)

    def _guncelle(self):
        if not self.aktifId:
            return
        veri, hata = self._formVerileri()
        if hata:
            QMessageBox.warning(self, "Eksik Bilgi", hata)
            return
        self.db.guncelle(self.aktifId, veri)
        self._formTemizle()
        self.listele()
        self._durumGoster("✅ Kayıt güncellendi!", "#F59E0B")
        self.statusBar().showMessage("Kayıt güncellendi.", 3000)

    def _sil(self):
        if not self.aktifId:
            return
        ad = self.adInput.text()
        cevap = QMessageBox.question(
            self, "Silme Onayı",
            f"<b>{ad}</b> kişisini silmek istediğinizden emin misiniz?",
            QMessageBox.Yes | QMessageBox.No
        )
        if cevap == QMessageBox.Yes:
            self.db.sil(self.aktifId)
            self._formTemizle()
            self.listele()
            self._durumGoster("🗑️ Kayıt silindi.", "#EF4444")

    def _formTemizle(self):
        for w in [self.adInput, self.soyadInput, self.telefonInput, self.emailInput]:
            w.clear()
        self.notInput.clear()
        self.favoriCheck.setChecked(False)
        self.grupCombo.setCurrentIndex(0)
        self.aktifId = None
        self.guncelleBtn.setEnabled(False)
        self.silBtn.setEnabled(False)
        self.durumLabel.setText("Bilgileri doldurup \"Ekle\" butonuna basın.")
        self.durumLabel.setStyleSheet("color: #6366F1; font-style: italic;")

    def _filtreUygula(self, grup):
        self._aktifFiltre = grup
        self.listele()

    def _istatGuncelle(self):
        ist = self.db.istatistik()
        self.toplamLabel.setText(f"Toplam: <b>{ist['toplam']}</b>")
        self.aileSayiLabel.setText(f"👨‍👩‍👧 Aile: {ist['aile']}")
        self.arkadasSayiLabel.setText(f"👥 Arkadaş: {ist['arkadaslar']}")
        self.isSayiLabel.setText(f"💼 İş: {ist['is']}")
        self.favoriSayiLabel.setText(f"⭐ Favori: {ist['favori']}")

    def _durumGoster(self, metin, renk="#6366F1"):
        self.durumLabel.setText(metin)
        self.durumLabel.setStyleSheet(f"color: {renk}; font-style: italic; font-weight: bold;")

    def _csvExport(self):
        yol, _ = QFileDialog.getSaveFileName(
            self, "CSV Dışa Aktar", "kisiler.csv", "CSV Dosyaları (*.csv)"
        )
        if not yol:
            return
        try:
            with sqlite3.connect(DB_DOSYA) as db:
                satirlar = db.execute("SELECT ad,soyad,telefon,email,grup,favori FROM kisiler ORDER BY ad").fetchall()
            with open(yol, "w", newline="", encoding="utf-8-sig") as f:
                w = csv.writer(f)
                w.writerow(["Ad", "Soyad", "Telefon", "E-posta", "Grup", "Favori"])
                w.writerows([[*r[:5], "Evet" if r[5] else "Hayır"] for r in satirlar])
            QMessageBox.information(self, "Başarılı", f"✅ {len(satirlar)} kişi dışa aktarıldı!\n{yol}")
        except Exception as e:
            QMessageBox.critical(self, "Hata", str(e))

    def _hakkinda(self):
        QMessageBox.information(self, "Hakkında",
            "<b>Kişi Rehberi</b><br><br>"
            "Qt Designer + PyQt5 örnek uygulaması<br>"
            "Görsel Programlama Dersi<br>"
            "Dr. Öğr. Üyesi Sevdanur GENÇ"
        )

    def closeEvent(self, event):
        # Veritabanını kapat
        event.accept()


# ══════════════════════════════════════════════════════════════════════════
#  ÇALIŞTIR
# ══════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    pencere = KisiRehberi()
    pencere.show()
    sys.exit(app.exec_())
