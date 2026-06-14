# 🤖 DIKO BATCH PROCESSING GUIDE - UPDATED v2

**Updated:** 2026-06-14
**Status:** ✅ Includes ZIP/RAR extraction
**Files to Process:** 28 PDF checklists
**Time Estimate:** 15-20 minutes

---

## 📋 BATCH 1: BTP JAK (13 files)

### Step 1: Upload BTP JAK files

**Web App URL:** https://tester.sintelboo.my.id
**Format:** Select "BTP JAK (Format Standar)"
**Activity:** Select "Perawatan"

**Files to upload:**
1. ✓ 01-06-2026_PERAWATAN POINT LOCK-PERINTANG-PELALAU 2 MINGGUAN_Bogor.pdf
2. ✓ 01-06-2026_PERAWATAN WESEL ELEKTRIK 2 MINGGUAN_Bogor.pdf
3. ✓ 01-06-2026_PERAWATAN WESEL ELEKTRIK 2 MINGGUAN_Bogor_1.pdf
4. ✓ 02-06-2026_PERAWATAN WESEL ELEKTRIK 2 MINGGUAN_Bogor.pdf
5. ✓ 02-06-2026_PERAWATAN WESEL ELEKTRIK 2 MINGGUAN_Bogor_1.pdf
6. ✓ 03-06-2026_PERAWATAN CATU DAYA 1 BULANAN_Cilebut.pdf
7. ✓ 03-06-2026_PERAWATAN PERALATAN DALAM PERSINYALAN ELEKTRIK 1 BULANAN_Cilebut.pdf
8. ✓ 03-06-2026_PERAWATAN PERALATAN TELEKOMUNIKASI DI STASIUN 1 BULANAN_Cilebut.pdf
9. ✓ 03-06-2026_PERAWATAN PERALATAN TELEKOMUNIKASI DI STASIUN 1 BULANAN_Cilebut_1.pdf
10. ✓ 03-06-2026_PERAWATAN SERAT OPTIK 1 BULANAN_Cilebut.pdf
11. ✓ 03-06-2026_PERAWATAN SERAT OPTIK 1 BULANAN_Cilebut_1.pdf
12. ✓ 03-06-2026_PERAWATAN WESEL ELEKTRIK 2 MINGGUAN_Cilebut.pdf
13. ✓ 12-06-2026_PERAWATAN SERAT OPTIK 1 BULANAN_Bogor.pdf

### Step 2: Download & Extract Batch 1

1. Wait for web app to process (3-5 minutes)
2. Click "Download" button
3. File will be: `hasil_download.zip` or `hasil_download.rar`
4. Save to: `C:\Users\SINTEL 1.21 BOO\Downloads\6. JUNI\hasil download\BTP JAK\`
5. **DO NOT extract manually** - Script will do it

---

## 📋 BATCH 2: BTP BD (15 files)

### Step 1: Upload BTP BD files

**Format:** Select "BTP BD (Format Khusus Sintel Boo)"
**Activity:** Select "Perawatan"

**Files to upload:**
1. ✓ 11-06-2026_PERAWATAN PERALATAN PINTU PERLINTASAN 1 BULANAN_Bogor-Batutulis.pdf
2. ✓ 11-06-2026_PERAWATAN PERALATAN TELEKOMUNIKASI DI PINTU PERLINTASAN 1 BULANAN_Bogor-Batutulis.pdf
3. ✓ 11-06-2026_PERAWATAN PERALATAN TELEKOMUNIKASI DI PINTU PERLINTASAN 1 BULANAN_Bogorpaledang-Batutulis.pdf
4. ✓ 12-06-2026_PERAWATAN AXLE COUNTER FRAUSCHER 1 BULANAN_Bogorpaledang.pdf
5. ✓ 12-06-2026_PERAWATAN AXLE COUNTER FRAUSCHER 1 BULANAN_Bogorpaledang_1.pdf
6. ✓ 12-06-2026_PERAWATAN CATU DAYA 1 BULANAN_Bogorpaledang.pdf
7. ✓ 12-06-2026_PERAWATAN PERAGA SINYAL ELEKTRIK 1 BULANAN_Bogorpaledang.pdf
8. ✓ 12-06-2026_PERAWATAN PERAGA SINYAL ELEKTRIK 1 BULANAN_Bogorpaledang_1.pdf
9. ✓ 12-06-2026_PERAWATAN PERALATAN DALAM PERSINYALAN ELEKTRIK 1 BULANAN_Bogorpaledang.pdf
10. ✓ 12-06-2026_PERAWATAN PERALATAN PINTU PERLINTASAN 1 BULANAN_Bogorpaledang.pdf
11. ✓ 12-06-2026_PERAWATAN PERALATAN TELEKOMUNIKASI DI LUAR STASIUN 1 BULANAN_Bogorpaledang.pdf
12. ✓ 12-06-2026_PERAWATAN PERALATAN TELEKOMUNIKASI DI PINTU PERLINTASAN 1 BULANAN_Bogor-Batutulis.pdf
13. ✓ 12-06-2026_PERAWATAN PERALATAN TELEKOMUNIKASI DI PINTU PERLINTASAN 1 BULANAN_Bogorpaledang.pdf
14. ✓ 12-06-2026_PERAWATAN PERALATAN TELEKOMUNIKASI DI STASIUN 1 BULANAN_Bogorpaledang.pdf
15. ✓ 12-06-2026_PERAWATAN SERAT OPTIK 1 BULANAN_Bogorpaledang.pdf

### Step 2: Download & Extract Batch 2

1. Wait for web app to process (3-5 minutes)
2. Click "Download" button
3. File will be: `hasil_download.zip` or `hasil_download.rar`
4. Save to: `C:\Users\SINTEL 1.21 BOO\Downloads\6. JUNI\hasil download\BTP BD\`
5. **DO NOT extract manually** - Script will do it

---

## 🔧 STEP 3: AUTO-EXTRACT & ORGANIZE (Most Important!)

**After BOTH batches downloaded:**

### Run the organizer script:

```bash
cd "C:\Users\SINTEL 1.21 BOO\Downloads\6. JUNI"
python3 organize_files.py
```

### What the script does:

1. ✅ **Finds ZIP/RAR files** in hasil download/BTP JAK/ and BTP BD/
2. ✅ **Extracts all archives** automatically
3. ✅ **Deletes ZIP/RAR files** after successful extraction
4. ✅ **Organizes PDFs** by asset type
5. ✅ **Creates subfolders** for each asset type
6. ✅ **Reports progress** as it works

### Example output:

```
🤖 DIKO File Organizer v2.0
======================================================================
🔍 Phase 1: Scanning for ZIP/RAR archives...
======================================================================

📁 Processing BTP JAK:
   📦 Found ZIP: hasil_download.zip
   ✅ Extracted: hasil_download.zip
   🗑️  Deleted: hasil_download.zip

📁 Processing BTP BD:
   📦 Found RAR: hasil_download.rar
   ✅ Extracted: hasil_download.rar
   🗑️  Deleted: hasil_download.rar

======================================================================
🔍 Phase 2: Organizing extracted files...
======================================================================

📁 Organizing BTP JAK:
   ✅ File1.pdf → Wesel/
   ✅ File2.pdf → Serat Optik/
   ✅ File3.pdf → PTDS/
   📊 Organized 13 files in BTP JAK

📁 Organizing BTP BD:
   ✅ File1.pdf → Axle Counter/
   ✅ File2.pdf → PTPP/
   ✅ File3.pdf → Pintu Perlintasan/
   📊 Organized 15 files in BTP BD

======================================================================
✅ Organization complete!
======================================================================
```

---

## 📁 EXPECTED FOLDER STRUCTURE

### After organize_files.py completes:

```
hasil download/
│
├── BTP JAK/
│   ├── Wesel/ (5 files)
│   ├── Catu Daya/ (1 file)
│   ├── PDSE/ (1 file)
│   ├── Peraga Sinyal Elektrik/ (1 file)
│   ├── PTDS/ (2 files)
│   └── Serat Optik/ (3 files)
│
└── BTP BD/
    ├── Axle Counter/ (2 files)
    ├── Pintu Perlintasan/ (2 files)
    ├── PTPP/ (4 files)
    ├── Serat Optik/ (1 file)
    ├── PTLS/ (1 file)
    ├── PTDS/ (1 file)
    ├── Peraga Sinyal Elektrik/ (2 files)
    ├── Catu Daya/ (1 file)
    └── PDSE/ (1 file)
```

**No ZIP/RAR files remaining** - all extracted and cleaned up!

---

## ✅ STEP-BY-STEP CHECKLIST

### Before Upload
- [ ] Read this guide completely
- [ ] Open web app: https://tester.sintelboo.my.id
- [ ] Confirm activity type: "Perawatan"
- [ ] Have folder ready: C:\Users\SINTEL 1.21 BOO\Downloads\6. JUNI\hasil download\

### Batch 1 Upload
- [ ] Select format: "BTP JAK (Format Standar)"
- [ ] Select activity: "Perawatan"
- [ ] Upload 13 files
- [ ] Wait for processing (3-5 min)
- [ ] Download ZIP/RAR
- [ ] Save to: hasil download\BTP JAK\
- [ ] **DO NOT extract - script will do it**

### Batch 2 Upload
- [ ] Select format: "BTP BD (Format Khusus Sintel Boo)"
- [ ] Select activity: "Perawatan"
- [ ] Upload 15 files
- [ ] Wait for processing (3-5 min)
- [ ] Download ZIP/RAR
- [ ] Save to: hasil download\BTP BD\
- [ ] **DO NOT extract - script will do it**

### Auto-Organize
- [ ] Open terminal/command prompt
- [ ] Navigate to: C:\Users\SINTEL 1.21 BOO\Downloads\6. JUNI\
- [ ] Run: `python3 organize_files.py`
- [ ] Wait for completion (1-2 min)
- [ ] Verify folder structure created
- [ ] Check all 28 files organized
- [ ] Confirm no ZIP/RAR files remaining

### Verification
- [ ] Total files: 28
- [ ] BTP JAK folder: 13 files
- [ ] BTP BD folder: 15 files
- [ ] All files in correct asset subfolders
- [ ] No files in root directories
- [ ] All ZIP/RAR cleaned up

---

## 💡 IMPORTANT NOTES

✅ **DO NOT manually extract ZIP/RAR files**
- The script does it automatically
- It also cleans up archive files

✅ **Save downloads to correct folders**
- BTP JAK downloads → hasil download\BTP JAK\
- BTP BD downloads → hasil download\BTP BD\

✅ **Run script only AFTER both batches downloaded**
- Process both uploads first
- Then run organize_files.py once

✅ **Script handles both ZIP and RAR**
- Automatic format detection
- Extracts both types seamlessly

---

## 🔧 TROUBLESHOOTING

**Script can't find files?**
- Verify files saved to: hasil download\BTP JAK\ or BTP BD\
- Check file extensions (.zip or .rar)
- Run script from correct directory

**RAR extraction fails?**
- Install 7z: `choco install 7zip` (Windows)
- Or install WinRAR
- Script will try both automatically

**Files not organized?**
- Check that PDFs were extracted
- Verify ZIP/RAR files present
- Re-run script: `python3 organize_files.py`

**Need to cleanup manually?**
```bash
# Remove all ZIP/RAR files
rm "hasil download/BTP JAK/"*.zip "hasil download/BTP JAK/"*.rar
rm "hasil download/BTP BD/"*.zip "hasil download/BTP BD/"*.rar

# Then run organizer
python3 organize_files.py
```

---

## ⏱️ TIME BREAKDOWN

| Phase | Time |
|-------|------|
| Batch 1 Upload | 3-5 min |
| Batch 1 Download | 1 min |
| Batch 2 Upload | 3-5 min |
| Batch 2 Download | 1 min |
| Auto-Organize | 1-2 min |
| **Total** | **~15-20 min** |

---

**Ready to start? Follow the checklist above!** 🚀

All steps are simple and the script handles the complex work automatically.
