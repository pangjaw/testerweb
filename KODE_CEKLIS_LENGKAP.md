# 📋 DAFTAR LENGKAP KODE CEKLIS app.py - GERBANG A & B

## Summary
**Total: 9 jenis ceklis yang dikonfigurasi**
- **GERBANG A:** 9 jenis (Dokumen Spesial - OCR-based detection)
- **GERBANG B:** 4 jenis (Multi-aset - Filename-based detection)

---

## GERBANG A - DOKUMEN SPESIAL (OCR-Based Detection)

| No | Jenis | Kode | Kategori | Deteksi Keyword | Asset Format | Line |
|----|-------|------|----------|-----------------|--------------|------|
| 1 | WESEL / POINT LOCK | **BPBYE1** | WESEL | "POINT LOCK" OR "PENGAMAN WESEL" | W-series (W23A, W61A1) | 153 |
| 2 | PDSE | **BPBYE2** | PDSE | "PERALATAN DALAM PERSINYALAN ELEKTRIK" | Lokasi only | 165 |
| 3 | SERAT OPTIK + JPL | **BPBKF4** | SERAT OPTIK | "SERAT OPTIK" + "JPL" | JPL [NUM] + Lokasi | 183 |
| 4 | TELKOM DI PINTU PERLINTASAN ⭐ | **BPBKS18** | PTPP | "TELEKOMUNIKASI DI PINTU PERLINTASAN" | JPL [NUM] + Lokasi | 210 |
| 5 | PINTU PERLINTASAN | **BPBKS17** | PINTU PERLINTASAN | "PINTU PERLINTASAN" (exclude TELKOM) | JPL [NUM] + Lokasi | 239 |
| 6 | TELKOM DI STASIUN | **BPBKS15** | PTDS | "TELEKOMUNIKASI DI STASIUN" | Lokasi only | 268 |
| 7 | TELKOM DI LUAR STASIUN ⭐ | **BPBKS16** | PTLS | "TELEKOMUNIKASI DI LUAR STASIUN" | Lokasi only | 286 |
| 8 | CATU DAYA | **BPBYE14** | CATU DAYA | "CATU DAYA" | Lokasi only | 304 |
| 9 | SERAT OPTIK (tanpa JPL) | **BPBKF4** | SERAT OPTIK | "SERAT OPTIK" (exclude "JPL") | Lokasi only | 322 |

**Detection Priority (Spesifik → Generic):**
1. POINT LOCK (line 149)
2. PDSE (line 160)
3. SERAT OPTIK + JPL (line 179) ⭐
4. TELKOM DI PINTU (line 206) ⭐
5. PINTU PERLINTASAN (line 235)
6. TELKOM STASIUN (line 264)
7. TELKOM LUAR STASIUN (line 282) ⭐
8. CATU DAYA (line 300)
9. SERAT OPTIK tanpa JPL (line 318)

---

## GERBANG B - DOKUMEN MULTI-ASET (Filename-Based Detection)

| No | Jenis | Kode | Kategori | Deteksi Keyword (filename) | Asset Format | Line |
|----|-------|------|----------|---------------------------|--------------|------|
| 1 | WESEL | **BPBYE1** | WESEL | "WESEL" OR "WLSE" | W-series | 342 |
| 2 | AXLE COUNTER | **BPBYE7** | AXC | "AXLE" OR "COUNTER" OR "AXL" | ZP-series | 344 |
| 3 | SERAT OPTIK | **BPBKF4** | SERAT OPTIK | "SERAT OPTIK" OR "SO" | JPL [NUM] + Lokasi | 346 |
| 4 | SINYAL | **BPBYE3** | SINYAL | "SINYAL" OR "BLOK" OR "ZP" | JL/L-series | 348 |

**Detection Condition:** Line 340 → `if not is_special_doc:` (Gerbang A tidak match)

---

## RINGKASAN KODE CEKLIS

### BPBYE Series (Peralatan Utama)
```
BPBYE1  = WESEL / POINT LOCK
BPBYE2  = PDSE (Peralatan Dalam Persinyalan Elektrik)
BPBYE3  = SINYAL (Peraga Sinyal Elektrik)
BPBYE7  = AXC (Axle Counter)
BPBYE14 = CATU DAYA (Power Supply)
```

### BPBKS Series (Telekomunikasi & Infrastruktur)
```
BPBKS15 = PTDS (Telkom Di Stasiun)
BPBKS16 = PTLS (Telkom Di Luar Stasiun) ⭐ NEW
BPBKS17 = PINTU PERLINTASAN (Level Crossing Gate)
BPBKS18 = PTPP (Telkom Di Pintu Perlintasan) ⭐ NEW
```

### BPBKF Series (Fiber Optik)
```
BPBKF4  = SERAT OPTIK (Fiber Optic ± JPL)
```

---

## Kode BARU (Update 2026-06-14)

⭐ **BPBKS16** - TELKOM LUAR STASIUN (PTLS)
- Deteksi: "TELEKOMUNIKASI DI LUAR STASIUN"
- Line: 282-299

⭐ **BPBKS18** - TELKOM DI PINTU PERLINTASAN (PTPP)
- Deteksi: "TELEKOMUNIKASI DI PINTU PERLINTASAN"
- Line: 206-233

---

## Output Format Examples

### GERBANG A (BTP BD Format - Sintel Boo)
```
2026-6_Resor 1.21 Boo_{KODE}_{JENIS}_{IDENTITAS}_{TANGGAL}.pdf
```

Contoh:
- `2026-6_Resor 1.21 Boo_BPBYE1_Perawatan_WESEL W23A BOO_03-06-2026.pdf`
- `2026-6_Resor 1.21 Boo_BPBKF4_Perawatan_SERAT OPTIK JPL 04 BOO-BOP_12-06-2026.pdf`
- `2026-6_Resor 1.21 Boo_BPBKS18_Perawatan_PTPP JPL_11-06-2026.pdf`
- `2026-6_Resor 1.21 Boo_BPBKS16_Perawatan_PTLS BOP_12-06-2026.pdf`

### GERBANG B (BTP JAK Format - Standard)
```
{JENIS} {IDENTITAS} {TANGGAL}.pdf
```

Contoh:
- `PERAWATAN SINYAL JL66B BOP 12-06-2026.pdf`
- `PERAWATAN WESEL W23A BOO 03-06-2026.pdf`

---

## Asset ID Validation Rules

✅ **Valid Format:** `[NAME] [SPACE] [NUMBER]`
- Contoh: `W23A`, `JPL 04`, `ZP 68`, `JL66B`

❌ **Invalid Format:** `[GABUNG_LANGSUNG]` (system code)
- Contoh: `JPL10506`, `WSL11089`, `TRA11348`
- Action: **REJECT** (tidak di-extract sebagai aset number)

---

## Duplicate File Detection

**Logic:** Line 410-415
```python
if new_name not in unique_filenames:
    zip_f.writestr(new_name, f.getvalue())
    processed_files.append(new_name)
    unique_filenames.add(new_name)
else:
    duplicate_errors.append(f"⚠️ {f.name}: ID {aid_clean} duplikat.")
```

**Behavior:**
- File pertama dengan output nama tertentu → di-save ke ZIP
- File kedua dengan output nama sama → di-skip dengan warning

---

**Last Updated:** 2026-06-14
**App Version:** Latest (commit 7911ad0)
**Status:** Semua kode sudah dikonfigurasi dan tested ✅
