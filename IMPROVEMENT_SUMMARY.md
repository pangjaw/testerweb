# Perbaikan App.py - Summary untuk Konfirmasi

## Status: SIAP UNTUK REVIEW & APPROVAL

---

## 🎯 Masalah yang Diperbaiki

### 1. TELKOM LUAR STASIUN (PTLS) - TIDAK TERDETEKSI
**Before:**
- Tidak ada di Gerbang A, hanya TELKOM STASIUN yang tersedia
- File TELKOM LUAR STASIUN akan hilang atau salah match

**After:**
- ✅ Ditambahkan deteksi TELKOM LUAR STASIUN
- ✅ Output: `2026-6_Resor 1.21 Boo_BPBKS16_Perawatan_PTLS BOP_12-06-2026.pdf`

---

### 2. TELKOM DI PINTU PERLINTASAN (PTPP) - BINGUNG DENGAN PINTU GENERIC
**Before:**
- Ada "TELEKOMUNIKASI DI PINTU PERLINTASAN" + "PINTU PERLINTASAN" + JPL
- Script tidak bisa bedakan mana yang diprioritaskan
- Hasil: Salah match atau kabur ke PINTU PERLINTASAN generic

**After:**
- ✅ Deteksi TELKOM DI PINTU diletakkan SEBELUM PINTU generic (prioritas)
- ✅ Kode baru: BPBKS18 (Telkom Pintu Perlintasan)
- ✅ Output: `2026-6_Resor 1.21 Boo_BPBKS18_Perawatan_PTPP JPL_11-06-2026.pdf`

**Note:** JPL number belum terextract optimal pada test ini (lihat section Findings)

---

### 3. SERAT OPTIK - TIDAK BERMASALAH SAAT INI
- Belum ada file test SERAT OPTIK + JPL di folder
- Logic sudah siap dengan exclude PINTU PERLINTASAN
- Akan output: `SERAT OPTIK JPL [NUM] [LOC]`

---

## 📋 Perubahan yang Diusulkan

### A. Urutan Deteksi (Gerbang A) - LIHAT BARIS ~143

**CURRENT ORDER:**
1. POINT LOCK
2. PDSE
3. TELKOM (STASIUN only)
4. PINTU PERLINTASAN
5. CATU DAYA
6. SERAT OPTIK (tanpa JPL)

**NEW ORDER (RECOMMENDED):**
1. POINT LOCK
2. PDSE
3. **TELKOM DI PINTU PERLINTASAN** ← NEW, PRIORITAS TINGGI
4. PINTU PERLINTASAN ← GENERIC, setelah TELKOM check
5. CATU DAYA
6. SERAT OPTIK ← Exclude PINTU PERLINTASAN
7. TELKOM STASIUN
8. **TELKOM LUAR STASIUN** ← NEW

---

### B. Kode Ceklis Baru

| Jenis | Kode Lama | Kode Baru | Catatan |
|-------|-----------|-----------|---------|
| TELKOM STASIUN | BPBKS15 | BPBKS15 | Tetap |
| TELKOM LUAR STASIUN | - | BPBKS16 | **BARU** |
| **TELKOM DI PINTU** | - | BPBKS18 | **BARU** |
| PINTU PERLINTASAN | BPBKS17 | BPBKS17 | Tetap |

---

### C. Logic Changes (Pseudocode)

#### BEFORE (Baris ~147-194):
```python
elif "TELEKOMUNIKASI DI STASIUN" in text_flat or "TELEKOMUNIKASI DI LUAR STASIUN" in text_flat:
    is_ptds = "DI STASIUN" in text_flat
    target_keyword = "PTDS" if is_ptds else "PTLS"
    # ... tapi PTLS handling tidak sempurna
```

#### AFTER (PROPOSED):
```python
# Prioritas: Check TELKOM DI PINTU terlebih dahulu
elif "TELEKOMUNIKASI DI PINTU PERLINTASAN" in text_flat:
    is_special_doc = True
    target_keyword = "PTPP"
    kategori_nama = "PTPP"
    kode_ceklis = "BPBKS18"
    # Extract JPL seperti PINTU PERLINTASAN

# Kemudian PINTU PERLINTASAN GENERIC (tapi exclude TELKOM)
elif "PINTU PERLINTASAN" in text_flat and "TELEKOMUNIKASI" not in text_flat:
    # ... existing logic
    
# ... lalu TELKOM variants
elif "TELEKOMUNIKASI DI STASIUN" in text_flat:
    # PTDS
    
elif "TELEKOMUNIKASI DI LUAR STASIUN" in text_flat:
    # PTLS - NEW
```

---

## 🧪 Test Results

| Case | Input | Output | Status |
|------|-------|--------|--------|
| TELKOM LUAR STASIUN | `12-06-2026_...DI LUAR STASIUN...Bogorpaledang.pdf` | `2026-6_Resor 1.21 Boo_BPBKS16_Perawatan_PTLS BOP_12-06-2026.pdf` | ✅ OK |
| TELKOM DI PINTU | `11-06-2026_...DI PINTU PERLINTASAN...Bogor-Batutulis.pdf` | `2026-6_Resor 1.21 Boo_BPBKS18_Perawatan_PTPP JPL_11-06-2026.pdf` | ⚠️ JPL incomplete |
| PINTU PERLINTASAN | `11-06-2026_...PINTU PERLINTASAN...Bogor-Batutulis.pdf` | `2026-6_Resor 1.21 Boo_BPBKS17_Perawatan_PINTU PERLINTASAN JPL 07 BOP - BTT_11-06-2026.pdf` | ✅ OK |

---

## 🔍 Findings & Notes

1. **JPL Extraction di TELKOM PINTU** - Belum optimal
   - Regex: `JPL\s+(?:ELEKTRIK\s+)?(?:NO[\.\s]*)?([\d]+)` 
   - OCR text: `JPL10506 : GENTANIK JPL BNR BOP-BTT`
   - Issue: Angka 10506 tidak sesuai pola, coba perbaiki regex ke: `JPL\s*(\d+)`

2. **SERAT OPTIK dengan JPL** - Belum ditest
   - Perlu file sample `SERAT OPTIK` yang juga punya `JPL` di konten
   - Saat ini tidak ada di folder

3. **Konsistensi Naming** 
   - PTDS, PTLS, PTPP sekarang berbeda dari WESEL, CATU DAYA, SERAT OPTIK
   - Ini OK karena sesuai standard Sintelis

---

## ✅ Checklist Sebelum Implement

- [ ] Confirm urutan deteksi baru (Prioritas TELKOM PINTU sebelum PINTU GENERIC)
- [ ] Confirm kode ceklis baru: BPBKS16 (PTLS), BPBKS18 (PTPP)
- [ ] Fix JPL regex jika perlu (dari `([\d]+)` menjadi `(\d+)`)
- [ ] Test SERAT OPTIK + JPL setelah ada file sample
- [ ] Update app.py official (jangan preview)

---

## 📝 Implementation Notes

**File yang perlu diubah:**
- `app.py` - Gerbang A (baris ~143-263)

**Tidak perlu diubah:**
- Gerbang B (filename-based detection)
- Asset extraction logic (Gerbang B)
- Output formatting

**Backup sebelum update:**
- Simpan `app.py` original sebagai `app.py.backup.2026-06-14`

---

**Status:** Menunggu konfirmasi dari user untuk proceed dengan update app.py
