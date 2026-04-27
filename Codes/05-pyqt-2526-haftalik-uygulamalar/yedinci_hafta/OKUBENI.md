# Kişi Rehberi — Qt Designer + PyQt5 Örnek Uygulaması
### Görsel Programlama Dersi | Dr. Öğr. Üyesi Sevdanur GENÇ

---

## 📁 Dosyalar

```
kisi_rehberi.ui    ← Qt Designer'da tasarlanan arayüz (XML)
kisi_rehberi.py    ← Python mantık kodu (uic.loadUi ile bağlanır)
OKUBENI.md         ← Bu dosya
```

---

## ⚙️ Kurulum

```bash
pip install pyqt5
```

### VS Code İçin Qt Designer Eklentisi

1. VS Code → Extensions → **"Qt for Python"** (seanwu) yükle
2. `.ui` dosyasına sağ tıkla → **"Edit in Qt Designer"**

---

## 🚀 Çalıştırma

```bash
python kisi_rehberi.py
```

**İki dosyanın aynı klasörde olması şarttır.**

---

## 🔗 .ui → Python Bağlama Yöntemleri

### Yöntem 1 — Çalışma zamanında yükle (bu projede kullanılan)
```python
from PyQt5 import uic
uic.loadUi("kisi_rehberi.ui", self)
# self.adInput, self.ekleBtn gibi tüm widget'lar hazır!
```

### Yöntem 2 — pyuic5 ile Python dosyasına dönüştür
```bash
# Terminalde çalıştır:
pyuic5 kisi_rehberi.ui -o kisi_rehberi_ui.py

# Sonra Python'da:
from kisi_rehberi_ui import Ui_MainWindow
class AnaPencere(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
```

---

## 🎯 Bu Projede Kullanılan Qt Designer Özellikleri

| Qt Designer Bileşeni | Kullanım Yeri |
|---|---|
| `QMainWindow` | Ana pencere çerçevesi |
| `QMenuBar` + `QMenu` + `QAction` | Dosya / Düzenle / Yardım menüleri |
| `QStatusBar` | Alt durum çubuğu |
| `QSplitter` | Sol form / Sağ tablo bölümü |
| `QGroupBox` | "Kişi Bilgileri" çerçevesi |
| `QFormLayout` | Etiket-giriş çiftleri |
| `QVBoxLayout` + `QHBoxLayout` | Düzen yönetimi |
| `QLineEdit` | Ad, soyad, telefon, e-posta girişi |
| `QComboBox` | Grup seçimi |
| `QTextEdit` | Not alanı |
| `QCheckBox` | Favori işaretleme |
| `QPushButton` | Ekle, güncelle, sil, filtre butonları |
| `QTableWidget` | Kişi listesi tablosu |
| `QLabel` | Başlık ve istatistik etiketleri |
| `QSpacer` | Boşluk kontrolü |

---

## 🗄️ SQLite Tablosu

```sql
CREATE TABLE kisiler (
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
```

---

## 💡 Öğrenci Notları

- `uic.loadUi()` tek satırla tüm arayüzü yükler
- Widget isimleri (objectName) `.ui` içinde tanımlanır, Python'da `self.isim` ile erişilir
- Sinyal-Slot bağlantıları **Python kodunda** kurulur (.ui içinde değil)
- `.ui` değiştiğinde Python kodunu değiştirmeye gerek yok (Yöntem 1 ile)
