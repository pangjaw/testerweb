# ============================================================================
# IMPROVEMENT DRAFT - Perbaikan Deteksi Dokumen Spesial
# ============================================================================
# 
# MASALAH YANG DIPERBAIKI:
# 1. TELKOM LUAR STASIUN (PTLS) - belum ada di Gerbang A, hanya STASIUN
# 2. TELKOM DI PINTU PERLINTASAN (PTPP) - kebetulan sama dengan PINTU PERLINTASAN
#    karena ada JPL, script bingung memilih mana yang diprioritaskan
# 3. SERAT OPTIK + JPL - sama masalahnya, perlu prioritas yang jelas
#
# SOLUSI:
# - Ubah urutan deteksi dengan prioritas: 
#   TELKOM DI PINTU > PINTU PERLINTASAN
#   SERAT OPTIK NORMAL > (diabaikan jika SERAT OPTIK + JPL terdeteksi di Gerbang B)
# - Tambah deteksi TELKOM LUAR STASIUN
#
# ============================================================================

# GERBANG A - DOKUMEN SPESIAL (Updated Order & Logic)
# ============================================================================

DETECTION_ORDER = [
    # 1. POINT LOCK / PENGAMAN WESEL
    {
        "name": "POINT LOCK",
        "keywords": ["POINT LOCK", "PENGAMAN WESEL"],
        "target_keyword": "WESEL",
        "kategori_nama": "WESEL",
        "kode_ceklis": "BPBYE1",
        "extract_logic": "extract_wesel_id"
    },
    
    # 2. PDSE
    {
        "name": "PDSE",
        "keywords": ["PERALATAN DALAM PERSINYALAN ELEKTRIK"],
        "target_keyword": "PDSE",
        "kategori_nama": "PDSE",
        "kode_ceklis": "BPBYE2",
        "extract_logic": "extract_location_only"
    },
    
    # 3. TELKOM DI PINTU PERLINTASAN (PRIORITY: Check this BEFORE generic PINTU)
    {
        "name": "TELKOM DI PINTU PERLINTASAN",
        "keywords": ["TELEKOMUNIKASI DI PINTU PERLINTASAN"],
        "target_keyword": "PTPP",
        "kategori_nama": "PTPP",
        "kode_ceklis": "BPBKS18",  # Baru
        "extract_logic": "extract_jpl_for_telkom_pintu"
    },
    
    # 4. PINTU PERLINTASAN (GENERIC - after TELKOM check)
    {
        "name": "PINTU PERLINTASAN",
        "keywords": ["PINTU PERLINTASAN"],
        "exclude_keywords": ["TELEKOMUNIKASI"],  # Exclude TELKOM variant
        "target_keyword": "PINTU PERLINTASAN",
        "kategori_nama": "PINTU PERLINTASAN",
        "kode_ceklis": "BPBKS17",
        "extract_logic": "extract_jpl_for_pintu"
    },
    
    # 5. CATU DAYA
    {
        "name": "CATU DAYA",
        "keywords": ["CATU DAYA"],
        "target_keyword": "CATU DAYA",
        "kategori_nama": "CATU DAYA",
        "kode_ceklis": "BPBYE14",
        "extract_logic": "extract_location_only"
    },
    
    # 6. SERAT OPTIK (tanpa JPL di nama/konten spesifik pintu)
    {
        "name": "SERAT OPTIK",
        "keywords": ["SERAT OPTIK"],
        "exclude_keywords": ["PINTU PERLINTASAN"],  # Exclude PINTU variant
        "target_keyword": "SERAT OPTIK",
        "kategori_nama": "SERAT OPTIK",
        "kode_ceklis": "BPBKF4",
        "extract_logic": "extract_location_only"
    },
    
    # 7. TELKOM STASIUN
    {
        "name": "TELKOM STASIUN",
        "keywords": ["TELEKOMUNIKASI DI STASIUN"],
        "target_keyword": "PTDS",
        "kategori_nama": "PTDS",
        "kode_ceklis": "BPBKS15",
        "extract_logic": "extract_location_only"
    },
    
    # 8. TELKOM LUAR STASIUN (NEW)
    {
        "name": "TELKOM LUAR STASIUN",
        "keywords": ["TELEKOMUNIKASI DI LUAR STASIUN"],
        "target_keyword": "PTLS",
        "kategori_nama": "PTLS",
        "kode_ceklis": "BPBKS16",
        "extract_logic": "extract_location_only"
    },
]

# ============================================================================
# EXTRACTION LOGIC
# ============================================================================

def extract_wesel_id(text_flat, text_crop):
    """Extract W-aset from POINT LOCK"""
    import re
    w_match = re.search(r'(W\d+)', text_flat)
    aid = w_match.group(1) if w_match else "W_UNKNOWN"
    loc_id = "BOO" if "BOGOR" in text_flat else "LOKASI"
    return [{"id": aid, "loc": loc_id}]

def extract_location_only(text_flat, text_crop):
    """Extract location code only (no asset ID)"""
    loc_id = _extract_location(text_flat)
    return [{"id": "", "loc": loc_id}]

def extract_jpl_for_pintu(text_flat, text_crop):
    """Extract JPL untuk PINTU PERLINTASAN"""
    import re
    jpl_match = re.search(r'JPL\s+(?:ELEKTRIK\s+)?(?:NO[\.\s]*)?([\d]+)\b((?:\s*[A-Z\-]+)*)', text_flat)
    
    if jpl_match:
        angka_jpl = jpl_match.group(1).strip()
        lokasi_raw = jpl_match.group(2).strip() if jpl_match.group(2) else ""
        
        for stop_word in ["LOKASI", "TANGGAL", "DISETUJUI", "BOGOR"]:
            if stop_word in lokasi_raw:
                lokasi_raw = lokasi_raw.split(stop_word)[0]
        
        lokasi_clean = lokasi_raw.strip()
        lokasi_clean = re.sub(r'^-|-$', '', lokasi_clean).strip()
        
        aid = f"JPL {angka_jpl}"
        loc_id = lokasi_clean
    else:
        aid = "JPL"
        loc_id = ""
    
    return [{"id": aid, "loc": loc_id}]

def extract_jpl_for_telkom_pintu(text_flat, text_crop):
    """Extract JPL untuk TELKOM DI PINTU PERLINTASAN
    Output format: PTPP JPL 04 BOP-BTT atau PTPP JPL 07 BTT
    """
    import re
    jpl_match = re.search(r'JPL\s+(?:ELEKTRIK\s+)?(?:NO[\.\s]*)?([\d]+)\b((?:\s*[A-Z\-]+)*)', text_flat)
    
    if jpl_match:
        angka_jpl = jpl_match.group(1).strip()
        lokasi_raw = jpl_match.group(2).strip() if jpl_match.group(2) else ""
        
        for stop_word in ["LOKASI", "TANGGAL", "DISETUJUI", "BOGOR"]:
            if stop_word in lokasi_raw:
                lokasi_raw = lokasi_raw.split(stop_word)[0]
        
        lokasi_clean = lokasi_raw.strip()
        lokasi_clean = re.sub(r'^-|-$', '', lokasi_clean).strip()
        
        aid = f"JPL {angka_jpl}"
        loc_id = lokasi_clean
    else:
        aid = "JPL"
        loc_id = ""
    
    return [{"id": aid, "loc": loc_id}]

def _extract_location(text_flat):
    """Helper: Extract location code"""
    if "BOGORPALEDANG" in text_flat or "PALEDANG" in text_flat: 
        return "BOP"
    elif "BOGOR" in text_flat: 
        return "BOO"
    elif "CILEBUT" in text_flat: 
        return "CLT"
    elif "BATUTULIS" in text_flat: 
        return "BTT"
    elif "MASENG" in text_flat: 
        return "MSG"
    elif "CIOMAS" in text_flat: 
        return "COS"
    elif "CIGOMBONG" in text_flat: 
        return "CGB"
    else: 
        return "LOKASI"

# ============================================================================
# PSEUDOCODE: Implementasi di app.py
# ============================================================================
"""
# Ganti bagian ini di app.py (sekitar baris 143-263):

# ====================================================
# GERBANG A: DOKUMEN SPESIAL (Pencegatan 1 File Utuh)
# ====================================================

is_special_doc = False
target_keyword = None
kode_ceklis = ""
kategori_nama = ""
assets_found = []

# Iterasi detection order sesuai prioritas
for detection in DETECTION_ORDER:
    # Check if all keywords match
    if all(kw in text_flat for kw in detection["keywords"]):
        # Check if exclude keywords NOT match (untuk filtering)
        if "exclude_keywords" in detection:
            if any(ex_kw in text_flat for ex_kw in detection["exclude_keywords"]):
                continue  # Skip ini, coba detection berikutnya
        
        # Match! Extract data
        is_special_doc = True
        target_keyword = detection["target_keyword"]
        kategori_nama = detection["kategori_nama"]
        kode_ceklis = detection["kode_ceklis"]
        
        # Call extraction logic
        logic_func = globals()[detection["extract_logic"]]
        assets_found = logic_func(text_flat, text_crop)
        
        break  # Stop setelah match pertama
"""

# ============================================================================
# TESTING OUTPUT YANG DIHARAPKAN
# ============================================================================
"""
TELKOM LUAR STASIUN (PTLS):
   Input:  12-06-2026_PERAWATAN PERALATAN TELEKOMUNIKASI DI LUAR STASIUN 1 BULANAN_Bogorpaledang.pdf
   Output: 2026-6_Resor 1.21 Boo_BPBKS16_Perawatan_PTLS BOP_12-06-2026.pdf
   
TELKOM DI PINTU PERLINTASAN (PTPP):
   Input:  11-06-2026_PERAWATAN PERALATAN TELEKOMUNIKASI DI PINTU PERLINTASAN 1 BULANAN_Bogor-Batutulis.pdf
   Output: 2026-6_Resor 1.21 Boo_BPBKS18_Perawatan_PTPP JPL [NUMBER] [LOCATION]_11-06-2026.pdf
   
PINTU PERLINTASAN (GENERIC):
   Input:  11-06-2026_PERAWATAN PERALATAN PINTU PERLINTASAN 1 BULANAN_Bogor-Batutulis.pdf
   Output: 2026-6_Resor 1.21 Boo_BPBKS17_Perawatan_PINTU PERLINTASAN JPL [NUMBER] [LOCATION]_11-06-2026.pdf
"""
