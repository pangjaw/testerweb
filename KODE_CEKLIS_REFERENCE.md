# 📋 DAFTAR LENGKAP KODE CEKLIS - app.py

## Summary
Total: **9 jenis ceklis** dengan **8 kode unik**

---

## Tabel Lengkap

| No | Jenis Ceklis | Kode | Kategori | Deteksi Keyword | Asset Type |
|----|--------------|------|----------|-----------------|------------|
| 1 | WESEL / POINT LOCK | **BPBYE1** | WESEL | "POINT LOCK" atau "PENGAMAN WESEL" | W-series (W23A, W61A1, dll) |
| 2 | PDSE | **BPBYE2** | PDSE | "PERALATAN DALAM PERSINYALAN ELEKTRIK" | Lokasi saja |
| 3 | SERAT OPTIK + JPL | **BPBKF4** | SERAT OPTIK | "SERAT OPTIK" + "JPL" | JPL number + Lokasi |
| 4 | TELKOM DI PINTU PERLINTASAN | **BPBKS18** | PTPP | "TELEKOMUNIKASI DI PINTU PERLINTASAN" | JPL number + Lokasi |
| 5 | PINTU PERLINTASAN | **BPBKS17** | PINTU PERLINTASAN | "PINTU PERLINTASAN" (exclude TELKOM) | JPL number + Lokasi |
| 6 | TELKOM DI STASIUN | **BPBKS15** | PTDS | "TELEKOMUNIKASI DI STASIUN" | Lokasi saja |
| 7 | TELKOM DI LUAR STASIUN | **BPBKS16** | PTLS | "TELEKOMUNIKASI DI LUAR STASIUN" | Lokasi saja |
| 8 | CATU DAYA | **BPBYE14** | CATU DAYA | "CATU DAYA" | Lokasi saja |
| 9 | SERAT OPTIK (tanpa JPL) | **BPBKF4** | SERAT OPTIK | "SERAT OPTIK" (exclude "JPL") | Lokasi saja |

---

## Kode Breakdown

### BPBYE Series (Peralatan Utama)
- **BPBYE1** = WESEL (Pengaman Wesel / Point Lock)
- **BPBYE2** = PDSE (Peralatan Dalam Persinyalan Elektrik)
- **BPBYE3** = SINYAL (Peraga Sinyal Elektrik) *[jika ada di Gerbang B]*
- **BPBYE7** = AXC (Axle Counter) *[jika ada di Gerbang B]*
- **BPBYE14** = CATU DAYA (Power Supply)

### BPBKS Series (Telekomunikasi & Infrastruktur)
- **BPBKS15** = PTDS (Telkom Stasiun)
- **BPBKS16** = PTLS (Telkom Luar Stasiun) ⭐ NEW
- **BPBKS17** = PINTU PERLINTASAN (Level Crossing Gate)
- **BPBKS18** = PTPP (Telkom Di Pintu Perlintasan) ⭐ NEW

### BPBKF Series (Fiber Optik)
- **BPBKF4** = SERAT OPTIK (Fiber Optic - dengan atau tanpa JPL)

---

## Catatan Penting

### Kode BARU (dari update 2026-06-14)
- ⭐ **BPBKS16** - TELKOM LUAR STASIUN (PTLS)
- ⭐ **BPBKS18** - TELKOM DI PINTU PERLINTASAN (PTPP)

### Asset Type Rules
- **Dengan Asset Number:** WESEL, SERAT OPTIK+JPL, PINTU PERLINTASAN, TELKOM PINTU
  - Format: `[TYPE] [NAME] [NUMBER] [LOCATION]`
  - Contoh: `WESEL W23A BOO`, `SERAT OPTIK JPL 04 BOO-BOP`

- **Tanpa Asset Number:** PDSE, TELKOM STASIUN, TELKOM LUAR STASIUN, CATU DAYA, SERAT OPTIK (tanpa JPL)
  - Format: `[TYPE] [LOCATION]`
  - Contoh: `PDSE CLT`, `PTLS BOP`

### Deteksi Priority (Spesifik → Generic)
1. POINT LOCK
2. PDSE
3. SERAT OPTIK + JPL ⭐ (spesifik)
4. TELKOM DI PINTU ⭐ (spesifik)
5. PINTU PERLINTASAN (generic)
6. TELKOM STASIUN
7. TELKOM LUAR STASIUN ⭐ (generic)
8. CATU DAYA
9. SERAT OPTIK (tanpa JPL) (generic)

---

## Lokasi Kode di app.py

| Kode | Line | Section |
|------|------|---------|
| BPBYE1 | 153 | WESEL Detection |
| BPBYE2 | 165 | PDSE Detection |
| BPBKF4 | 183, 322 | SERAT OPTIK Detection (2x: +JPL dan -JPL) |
| BPBKS18 | 210 | TELKOM DI PINTU Detection |
| BPBKS17 | 239 | PINTU PERLINTASAN Detection |
| BPBKS15 | 268 | TELKOM STASIUN Detection |
| BPBKS16 | 286 | TELKOM LUAR STASIUN Detection |
| BPBYE14 | 304 | CATU DAYA Detection |

---

**Last Updated:** 2026-06-14
**App Version:** Latest (commit 7911ad0)
