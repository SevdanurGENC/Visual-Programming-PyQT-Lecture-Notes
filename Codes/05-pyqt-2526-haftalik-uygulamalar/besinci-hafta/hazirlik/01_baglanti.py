"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 PyQt5 / Python Mini Örnek — SQLite Bağlantı
 Konu : sqlite3 modülü, bağlantı, cursor
 Hafta: 5
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
import sqlite3
import os

print("=" * 50)
print("  SQLite — Bağlantı ve Temel Kavramlar")
print("=" * 50)

# ── 1. Diske kayıtlı veritabanı bağlantısı ────────
# Dosya yoksa otomatik oluşturulur
baglanti = sqlite3.connect("okul.db")
print("\n✅ 'okul.db' veritabanına bağlandı.")
print(f"   Dosya yolu: {os.path.abspath('okul.db')}")

# ── 2. Cursor (imleç) oluşturma ───────────────────
# Cursor; SQL komutlarını çalıştıran nesnedir
cursor = baglanti.cursor()
print("✅ Cursor oluşturuldu.")

# ── 3. SQLite sürüm bilgisi ───────────────────────
cursor.execute("SELECT sqlite_version()")
surum = cursor.fetchone()
print(f"✅ SQLite sürümü: {surum[0]}")

# ── 4. Bellekte geçici veritabanı ─────────────────
# Test için kullanışlı — program kapanınca silinir
gecici_db = sqlite3.connect(":memory:")
print("\n✅ ':memory:' ile bellekte geçici DB oluşturuldu.")

# ── 5. Bağlantıyı kapatma ─────────────────────────
# İşlemler bitince mutlaka kapatılmalıdır
baglanti.close()
gecici_db.close()
print("✅ Bağlantılar kapatıldı.")

# ── 6. Context Manager (with) — ÖNERİLEN YÖNTEM ──
print("\n--- Context Manager (with) Kullanımı ---")
with sqlite3.connect("okul.db") as baglanti:
    cursor = baglanti.cursor()
    cursor.execute("SELECT sqlite_version()")
    print(f"✅ with bloğunda sürüm: {cursor.fetchone()[0]}")
# with bloğu kapanınca bağlantı otomatik commit + close yapar
print("✅ with bloğu kapandı — bağlantı otomatik kapatıldı.")

# Temizlik
if os.path.exists("okul.db"):
    os.remove("okul.db")
    print("\n🗑️  Test dosyası silindi.")

print("\n" + "=" * 50)
print("  ÖZET")
print("=" * 50)
print("""
  sqlite3.connect('dosya.db')   → diske kayıtlı DB
  sqlite3.connect(':memory:')   → bellekte geçici DB
  baglanti.cursor()             → cursor oluştur
  cursor.execute(sql)           → SQL çalıştır
  baglanti.commit()             → değişiklikleri kaydet
  baglanti.close()              → bağlantıyı kapat
  with sqlite3.connect(...):    → önerilen yöntem
""")
