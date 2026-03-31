"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Python Mini Örnek — Sorgulama & Filtreleme
 Konu : WHERE, ORDER BY, LIKE, BETWEEN, JOIN
 Hafta: 5
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
import sqlite3

def yazdir(baslik, rows, cols):
    print(f"\n  📌 {baslik}")
    if not rows:
        print("  (sonuç yok)")
        return
    genislik = [max(len(str(c)), max(len(str(r[i])) for r in rows)) for i, c in enumerate(cols)]
    fmt = "  " + " │ ".join(f"{{:<{g}}}" for g in genislik)
    print(fmt.format(*cols))
    print("  " + "─┼─".join("─"*g for g in genislik))
    for r in rows:
        print(fmt.format(*[str(x) for x in r]))

with sqlite3.connect(":memory:") as db:
    db.row_factory = sqlite3.Row
    cur = db.cursor()

    # Hazırlık
    cur.executescript("""
        CREATE TABLE ogrenciler (
            id INTEGER PRIMARY KEY, ad TEXT, soyad TEXT,
            bolum TEXT, gpa REAL, sehir TEXT, yas INTEGER
        );
        CREATE TABLE notlar (
            id INTEGER PRIMARY KEY, ogrenci_id INTEGER,
            ders TEXT, not_degeri REAL
        );
        INSERT INTO ogrenciler VALUES
          (1,'Ahmet','Yılmaz','Bilgisayar',3.45,'Ankara',21),
          (2,'Zeynep','Kaya','Elektrik',3.80,'İstanbul',22),
          (3,'Mehmet','Demir','Makine',2.95,'İzmir',20),
          (4,'Elif','Çelik','Bilgisayar',3.92,'Ankara',23),
          (5,'Can','Arslan','Endüstri',3.10,'Bursa',21),
          (6,'Selin','Öztürk','Bilgisayar',3.67,'İstanbul',22),
          (7,'Burak','Şahin','Elektrik',2.40,'Ankara',24);
        INSERT INTO notlar VALUES
          (1,1,'Matematik',85),(2,1,'Fizik',72),
          (3,2,'Matematik',91),(4,2,'Fizik',88),
          (5,3,'Matematik',60),(6,4,'Matematik',95),
          (7,4,'Fizik',90),(8,6,'Matematik',82);
    """)
    db.commit()
    print("✅ Test veritabanı hazır.\n")

    # ── 1. WHERE ile filtreleme ───────────────────
    cur.execute("SELECT ad, soyad, gpa FROM ogrenciler WHERE bolum = ?", ("Bilgisayar",))
    yazdir("WHERE bolum='Bilgisayar'", cur.fetchall(), ["ad","soyad","gpa"])

    # ── 2. AND / OR ───────────────────────────────
    cur.execute("SELECT ad, bolum, gpa FROM ogrenciler WHERE bolum='Bilgisayar' AND gpa > 3.5")
    yazdir("WHERE bolum='Bilgisayar' AND gpa > 3.5", cur.fetchall(), ["ad","bolum","gpa"])

    # ── 3. BETWEEN ────────────────────────────────
    cur.execute("SELECT ad, soyad, gpa FROM ogrenciler WHERE gpa BETWEEN ? AND ?", (3.0, 3.7))
    yazdir("WHERE gpa BETWEEN 3.0 AND 3.7", cur.fetchall(), ["ad","soyad","gpa"])

    # ── 4. LIKE — metin arama ─────────────────────
    cur.execute("SELECT ad, sehir FROM ogrenciler WHERE sehir LIKE ?", ("%a%",))
    yazdir("WHERE sehir LIKE '%a%'", cur.fetchall(), ["ad","sehir"])

    # ── 5. IN ─────────────────────────────────────
    cur.execute("SELECT ad, sehir FROM ogrenciler WHERE sehir IN (?,?)", ("Ankara","İstanbul"))
    yazdir("WHERE sehir IN ('Ankara','İstanbul')", cur.fetchall(), ["ad","sehir"])

    # ── 6. ORDER BY — sıralama ────────────────────
    cur.execute("SELECT ad, gpa FROM ogrenciler ORDER BY gpa DESC LIMIT 3")
    yazdir("ORDER BY gpa DESC LIMIT 3 (ilk 3)", cur.fetchall(), ["ad","gpa"])

    cur.execute("SELECT ad, soyad FROM ogrenciler ORDER BY soyad ASC")
    yazdir("ORDER BY soyad ASC (alfabetik)", cur.fetchall(), ["ad","soyad"])

    # ── 7. GROUP BY + COUNT ───────────────────────
    cur.execute("SELECT bolum, COUNT(*) as sayi, ROUND(AVG(gpa),2) as ort_gpa FROM ogrenciler GROUP BY bolum ORDER BY sayi DESC")
    yazdir("GROUP BY bolum — bölüm istatistikleri", cur.fetchall(), ["bolum","sayi","ort_gpa"])

    # ── 8. INNER JOIN ─────────────────────────────
    cur.execute("""
        SELECT o.ad, o.soyad, n.ders, n.not_degeri
        FROM ogrenciler o
        INNER JOIN notlar n ON o.id = n.ogrenci_id
        ORDER BY o.ad, n.ders
    """)
    yazdir("INNER JOIN — öğrenci notları", cur.fetchall(), ["ad","soyad","ders","not"])

    # ── 9. Alt sorgu (Subquery) ───────────────────
    cur.execute("""
        SELECT ad, gpa FROM ogrenciler
        WHERE gpa > (SELECT AVG(gpa) FROM ogrenciler)
        ORDER BY gpa DESC
    """)
    yazdir("Subquery — GPA ortalamanın üstündekiler", cur.fetchall(), ["ad","gpa"])

print("\n  Kullanılan SQL Anahtar Kelimeleri:")
print("  WHERE, AND, OR, BETWEEN, LIKE, IN, ORDER BY, ASC, DESC")
print("  LIMIT, GROUP BY, COUNT, AVG, INNER JOIN, Subquery")
