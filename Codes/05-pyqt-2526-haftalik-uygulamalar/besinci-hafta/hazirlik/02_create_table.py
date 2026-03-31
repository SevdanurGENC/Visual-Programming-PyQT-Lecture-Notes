"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Python Mini Örnek — CREATE TABLE
 Konu : Tablo oluşturma, veri tipleri
 Hafta: 5
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
import sqlite3

print("=" * 55)
print("  SQLite — CREATE TABLE ve Veri Tipleri")
print("=" * 55)

with sqlite3.connect(":memory:") as db:
    cursor = db.cursor()

    # ── 1. Temel tablo oluşturma ──────────────────
    # IF NOT EXISTS → tablo zaten varsa hata vermez
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ogrenciler (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            ad        TEXT    NOT NULL,
            soyad     TEXT    NOT NULL,
            numara    TEXT    UNIQUE NOT NULL,
            yas       INTEGER,
            gpa       REAL    DEFAULT 0.0,
            aktif     INTEGER DEFAULT 1,
            kayit_tarihi TEXT DEFAULT CURRENT_DATE
        )
    """)
    print("\n✅ 'ogrenciler' tablosu oluşturuldu.")

    # ── 2. İlişkili ikinci tablo ──────────────────
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dersler (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            ogrenci_id INTEGER NOT NULL,
            ders_adi  TEXT    NOT NULL,
            not_degeri REAL,
            donem     TEXT,
            FOREIGN KEY (ogrenci_id) REFERENCES ogrenciler(id)
        )
    """)
    print("✅ 'dersler' tablosu oluşturuldu.")

    # ── 3. Tablo listesini görüntüle ──────────────
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tablolar = cursor.fetchall()
    print(f"\n📋 Mevcut tablolar: {[t[0] for t in tablolar]}")

    # ── 4. Tablo yapısını görüntüle ───────────────
    cursor.execute("PRAGMA table_info(ogrenciler)")
    kolonlar = cursor.fetchall()
    print("\n🔍 'ogrenciler' tablo yapısı:")
    print(f"  {'Sıra':<5} {'Ad':<18} {'Tip':<12} {'NULL?':<8} {'Varsayılan':<14} {'PK'}")
    print("  " + "-" * 62)
    for kolon in kolonlar:
        cid, isim, tip, notnull, default, pk = kolon
        null_str = "NOT NULL" if notnull else "NULL"
        def_str  = str(default) if default is not None else "-"
        pk_str   = "✅ PK" if pk else ""
        print(f"  {cid:<5} {isim:<18} {tip:<12} {null_str:<8} {def_str:<14} {pk_str}")

    # ── 5. Tabloyu silme ──────────────────────────
    cursor.execute("DROP TABLE IF EXISTS dersler")
    print("\n🗑️  'dersler' tablosu silindi.")

print("\n" + "=" * 55)
print("  SQLite Veri Tipleri Özeti")
print("=" * 55)
print("""
  INTEGER  → Tam sayı (id, yaş, bool için 0/1)
  TEXT     → Metin
  REAL     → Ondalıklı sayı (GPA, fiyat)
  BLOB     → İkili veri (resim, dosya)
  NULL     → Boş değer

  Kısıtlar (Constraints):
  PRIMARY KEY     → Birincil anahtar, benzersiz
  AUTOINCREMENT   → Otomatik artan sayı
  NOT NULL        → Boş bırakılamaz
  UNIQUE          → Tekrar edemez
  DEFAULT değer   → Varsayılan değer
  FOREIGN KEY     → Yabancı anahtar (ilişki)
""")
