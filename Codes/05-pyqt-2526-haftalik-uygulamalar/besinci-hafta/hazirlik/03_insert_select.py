"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Python Mini Örnek — INSERT & SELECT
 Konu : Veri ekleme, sorgulama, fetchall
 Hafta: 5
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
import sqlite3

def tablo_yazdir(baslik, satirlar, basliklar):
    print(f"\n  {'─'*60}")
    print(f"  {baslik}")
    print(f"  {'─'*60}")
    genislikler = [max(len(str(b)), max((len(str(s[i])) for s in satirlar), default=0))
                   for i, b in enumerate(basliklar)]
    fmt = "  " + "  ".join(f"{{:<{g}}}" for g in genislikler)
    print(fmt.format(*basliklar))
    print("  " + "  ".join("─" * g for g in genislikler))
    for satir in satirlar:
        print(fmt.format(*[str(s) for s in satir]))

with sqlite3.connect(":memory:") as db:
    db.row_factory = sqlite3.Row   # ← Sütun adıyla erişim sağlar
    cursor = db.cursor()

    # Tablo oluştur
    cursor.execute("""
        CREATE TABLE ogrenciler (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ad TEXT NOT NULL, soyad TEXT NOT NULL,
            bolum TEXT, gpa REAL DEFAULT 0.0
        )
    """)

    # ── 1. Tekli INSERT ───────────────────────────
    # ? ile parametreli sorgu — SQL injection'a karşı güvenli!
    cursor.execute(
        "INSERT INTO ogrenciler (ad, soyad, bolum, gpa) VALUES (?, ?, ?, ?)",
        ("Ahmet", "Yılmaz", "Bilgisayar Müh.", 3.45)
    )
    print(f"✅ Tekli INSERT — son eklenen id: {cursor.lastrowid}")

    # ── 2. Çoklu INSERT (executemany) ────────────
    veri_listesi = [
        ("Zeynep", "Kaya",   "Elektrik Müh.",  3.80),
        ("Mehmet", "Demir",  "Makine Müh.",     2.95),
        ("Elif",   "Çelik",  "Bilgisayar Müh.", 3.92),
        ("Can",    "Arslan", "Endüstri Müh.",   3.10),
        ("Selin",  "Öztürk","Bilgisayar Müh.", 3.67),
    ]
    cursor.executemany(
        "INSERT INTO ogrenciler (ad, soyad, bolum, gpa) VALUES (?, ?, ?, ?)",
        veri_listesi
    )
    print(f"✅ executemany ile {len(veri_listesi)} kayıt eklendi.")
    db.commit()

    # ── 3. Tüm kayıtları getir ────────────────────
    cursor.execute("SELECT * FROM ogrenciler")
    satirlar = cursor.fetchall()
    tablo_yazdir("Tüm Öğrenciler (fetchall)", satirlar, ["id","ad","soyad","bolum","gpa"])

    # ── 4. fetchone — tek satır ───────────────────
    cursor.execute("SELECT * FROM ogrenciler WHERE id = ?", (1,))
    tek = cursor.fetchone()
    print(f"\n  fetchone → id=1: {tek['ad']} {tek['soyad']}")

    # ── 5. WHERE filtresi ─────────────────────────
    cursor.execute("SELECT * FROM ogrenciler WHERE bolum = ?", ("Bilgisayar Müh.",))
    bm = cursor.fetchall()
    tablo_yazdir("Bilgisayar Müh. Öğrencileri (WHERE)", bm, ["id","ad","soyad","bolum","gpa"])

    # ── 6. ORDER BY ───────────────────────────────
    cursor.execute("SELECT ad, soyad, gpa FROM ogrenciler ORDER BY gpa DESC")
    sirali = cursor.fetchall()
    tablo_yazdir("GPA'ya Göre Sıralı (ORDER BY DESC)", sirali, ["ad","soyad","gpa"])

    # ── 7. Aggregate fonksiyonlar ─────────────────
    cursor.execute("SELECT COUNT(*), AVG(gpa), MAX(gpa), MIN(gpa) FROM ogrenciler")
    istat = cursor.fetchone()
    print(f"\n  📊 İstatistik → Sayı: {istat[0]} | Ort: {istat[1]:.2f} | Max: {istat[2]} | Min: {istat[3]}")

    # ── 8. LIKE ile metin arama ───────────────────
    cursor.execute("SELECT ad, soyad FROM ogrenciler WHERE ad LIKE ?", ("%e%",))
    eslesler = cursor.fetchall()
    print(f"\n  LIKE '%e%' → {[f'{r[0]} {r[1]}' for r in eslesler]}")

print("\n⚠️  ÖNEMLİ: ? Parametreli Sorgu Neden Şart?")
print("   ❌ YANLIŞ: f\"SELECT * FROM t WHERE ad = '{ad}'\"  → SQL Injection riski!")
print("   ✅ DOĞRU:  cursor.execute('SELECT * FROM t WHERE ad = ?', (ad,))")
