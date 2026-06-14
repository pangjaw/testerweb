import streamlit as st
import json
import re
import os
import zipfile
import platform
import pytesseract
import gc
from io import BytesIO
from pdf2image import convert_from_bytes
from streamlit_lottie import st_lottie
from PIL import ImageOps

# --- 1. KONFIGURASI TESSERACT ---
if platform.system() == "Windows":
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
else:
    pytesseract.pytesseract.tesseract_cmd = 'tesseract'

def load_lottiefile(filepath: str):
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except:
        return None

lottie_train = load_lottiefile("Metro Rail.json")

# --- 2. LOGIKA ADMIN MODE ---
is_admin = st.query_params.get("mode") == "admin"

# --- 3. TAMPILAN UTAMA ---
st.set_page_config(page_title="Sintelis 1.21 BOO Utility", page_icon="📑", layout="wide")
st.title("📑 GANTI NAMA PDFs CEKLIS SINTELIS")

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("📁 Input & Setting")
    
    jenis_kegiatan = st.radio(
        "Pilih Jenis Kegiatan:",
        ["Perawatan", "Pemeriksaan"],
        index=0,
        horizontal=True
    )
    
    instansi = st.radio(
        "Pilih Instansi/Format Nama:",
        ["BTP JAK (Format Standar)", "BTP BD (Format Khusus Sintel Boo)"],
        index=0
    )
    
    format_eksklusif = True if "BTP BD" in instansi else False
    
    if is_admin:
        with st.expander("🛠️ Admin Debug Tools", expanded=False):
            st.info("Mode Admin: Fitur bantuan teknis.")
            debug_mode = st.checkbox("Aktifkan Layar Intip (Debug Mode)", value=False)
    else:
        debug_mode = False

    if "file_uploader_key" not in st.session_state:
        st.session_state["file_uploader_key"] = 0

    if st.button("🗑️ Hapus Semua File", use_container_width=True):
        st.session_state["file_uploader_key"] += 1
        st.rerun()

    uploaded_files = st.file_uploader(
        "Upload PDF",
        type="pdf",
        accept_multiple_files=True,
        key=f"uploader_{st.session_state['file_uploader_key']}"
    )

# --- FUNGSI OCR TERPISAH (CACHING AGAR TIDAK LELET) ---
@st.cache_data(show_spinner=False, max_entries=50)
def process_pdf_ocr(file_bytes, debug=False):
    images = convert_from_bytes(file_bytes, dpi=150, first_page=1, last_page=1)
    img = images[0].convert('L')
    img = ImageOps.autocontrast(img)
    width, height = img.size
    
    img_cropped = img.crop((0.0, 0.0, width * 1.0, height * 0.30)) 
    text_crop = pytesseract.image_to_string(img_cropped).upper()
    
    # Clean memory
    del img, images
    gc.collect()
    
    return text_crop, img_cropped

# --- 4. PROSES DATA ---
if uploaded_files:
    zip_buffer = BytesIO()
    processed_files, duplicate_errors, unique_filenames = [], [], set()
    
    with col2:
        head_col, btn_col = st.columns([1.5, 1])
        with head_col:
            st.subheader("📋 Hasil Proses")
        
        status_container = st.empty()
        with status_container.container():
            if lottie_train:
                st_lottie(lottie_train, height=150, key="train_loader")
            progress_text = st.empty()

        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_f:
            for idx, f in enumerate(uploaded_files):
                progress_text.info(f"🚂 Memproses {idx+1}/{len(uploaded_files)}...")
                
                name_only = f.name.upper()
                tgl_match = re.search(r'(\d{2})-(\d{2})-(\d{4})', name_only)
                
                if not tgl_match:
                    duplicate_errors.append(f"❌ {f.name}: Format tanggal tidak ditemukan.")
                    continue
                    
                tgl_full = tgl_match.group(0)
                bln_angka = str(int(tgl_match.group(2)))
                thn_angka = tgl_match.group(3)
                prefix_periode = f"{thn_angka}-{bln_angka}"
                
                assets_found = []
                target_keyword = None
                kode_ceklis = ""
                kategori_nama = ""

                try:
                    file_bytes = f.getvalue()
                    text_crop, img_cropped = process_pdf_ocr(file_bytes, debug_mode)
                    
                    if debug_mode: 
                        st.image(img_cropped, caption=f"Scan: {f.name}")
                        with st.expander(f"👀 Intip Teks OCR: {f.name}"):
                            st.text(text_crop)
                            
                    text_flat = text_crop.replace('\n', ' ')
                    is_special_doc = False

                    # ====================================================
                    # GERBANG A: DOKUMEN SPESIAL (Pencegatan 1 File Utuh)
                    # URUTAN PENTING: Dari spesifik → generic
                    # ====================================================
                    
                    # 1. PENGAMAN WESEL / POINT LOCK
                    if any(x in text_flat for x in ["POINT LOCK", "PENGAMAN WESEL"]):
                        is_special_doc = True
                        target_keyword = "WESEL"
                        kategori_nama = "WESEL"
                        kode_ceklis = "BPBYE1"
                        
                        w_match = re.search(r'(W\d+)', text_flat)
                        aid = w_match.group(1) if w_match else "W_UNKNOWN"
                        loc_id = "BOO" if "BOGOR" in text_flat else "LOKASI"
                        assets_found.append({"id": aid, "loc": loc_id})

                    # 2. PDSE
                    elif "PERALATAN DALAM PERSINYALAN ELEKTRIK" in text_flat:
                        is_special_doc = True
                        target_keyword = "PDSE"
                        kategori_nama = "PDSE"
                        kode_ceklis = "BPBYE2"
                        
                        if "BOGORPALEDANG" in text_flat or "PALEDANG" in text_flat: loc_id = "BOP"
                        elif "BOGOR" in text_flat: loc_id = "BOO"
                        elif "CILEBUT" in text_flat: loc_id = "CLT"
                        elif "BATUTULIS" in text_flat: loc_id = "BTT"
                        elif "MASENG" in text_flat: loc_id = "MSG"
                        elif "CIOMAS" in text_flat: loc_id = "COS"
                        elif "CIGOMBONG" in text_flat: loc_id = "CGB"
                        else: loc_id = "LOKASI"
                        
                        assets_found.append({"id": "", "loc": loc_id})

                    # 3. SERAT OPTIK + JPL (SANGAT SPESIFIK - CHECK DULU SEBELUM GENERIC)
                    elif "SERAT OPTIK" in text_flat and "JPL" in text_flat:
                        is_special_doc = True
                        target_keyword = "SERAT OPTIK"
                        kategori_nama = "SERAT OPTIK"
                        kode_ceklis = "BPBKF4"
                        
                        # Extract JPL number + lokasi dari OCR
                        lines = [line.strip() for line in text_crop.split('\n') if line.strip()]
                        noise_local = ["PERAWATAN", "PEMERIKSAAN", "MINGGUAN", "BULANAN", "TAHUNAN", "CEKLIS", "ULANG", 
                                       "PENGGERAK", "WESEL", "ELEKTRIK", "AXLE", "COUNTER", "SIEMENS", "PERAGA",
                                       "SINYAL", "SAMPEL", "NOMOR", "INTERNAL", "TERLAYAN", "SETEMPAT", "BLOK",
                                       "MASUK", "KELUAR", "MUKA", "DAN", "LANGSIR", "JALAN", "SERAT", "OPTIK"]
                        
                        for line in lines:
                            if "JPL" in line and ("OTB" in line or "FO" in line):
                                clean = line.split(":")[-1].strip() if ":" in line else line.strip()
                                words = clean.replace(".", " ").split()
                                final = [w for w in words if w not in noise_local]
                                
                                if final and "JPL" in final:
                                    jpl_idx = final.index("JPL")
                                    if jpl_idx + 1 < len(final):
                                        aid = f"JPL {final[jpl_idx + 1]}"
                                        loc_id = " ".join(final[jpl_idx + 2:]) if jpl_idx + 2 < len(final) else "LOKASI"
                                        assets_found.append({"id": aid, "loc": loc_id})

                    # 4. TELKOM DI PINTU PERLINTASAN (PTPP - SPESIFIK)
                    elif "TELEKOMUNIKASI DI PINTU PERLINTASAN" in text_flat:
                        is_special_doc = True
                        target_keyword = "PTPP"
                        kategori_nama = "PTPP"
                        kode_ceklis = "BPBKS17"
                        
                        # Extract JPL seperti PINTU PERLINTASAN
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
                            
                        assets_found.append({"id": aid, "loc": loc_id})

                    # 5. PINTU PERLINTASAN GENERIC (HANYA JPL, BUKAN TELKOM)
                    elif "PINTU PERLINTASAN" in text_flat and "TELEKOMUNIKASI" not in text_flat:
                        is_special_doc = True
                        target_keyword = "PINTU PERLINTASAN"
                        kategori_nama = "PINTU PERLINTASAN"
                        kode_ceklis = "BPBKS17"
                        
                        # Extract JPL number + lokasi
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
                            
                        assets_found.append({"id": aid, "loc": loc_id})

                    # 6. TELKOM DI STASIUN (PTDS)
                    elif "TELEKOMUNIKASI DI STASIUN" in text_flat:
                        is_special_doc = True
                        target_keyword = "PTDS"
                        kategori_nama = "PTDS"
                        kode_ceklis = "BPBKS15"
                        
                        if "BOGORPALEDANG" in text_flat or "PALEDANG" in text_flat: loc_id = "BOP"
                        elif "BOGOR" in text_flat: loc_id = "BOO"
                        elif "CILEBUT" in text_flat: loc_id = "CLT"
                        elif "BATUTULIS" in text_flat: loc_id = "BTT"
                        elif "MASENG" in text_flat: loc_id = "MSG"
                        elif "CIOMAS" in text_flat: loc_id = "COS"
                        elif "CIGOMBONG" in text_flat: loc_id = "CGB"
                        else: loc_id = "LOKASI"
                        
                        assets_found.append({"id": "", "loc": loc_id})

                    # 7. TELKOM DI LUAR STASIUN (PTLS)
                    elif "TELEKOMUNIKASI DI LUAR STASIUN" in text_flat:
                        is_special_doc = True
                        target_keyword = "PTLS"
                        kategori_nama = "PTLS"
                        kode_ceklis = "BPBKS16"
                        
                        if "BOGORPALEDANG" in text_flat or "PALEDANG" in text_flat: loc_id = "BOP"
                        elif "BOGOR" in text_flat: loc_id = "BOO"
                        elif "CILEBUT" in text_flat: loc_id = "CLT"
                        elif "BATUTULIS" in text_flat: loc_id = "BTT"
                        elif "MASENG" in text_flat: loc_id = "MSG"
                        elif "CIOMAS" in text_flat: loc_id = "COS"
                        elif "CIGOMBONG" in text_flat: loc_id = "CGB"
                        else: loc_id = "LOKASI"
                        
                        assets_found.append({"id": "", "loc": loc_id})

                    # 8. CATU DAYA
                    elif "CATU DAYA" in text_flat:
                        is_special_doc = True
                        target_keyword = "CATU DAYA"
                        kategori_nama = "CATU DAYA"
                        kode_ceklis = "BPBYE14"
                        
                        if "BOGORPALEDANG" in text_flat or "PALEDANG" in text_flat: loc_id = "BOP"
                        elif "BOGOR" in text_flat: loc_id = "BOO"
                        elif "CILEBUT" in text_flat: loc_id = "CLT"
                        elif "BATUTULIS" in text_flat: loc_id = "BTT"
                        elif "MASENG" in text_flat: loc_id = "MSG"
                        elif "CIOMAS" in text_flat: loc_id = "COS"
                        elif "CIGOMBONG" in text_flat: loc_id = "CGB"
                        else: loc_id = "LOKASI"
                        
                        assets_found.append({"id": "", "loc": loc_id})

                    # 9. SERAT OPTIK NORMAL (TANPA JPL)
                    elif "SERAT OPTIK" in text_flat and "JPL" not in text_flat:
                        is_special_doc = True
                        target_keyword = "SERAT OPTIK"
                        kategori_nama = "SERAT OPTIK"
                        kode_ceklis = "BPBKF4"
                        
                        if "BOGORPALEDANG" in text_flat or "PALEDANG" in text_flat: loc_id = "BOP"
                        elif "BOGOR" in text_flat: loc_id = "BOO"
                        elif "CILEBUT" in text_flat: loc_id = "CLT"
                        elif "BATUTULIS" in text_flat: loc_id = "BTT"
                        elif "MASENG" in text_flat: loc_id = "MSG"
                        elif "CIOMAS" in text_flat: loc_id = "COS"
                        elif "CIGOMBONG" in text_flat: loc_id = "CGB"
                        else: loc_id = "LOKASI"
                        
                        assets_found.append({"id": "", "loc": loc_id})

                    # ====================================================
                    # TEMPLATE KODE CEKLIS TAMBAHAN (READY FOR FUTURE USE)
                    # ====================================================
                    # Kode berikut siap untuk diaktifkan ketika ada dokumen baru
                    # Sesuaikan keyword deteksi sesuai konten OCR dokumen
                    
                    # BPBYE4 - Perawatan Peralatan CTC CTS 1 Bulanan
                    # elif "CTC" in text_flat or "CTS" in text_flat:
                    #     is_special_doc = True
                    #     target_keyword = "CTC_CTS"
                    #     kategori_nama = "CTC CTS"
                    #     kode_ceklis = "BPBYE4"
                    #     # Extract lokasi logic here
                    #     assets_found.append({"id": "", "loc": loc_id})
                    
                    # BPBYE5 - Perawatan Axle Counter Siemens 1 Bulanan
                    # elif "AXLE" in text_flat and "SIEMENS" in text_flat:
                    #     is_special_doc = True
                    #     target_keyword = "AXC_SIEMENS"
                    #     kategori_nama = "AXC SIEMENS"
                    #     kode_ceklis = "BPBYE5"
                    #     # Extract ZP logic here
                    #     assets_found.append({"id": aid, "loc": loc_id})
                    
                    # BPBYE6 - Perawatan Axle Counter Altpro 1 Bulanan
                    # elif "AXLE" in text_flat and "ALTPRO" in text_flat:
                    #     is_special_doc = True
                    #     target_keyword = "AXC_ALTPRO"
                    #     kategori_nama = "AXC ALTPRO"
                    #     kode_ceklis = "BPBYE6"
                    #     assets_found.append({"id": aid, "loc": loc_id})
                    
                    # BPBYE8 - Perawatan Axle Counter Thales 1 Bulanan
                    # elif "AXLE" in text_flat and "THALES" in text_flat:
                    #     is_special_doc = True
                    #     target_keyword = "AXC_THALES"
                    #     kategori_nama = "AXC THALES"
                    #     kode_ceklis = "BPBYE8"
                    #     assets_found.append({"id": aid, "loc": loc_id})
                    
                    # BPBYE9 - Perawatan Axle Counter Esso-M 1 Bulanan
                    # elif "AXLE" in text_flat and "ESSO" in text_flat:
                    #     is_special_doc = True
                    #     target_keyword = "AXC_ESSOM"
                    #     kategori_nama = "AXC ESSO-M"
                    #     kode_ceklis = "BPBYE9"
                    #     assets_found.append({"id": aid, "loc": loc_id})
                    
                    # BPBYE10 - Perawatan Track Circuit 1 Bulanan
                    # elif "TRACK CIRCUIT" in text_flat:
                    #     is_special_doc = True
                    #     target_keyword = "TRACK_CIRCUIT"
                    #     kategori_nama = "TRACK CIRCUIT"
                    #     kode_ceklis = "BPBYE10"
                    #     assets_found.append({"id": "", "loc": loc_id})
                    
                    # BPBYE11 - Perawatan Location Case 1 Bulanan
                    # elif "LOCATION CASE" in text_flat:
                    #     is_special_doc = True
                    #     target_keyword = "LOCATION_CASE"
                    #     kategori_nama = "LOCATION CASE"
                    #     kode_ceklis = "BPBYE11"
                    #     assets_found.append({"id": "", "loc": loc_id})
                    
                    # BPBYE12 - Perawatan Point Lock Perintang Pelalau 2 Mingguan
                    # elif "POINT LOCK" in text_flat and "PELALAU" in text_flat:
                    #     is_special_doc = True
                    #     target_keyword = "POINT_LOCK_PELALAU"
                    #     kategori_nama = "POINT LOCK PELALAU"
                    #     kode_ceklis = "BPBYE12"
                    #     assets_found.append({"id": aid, "loc": loc_id})
                    
                    # BPBYE13 - Perawatan Peralatan Pintu Perlintasan 1 Bulanan
                    # (NOTE: Hati-hati, overlap dengan PINTU PERLINTASAN)
                    # elif "PERALATAN PINTU PERLINTASAN" in text_flat:
                    #     is_special_doc = True
                    #     target_keyword = "PINTU_PERLINTASAN_PERALATAN"
                    #     kategori_nama = "PINTU PERLINTASAN PERALATAN"
                    #     kode_ceklis = "BPBYE13"
                    #     assets_found.append({"id": "", "loc": loc_id})
                    
                    # BPBYE15 - Perawatan Wesel Terlayan Setempat Elektrik 1 Bulanan
                    # elif "WESEL" in text_flat and "TERLAYAN SETEMPAT" in text_flat:
                    #     is_special_doc = True
                    #     target_keyword = "WESEL_TERLAYAN"
                    #     kategori_nama = "WESEL TERLAYAN"
                    #     kode_ceklis = "BPBYE15"
                    #     assets_found.append({"id": aid, "loc": loc_id})
                    
                    # BPBKS1-14 - Radio & Telkom Series (Uncomment saat diperlukan)
                    # elif "RADIO LOKOMOTIF" in text_flat:
                    #     if "TAIT" in text_flat:
                    #         kode_ceklis = "BPBKS10"  # BPBKS10 - TAIT 3 Bulanan
                    #     elif "HARIAN" in text_flat:
                    #         kode_ceklis = "BPBKS1"   # BPBKS1 - Harian
                    #     else:
                    #         kode_ceklis = "BPBKS2"   # BPBKS2 - 3 Bulanan
                    #     is_special_doc = True
                    #     target_keyword = "RADIO_LOKOMOTIF"
                    #     kategori_nama = "RADIO LOKOMOTIF"
                    #     assets_found.append({"id": "", "loc": loc_id})
                    
                    # BPBKF1-3 - Radio Basestation Series
                    # elif "RADIO BASESTATION" in text_flat:
                    #     if "TAIT" in text_flat:
                    #         kode_ceklis = "BPBKF3"   # BPBKF3 - Tait
                    #     elif "DIGITAL" in text_flat:
                    #         kode_ceklis = "BPBKF2"   # BPBKF2 - Digital
                    #     else:
                    #         kode_ceklis = "BPBKF1"   # BPBKF1 - Standard
                    #     is_special_doc = True
                    #     target_keyword = "RADIO_BASESTATION"
                    #     kategori_nama = "RADIO BASESTATION"
                    #     assets_found.append({"id": "", "loc": loc_id})
                    
                    # BPBKF5 - Perawatan Saluran Blok 1 Bulanan
                    # elif "SALURAN BLOK" in text_flat:
                    #     is_special_doc = True
                    #     target_keyword = "SALURAN_BLOK"
                    #     kategori_nama = "SALURAN BLOK"
                    #     kode_ceklis = "BPBKF5"
                    #     assets_found.append({"id": "", "loc": loc_id})
                    
                    # BPBKF6 - Perawatan Saluran Blok 6 Bulanan
                    # elif "SALURAN BLOK" in text_flat and "6 BULANAN" in text_flat:
                    #     is_special_doc = True
                    #     target_keyword = "SALURAN_BLOK_6BLN"
                    #     kategori_nama = "SALURAN BLOK 6BLN"
                    #     kode_ceklis = "BPBKF6"
                    #     assets_found.append({"id": "", "loc": loc_id})


                    # ====================================================
                    # GERBANG B: DOKUMEN MULTI-ASET (Sistem Standar Lama)
                    # ====================================================
                    
                    if not is_special_doc:
                        if any(x in name_only for x in ["WESEL", "WLSE"]):
                            target_keyword, kode_ceklis, kategori_nama = "WESEL", "BPBYE1", "WESEL"
                        elif any(x in name_only for x in ["AXLE", "COUNTER", "AXL"]):
                            target_keyword, kode_ceklis, kategori_nama = "AXLE", "BPBYE7", "AXC"
                        elif any(x in name_only for x in ["SERAT OPTIK", "SO"]): 
                            target_keyword, kode_ceklis, kategori_nama = "SERAT OPTIK", "BPBKF4", "SERAT OPTIK"
                        elif any(x in name_only for x in ["SINYAL", "BLOK", "ZP"]):
                            target_keyword, kode_ceklis, kategori_nama = "SINYAL", "BPBYE3", "SINYAL"

                        if target_keyword:
                            lines = [line.strip() for line in text_crop.split('\n') if line.strip()]
                            noise = ["PERAWATAN", "PEMERIKSAAN", "MINGGUAN", "BULANAN", "TAHUNAN", "CEKLIS", "ULANG", 
                                     "PENGGERAK", "WESEL", "ELEKTRIK", "AXLE", "COUNTER", "SIEMENS", "PERAGA",
                                     "SINYAL", "SAMPEL", "NOMOR", "INTERNAL", "TERLAYAN", "SETEMPAT", "BLOK",
                                     "MASUK", "KELUAR", "MUKA", "DAN", "LANGSIR", "JALAN", "SERAT", "OPTIK"]

                            for line in lines:
                                if any(k in line for k in ["SINYAL", "BLOK", "WESEL", "AXLE", "COUNTER", "JPL"]):
                                    if any(judul in line for judul in ["BULANAN", "MINGGUAN", "TAHUNAN"]):
                                        continue
                                        
                                    clean = line.split(":")[-1].strip() if ":" in line else line.strip()
                                    words = clean.replace(".", " ").split()
                                    final = [w for w in words if w not in noise]
                                    
                                    if final:
                                        jpl_match = re.search(r'(JPL\s+\d+\b(?:\s+[A-Z-]+)?)', line)
                                        
                                        if target_keyword == "SERAT OPTIK" and jpl_match:
                                            j_full = jpl_match.group(1).strip()
                                            j_words = j_full.split()
                                            if len(j_words) > 2:
                                                aid = f"{j_words[0]} {j_words[1]}"
                                                loc_id = " ".join(j_words[2:])
                                            else:
                                                aid = j_full
                                                loc_id = "LOKASI"
                                        elif final[0] == "ZP" and len(final) > 1 and any(char.isdigit() for char in final[1]):
                                            aid = f"{final[0]} {final[1]}"
                                            loc_id = " ".join(final[2:]) if len(final) > 2 else "LOKASI"
                                        else:
                                            aid = final[0]
                                            loc_id = " ".join(final[1:]) if len(final) > 1 else "LOKASI"
                                            
                                        loc_id = loc_id.replace("BUD", "BJD").strip()
                                        
                                        if target_keyword == "WESEL" and not aid.startswith("W"): aid = f"W{aid}"
                                        elif target_keyword == "AXLE" and not aid.startswith("ZP"): aid = f"ZP{aid}"
                                        
                                        assets_found.append({"id": aid, "loc": loc_id})
                                        
                except Exception as e:
                    duplicate_errors.append(f"❌ {f.name}: OCR Error ({str(e)})")

                # === 5. MERAKIT NAMA FILE AKHIR ===
                if assets_found:
                    for asset in assets_found:
                        aid_clean = asset["id"].strip()
                        aloc_clean = asset["loc"].strip()
                        
                        identitas = f"{kategori_nama} {aid_clean} {aloc_clean}".replace("  ", " ").strip()
                        
                        if format_eksklusif:
                            new_name = f"{prefix_periode}_Resor 1.21 Boo_{kode_ceklis}_{jenis_kegiatan}_{identitas}_{tgl_full}.pdf"
                            new_name = new_name.replace("__", "_").replace(" _", "_")
                        else:
                            new_name = f"{jenis_kegiatan.upper()} {identitas} {tgl_full}.pdf"
                            new_name = new_name.replace("  ", " ")
                            
                        if new_name not in unique_filenames:
                            zip_f.writestr(new_name, f.getvalue())
                            processed_files.append(new_name)
                            unique_filenames.add(new_name)
                        else:
                            duplicate_errors.append(f"⚠️ {f.name}: ID {aid_clean} duplikat.")
                else:
                    duplicate_errors.append(f"🔍 {f.name}: Gagal identifikasi ID Aset.")
                    
            status_container.empty()

    # --- 6. OUTPUT & DOWNLOAD BLOK ---
    with col2:
        if processed_files:
            with btn_col:
                st.download_button(
                    label="📥 DOWNLOAD ZIP", 
                    data=zip_buffer.getvalue(), 
                    file_name="Hasil_Rename_Sintelis_BOO.zip", 
                    mime="application/zip", 
                    use_container_width=True, 
                    type="primary"
                )
            
            with st.expander(f"✅ Sukses Teridentifikasi ({len(processed_files)})", expanded=True):
                if processed_files:
                    with st.container(height=150):
                        for p_file in processed_files: 
                            st.write(f"📄 {p_file}")
                else:
                    st.write("Belum ada file yang berhasil diproses.")

        with st.expander(f"❌ Gagal Diproses ({len(duplicate_errors)})", expanded=True):
            if duplicate_errors:
                with st.container(height=150):
                    for err in duplicate_errors: 
                        st.warning(err)
            else:
                st.write("Tidak ada kendala pada file.")

st.markdown("---")
st.markdown("Developed by Dika Armansyah | Sintelis 1.21 BOO Utility", unsafe_allow_html=True)