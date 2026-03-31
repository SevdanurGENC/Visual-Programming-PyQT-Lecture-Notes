"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Python Mini Örnek — UPDATE & DELETE
 Konu : Veri güncelleme ve silme
 Hafta: 5
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
import sqlite3

def listele(cursor, baslik=""):
    cursor.execute("SELECT id, ad, soyad, gpa, aktif FROM ogrenciler ORDER BY id")
    satirlar = cursor.fetchall()
    print(f"\n  {'─'*52}  {baslik}")
    print(f"  {'id':<5} {'Ad':<10} {'Soyad':<12} {'GPA':<7} {'Aktif'}")
    print("  " + "─"*52)
    for r in satirlar:
        aktif_str = "✅" if r[4] else "❌"
        print(f"  {r[0]:<5} {r[1]:<10} {r[2]:<12} {r[3]:<7} {aktif_str}")

with sqlite3.connect(":memory:") as db:
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE ogrenciler (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ad TEXT, soyad TEXT, gpa REAL, aktif INTEGER DEFAULT 1
        )
    """)
    cursor.executemany("INSERT INTO ogrenciler (ad, soyad, gpa) VALUES (?,?,?)", [
        ("Ahmet","Yılmaz",3.2), ("Zeynep","Kaya",3.8),
        ("Mehmet","Demir",2.5), ("Elif","Çelik",3.9), ("Can","Arslan",1.8),
    ])
    db.commit()
    listele(cursor, "← Başlangıç durumu")

    # ── 1. Tek kayıt güncelleme ───────────────────
    cursor.execute("UPDATE ogrenciler SET gpa = ? WHERE id = ?", (3.5, 1))
    db.commit()
    etkilenen = cursor.rowcount           # kaç satır etkilendi?
    print(f"\n✅ UPDATE id=1: gpa → 3.5  (etkilenen satır: {etkilenen})")
    listele(cursor, "← id=1 GPA güncellendi")

    # ── 2. Koşullu toplu güncelleme ───────────────
    cursor.execute("UPDATE ogrenciler SET aktif = 0 WHERE gpa < ?", (2.0,))
    db.commit()
    print(f"\n✅ UPDATE aktif=0 WHERE gpa<2.0  (etkilenen: {cursor.rowcount})")
    listele(cursor, "← GPA<2.0 pasife alındı")

    # ── 3. Birden fazla alan güncelleme ───────────
    cursor.execute(
        "UPDATE ogrenciler SET gpa = ?, aktif = ? WHERE id = ?",
        (4.0, 1, 3)
    )
    db.commit()
    print(f"\n✅ UPDATE id=3: gpa=4.0, aktif=1")
    listele(cursor, "← id=3 tam güncelleme")

    # ── 4. Tek kayıt silme ────────────────────────
    cursor.execute("DELETE FROM ogrenciler WHERE id = ?", (5,))
    db.commit()
    print(f"\n✅ DELETE id=5  (etkilenen: {cursor.rowcount})")
    listele(cursor, "← id=5 silindi")

    # ── 5. Koşullu silme ──────────────────────────
    cursor.execute("DELETE FROM ogrenciler WHERE aktif = 0")
    db.commit()
    print(f"\n✅ DELETE WHERE aktif=0  (etkilenen: {cursor.rowcount})")
    listele(cursor, "← Pasif kayıtlar temizlendi")

    # ── 6. Tüm tabloyu temizle (DİKKAT!) ─────────
    # cursor.execute("DELETE FROM ogrenciler")  # Tüm satırları siler
    # cursor.execute("DROP TABLE ogrenciler")    # Tabloyu tamamen siler
    print("\n  ⚠️  DELETE FROM tablo → tüm satırları siler (WHERE olmadan!)")
    print("  ⚠️  DROP TABLE tablo  → tabloyu komple siler")

    # ── 7. ROLLBACK — geri alma ───────────────────
    print("\n--- ROLLBACK (geri alma) Örneği ---")
    cursor.execute("DELETE FROM ogrenciler WHERE id = ?", (1,))
    print(f"  id=1 silindi (commit edilmedi)...")
    listele(cursor, "← commit öncesi (geçici)")
    db.rollback()                         # ← geri al!
    listele(cursor, "← rollback sonrası (geri alındı)")
    print("✅ rollback() ile silme geri alındı.")
