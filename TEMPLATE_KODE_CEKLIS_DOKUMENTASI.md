# 📋 TEMPLATE KODE CEKLIS - DOKUMENTASI

**Last Updated:** 2026-06-14
**App Version:** commit a914ba9
**Status:** ✅ Semua 38 kode ceklis sudah siap

---

## SUMMARY

| Series | Aktif | Template | Total |
|--------|-------|----------|-------|
| BPBYE | 5 | 10 | 15 |
| BPBKS | 3 | 14 | 17 |
| BPBKF | 1 | 5 | 6 |
| **TOTAL** | **9** | **29** | **38** |

---

## BPBYE SERIES (15 kode)

### ✅ AKTIF (5 kode)

```
BPBYE1  - Perawatan Wesel Elektrik 2 Mingguan
          Keyword: "POINT LOCK" OR "PENGAMAN WESEL"
          Extract: W-number (W23A, W61A1, etc)
          Status: ACTIVE

BPBYE2  - Perawatan Peralatan Dalam Persinyalan Elektrik 1 Bulanan
          Keyword: "PERALATAN DALAM PERSINYALAN ELEKTRIK"
          Extract: Lokasi only (BOO, BOP, CLT, dll)
          Status: ACTIVE

BPBYE3  - Perawatan Peraga Persinyalan Elektrik 1 Bulanan
          Keyword: "SINYAL" OR "BLOK" OR "ZP" (GERBANG B)
          Extract: JL-number or Z-number
          Status: ACTIVE (GERBANG B)

BPBYE7  - Perawatan Axle Counter Frauscher 1 Bulanan
          Keyword: "AXLE" OR "COUNTER" OR "AXL" (GERBANG B)
          Extract: ZP-number
          Status: ACTIVE (GERBANG B)

BPBYE14 - Perawatan Catu Daya 1 Bulanan
          Keyword: "CATU DAYA"
          Extract: Lokasi only
          Status: ACTIVE
```

### 📋 TEMPLATE (10 kode - Siap Diaktifkan)

```
BPBYE4  - Perawatan Peralatan CTC CTS 1 Bulanan
          Keyword: "CTC" OR "CTS"
          Line: app.py (commented, ready to uncomment)
          Status: TEMPLATE

BPBYE5  - Perawatan Axle Counter Siemens 1 Bulanan
          Keyword: "AXLE" AND "SIEMENS"
          Extract: ZP-number
          Status: TEMPLATE

BPBYE6  - Perawatan Axle Counter Altpro 1 Bulanan
          Keyword: "AXLE" AND "ALTPRO"
          Extract: ZP-number
          Status: TEMPLATE

BPBYE8  - Perawatan Axle Counter Thales 1 Bulanan
          Keyword: "AXLE" AND "THALES"
          Extract: ZP-number
          Status: TEMPLATE

BPBYE9  - Perawatan Axle Counter Esso-M 1 Bulanan
          Keyword: "AXLE" AND "ESSO"
          Extract: ZP-number
          Status: TEMPLATE

BPBYE10 - Perawatan Track Circuit 1 Bulanan
          Keyword: "TRACK CIRCUIT"
          Extract: Lokasi only
          Status: TEMPLATE

BPBYE11 - Perawatan Location Case 1 Bulanan
          Keyword: "LOCATION CASE"
          Extract: Lokasi only
          Status: TEMPLATE

BPBYE12 - Perawatan Point Lock Perintang Pelalau 2 Mingguan
          Keyword: "POINT LOCK" AND "PELALAU"
          Extract: Asset-number + Lokasi
          Status: TEMPLATE
          Note: Hati-hati overlap dengan BPBYE1

BPBYE13 - Perawatan Peralatan Pintu Perlintasan 1 Bulanan
          Keyword: "PERALATAN PINTU PERLINTASAN"
          Extract: Lokasi only
          Status: TEMPLATE
          Note: Hati-hati overlap dengan BPBKS17

BPBYE15 - Perawatan Wesel Terlayan Setempat Elektrik 1 Bulanan
          Keyword: "WESEL" AND "TERLAYAN SETEMPAT"
          Extract: W-number + Lokasi
          Status: TEMPLATE
```

---

## BPBKS SERIES (17 kode)

### ✅ AKTIF (3 kode)

```
BPBKS15 - Perawatan Peralatan Telekomunikasi di Stasiun 1 Bulanan
          Keyword: "TELEKOMUNIKASI DI STASIUN"
          Extract: Lokasi only
          Status: ACTIVE

BPBKS16 - Perawatan Peralatan Telekomunikasi di Luar Stasiun 1 Bulanan
          Keyword: "TELEKOMUNIKASI DI LUAR STASIUN"
          Extract: Lokasi only
          Status: ACTIVE

BPBKS17 - Perawatan Peralatan Telekomunikasi di Pintu Perlintasan 1 Bulanan
          Keyword: "TELEKOMUNIKASI DI PINTU PERLINTASAN"
          Extract: JPL-number + Lokasi
          Status: ACTIVE
          Note: Sebelumnya BPBKS18, diperbaiki 2026-06-14
```

### 📋 TEMPLATE (14 kode - Siap Diaktifkan)

```
BPBKS1  - Perawatan Peralatan Radio Lokomotif Harian
          Keyword: "RADIO LOKOMOTIF" AND "HARIAN"
          Status: TEMPLATE

BPBKS2  - Perawatan Peralatan Radio Lokomotif 3 Bulanan
          Keyword: "RADIO LOKOMOTIF" AND "3 BULANAN"
          Status: TEMPLATE

BPBKS3  - Perawatan Peralatan Radio Lokomotif 1 Tahunan
          Keyword: "RADIO LOKOMOTIF" AND "TAHUNAN"
          Status: TEMPLATE

BPBKS4  - Perawatan Peralatan Radio Way Station 3 Bulanan
          Keyword: "RADIO" AND "WAY STATION"
          Status: TEMPLATE

BPBKS5  - Perawatan Peralatan Sistem Waystation 1 Tahunan
          Keyword: "SISTEM WAYSTATION" AND "TAHUNAN"
          Status: TEMPLATE

BPBKS6  - Perawatan Peralatan Pusat Kendali (PK) Analog 6 Bulanan
          Keyword: "PUSAT KENDALI" AND "ANALOG"
          Status: TEMPLATE

BPBKS7  - Perawatan Peralatan Radio Waystation Digital 3 Bulanan
          Keyword: "WAYSTATION DIGITAL"
          Status: TEMPLATE

BPBKS8  - Perawatan Peralatan Pusat Kendali (PK) Digital 1 Tahunan
          Keyword: "PUSAT KENDALI" AND "DIGITAL"
          Status: TEMPLATE

BPBKS9  - Perawatan Peralatan Radio Lokomotif Tait Harian
          Keyword: "RADIO LOKOMOTIF TAIT" AND "HARIAN"
          Status: TEMPLATE

BPBKS10 - Perawatan Peralatan Radio Lokomotif Tait 3 Bulanan
          Keyword: "RADIO LOKOMOTIF TAIT" AND "3 BULANAN"
          Status: TEMPLATE

BPBKS11 - Perawatan Peralatan Radio Lokomotif Tait 1 Tahunan
          Keyword: "RADIO LOKOMOTIF TAIT" AND "TAHUNAN"
          Status: TEMPLATE

BPBKS12 - Perawatan Peralatan Radio Waystation Tait 3 Bulanan
          Keyword: "RADIO WAYSTATION TAIT"
          Status: TEMPLATE

BPBKS13 - Perawatan Peralatan Sistem Waystation Tait 1 Tahunan
          Keyword: "SISTEM WAYSTATION TAIT"
          Status: TEMPLATE

BPBKS14 - Perawatan Peralatan Pusat Kendali (PK) Tait 3 Bulanan
          Keyword: "PUSAT KENDALI" AND "TAIT"
          Status: TEMPLATE
```

---

## BPBKF SERIES (6 kode)

### ✅ AKTIF (1 kode)

```
BPBKF4  - Perawatan Serat Optik 1 Bulanan
          Keyword: "SERAT OPTIK" (with or without JPL)
          Extract: JPL-number + Lokasi (jika ada)
          Status: ACTIVE
```

### 📋 TEMPLATE (5 kode - Siap Diaktifkan)

```
BPBKF1  - Perawatan Peralatan Radio Basestation 6 Bulanan
          Keyword: "RADIO BASESTATION" (not TAIT, not DIGITAL)
          Status: TEMPLATE

BPBKF2  - Perawatan Peralatan Radio Basestation Digital 6 Bulanan
          Keyword: "RADIO BASESTATION" AND "DIGITAL"
          Status: TEMPLATE

BPBKF3  - Perawatan Peralatan Radio Basestation Tait 6 Bulanan
          Keyword: "RADIO BASESTATION" AND "TAIT"
          Status: TEMPLATE

BPBKF5  - Perawatan Saluran Blok 1 Bulanan
          Keyword: "SALURAN BLOK" (not "6 BULANAN")
          Status: TEMPLATE

BPBKF6  - Perawatan Saluran Blok 6 Bulanan
          Keyword: "SALURAN BLOK" AND "6 BULANAN"
          Status: TEMPLATE
```

---

## CARA MENGAKTIFKAN TEMPLATE

### Langkah 1: Identifikasi dokumen baru
Ketika ada dokumen ceklis jenis baru yang akan diproses.

### Langkah 2: Temukan template di app.py
Cari kode ceklis yang sesuai di bagian:
```
# ====================================================
# TEMPLATE KODE CEKLIS TAMBAHAN (READY FOR FUTURE USE)
# ====================================================
```

### Langkah 3: Uncomment dan sesuaikan
- Hilangkan `#` di awal baris
- Sesuaikan `keyword` dengan konten OCR dokumen
- Sesuaikan `extract logic` jika diperlukan

### Langkah 4: Test lokal
- Upload dokumen test
- Verifikasi output naming

### Langkah 5: Commit & Push
```bash
git add app.py
git commit -m "feat: Activate BPBKS1 (Radio Lokomotif) detection"
git push
```

---

## PRIORITAS DETEKSI (PENTING!)

Urutan pengecekan sudah diatur dari **spesifik → generic**:

1. POINT LOCK (BPBYE1)
2. PDSE (BPBYE2)
3. SERAT OPTIK + JPL (BPBKF4) ← spesifik
4. TELKOM DI PINTU (BPBKS17) ← spesifik
5. PINTU PERLINTASAN (generic)
6. TELKOM STASIUN (BPBKS15)
7. TELKOM LUAR STASIUN (BPBKS16) ← generic
8. CATU DAYA (BPBYE14)
9. SERAT OPTIK (tanpa JPL) (BPBKF4) ← generic

**Saat menambah template baru, perhatikan:**
- Jangan insert di tengah (akan break prioritas)
- Insert sebelum GERBANG B
- Ikuti urutan spesifik → generic

---

## CHECKLIST UNTUK MAINTENANCE

- [ ] Template kode ceklis sudah di-review sesuai Cloud KAI
- [ ] Keyword detection sudah validated
- [ ] Asset extraction logic sudah ditest
- [ ] Tidak ada overlap dengan kode lain
- [ ] Dokumentasi sudah update
- [ ] Backup app.py sudah dibuat

---

**Notes:**
- Semua 38 kode ceklis SUDAH TERDAFTAR di app.py
- 9 kode sudah AKTIF dan tested
- 29 kode TEMPLATE siap di-uncomment
- Webhook sudah aktif untuk auto-deploy
- Setiap penambahan template baru hanya perlu uncomment + test

---

**Kontribusi dari Cloud KAI:**
https://cloud.kai.id/s/m52fHjPzkxLrZwE?dir=/1.%20STL/2.%20BPBYE
