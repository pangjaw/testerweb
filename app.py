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

# --- 2. FUNGSI OCR & CACHE (MESIN UTAMA) ---
@st.cache_data(show_spinner=False, max_entries=100)
def extract_pdf_data(name_only, file_bytes):
    tgl_full, prefix_periode, kode_ceklis, kategori_nama = "", "", "", ""
    assets_found, ocr_error = [], None
    debug_text = ""
    
    tgl_match = re.search(r'(\d{2})-(\d{2})-(\d{4})', name_only)
    
    if not tgl_match:
        ocr_error = "Format tanggal (DD-MM-YYYY) tidak ditemukan pada nama file."
        return tgl_full, prefix_periode, kode_ceklis, kategori_nama, assets_found, ocr_error, debug_text
        
    tgl_full = tgl_match.group(0)
    bln_angka = str(int(tgl_match.group(2)))
    thn_angka = tgl_match.group(3)
    prefix_periode = f"{thn_angka}-{bln_angka}"
    
    # --- PENGATURAN AWAL JALUR STANDAR (ORISINAL) ---
    target_keyword = None
    if any(x in name_only for x in ["WESEL", "WLSE"]): 
        target_keyword, kode_ceklis, kategori_nama = "WESEL", "BPBYE1", "WESEL"
    elif any(x in name_only for x in ["AXLE", "COUNTER", "AXL"]): 
        target_keyword, kode_ceklis, kategori_nama = "AXLE", "BPBYE7", "AXC"
    elif any(x in name_only for x in ["SINYAL", "BLOK", "ZP"]): 
        target_keyword, kode_ceklis, kategori_nama = "SINYAL", "BPBYE3", "SINYAL"

    try:
        images = convert_from_bytes(file_bytes, dpi=150, first_page=1, last_page=1)
        img = images[0].convert('L') 
        img = ImageOps.autocontrast(img) 
        
        width, height = img.size
        img_cropped = img.crop((0.0, 0.0, width*1.0, height*0.35))
        
        text_crop = pytesseract.image_to_string(img_cropped).upper()
        text_flat = re.sub(r'\s+', ' ', text_crop)
        debug_text = text_flat
        
        # --- DETEKSI LOKASI UMUM (DARI KOP SURAT) ---
        general_loc = "LOKASI"
        if "PALEDANG" in text_flat: general_loc = "BOP"
        elif "BOGOR" in text_flat: general_loc = "BOO"
        elif "CILEBUT" in text_flat: general_loc = "CLT"
        elif "BATUTULIS" in text_flat: general_loc = "BTT"
        elif "MASENG" in text_flat: general_loc = "MSG"
        elif "CIOMAS" in text_flat: general_loc = "COS"
        elif "CIGOMBONG" in text_flat: general_loc = "CGB"
        elif "BOJONG" in text_flat or "BJD" in text_flat: general_loc = "BJD"
        elif "CITAYAM" in text_flat: general_loc = "CTA"
        elif "DEPOK" in text_flat: general_loc = "DP"

        # --- PEMBAGIAN KATEGORI KHUSUS ---
        is_ptds = "TELEKOMUNIKASI DI STASIUN" in text_flat
        is_ptls = "TELEKOMUNIKASI DI LUAR STASIUN" in text_flat
        is_ptpp = "TELEKOMUNIKASI DI PINTU PERLINTASAN" in text_flat
        is_catudaya = "CATU DAYA" in text_flat
        is_pdse = "PERALATAN DALAM PERSINYALAN ELEKTRIK" in text_flat
        is_point_lock = "POINT LOCK" in text_flat or "PENGAMAN WESEL" in text_flat
        
        is_serat_optik = "SERAT OPTIK" in text_flat or "SERAT OPTIK" in name_only
        is_so_jpl = is_serat_optik and ("JPL" in name_only or "JPL" in text_flat)
        is_so_normal = is_serat_optik and not is_so_jpl
        
        # --- JALUR A: PENCEGATAN DOKUMEN SPESIAL (1 FILE / LOKASI) ---
        if any([is_ptds, is_ptls, is_ptpp, is_catudaya, is_pdse, is_point_lock, is_so_normal]):
            loc_code = general_loc
            kategori_nama = "" 
            
            if is_ptds:
                aid, kode_ceklis = "PTDS", "BPBKS15"
            elif is_ptls:
                aid, kode_ceklis = "PTLS", "BPBKS16"
            elif is_ptpp:
                aid, kode_ceklis = "PTPP", "BPBKS17"
                match_jpl = re.search(r'JPL\s+\d+\b(?:\s+[A-Z\-]+)?', text_flat)
                if match_jpl: loc_code = match_jpl.group(0).strip()
            elif is_catudaya:
                aid, kode_ceklis = "CATUDAYA", "BPBYE14"
            elif is_pdse:
                aid, kode_ceklis = "PDSE", "BPBYE2"
            elif is_so_normal:
                aid, kode_ceklis = "SERAT OPTIK", "BPBKF4"
            elif is_point_lock:
                match_wesel = re.search(r'W\d+', text_flat)
                aid = match_wesel.group(0).strip() if match_wesel else "WESEL"
                kode_ceklis = "BPBYE1"
                kategori_nama = "WPENGAMAN"

            assets_found.append({"id": aid, "loc": loc_code})
            
        # --- JALUR B: SISTEM MULTI-ASET ORISINAL (WESEL, AXLE, SINYAL) ---
        else:
            if is_so_jpl:
                target_keyword, kode_ceklis, kategori_nama = "SO_JPL", "BPBKF4", "SERAT OPTIK"
                
            if target_keyword:
                lines = [line.strip() for line in text_crop.split('\n') if line.strip()]
                noise = ["PERAWATAN", "PEMERIKSAAN", "MINGGUAN", "BULANAN", "TAHUNAN", "CEKLIS", "ULANG", 
                         "PENGGERAK", "WESEL", "ELEKTRIK", "AXLE", "COUNTER", "SIEMENS", "PERAGA", 
                         "SINYAL", "SAMPEL", "NOMOR", "INTERNAL", "TERLAYAN", "SETEMPAT", "BLOK", 
                         "MASUK", "KELUAR", "MUKA", "DAN", "LANGSIR", "JALAN"]

                for line in lines:
                    if any(judul in line for judul in ["BULANAN", "MINGGUAN", "TAHUNAN"]):
                        continue
                        
                    if target_keyword == "SO_JPL":
                        if "JPL" in line:
                            match_jpl = re.search(r'JPL\s+\d+\b(?:\s+[A-Z\-]+)?', line)
                            if match_jpl:
                                jpl_str = match_jpl.group(0).strip()
                                parts = jpl_str.split(" ", 2)
                                aid_jpl = f"{parts[0]} {parts[1]}" if len(parts) >= 2 else parts[0]
                                # Ambil lokasi dari Kop jika di dalam tabel tidak ada
                                loc_jpl = parts[2] if len(parts) == 3 else general_loc 
                                assets_found.append({"id": aid_jpl, "loc": loc_jpl})
                    else:
                        # LOGIKA ORISINAL 100% UNTUK WESEL & SINYAL
                        if any(k in line for k in ["SINYAL", "BLOK", "WESEL", "AXLE", "COUNTER"]):
                            clean = line.split(":")[-1].strip() if ":" in line else line.strip()
                            words = clean.replace(".", " ").split()
                            final = [w for w in words if w not in noise]
                            
                            if final:
                                if final[0] == "ZP" and len(final) > 1 and any(char.isdigit() for char in final[1]):
                                    aid = f"{final[0]} {final[1]}"
                                    loc_id = " ".join(final[2:]) if len(final) > 2 else "LOKASI"
                                else:
                                    aid = final[0]
                                    loc_id = " ".join(final[1:]) if len(final) > 1 else "LOKASI"
                                
                                loc_id = loc_id.replace("BUD", "BJD").strip()
                                
                                if target_keyword == "WESEL" and not aid.startswith("W"): aid = f"W{aid}"
                                elif target_keyword == "AXLE" and not aid.startswith("ZP"): aid = f"ZP{aid}"
                                assets_found.append({"id": aid, "loc": loc_id})
            else:
                ocr_error = "Bukan dokumen ceklis yang dikenali."
                
        del img, img_cropped, images
        gc.collect() 
    except Exception as e:
        ocr_error = f"OCR Error ({str(e)})"
        
    return tgl_full, prefix_periode, kode_ceklis, kategori_nama, assets_found, ocr_error, debug_text

# --- 3. TAMPILAN UTAMA UI ---
is_admin = st.query_params.get("mode") == "admin"
st.set_page_config(page_title="Sintelis 1.21 BOO Utility", page_icon="📑", layout="wide")
st.title("📑 GANTI NAMA PDFs CEKLIS SINTELIS")

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("📁 Input & Setting")
    
    jenis_kegiatan = st.radio("Pilih Jenis Kegiatan:", ["Perawatan", "Pemeriksaan"], index=0, horizontal=True)
    instansi = st.radio("Pilih Instansi/Format Nama:", ["BTP JAK (Format Standar)", "BTP BD (Format Khusus Sintel Boo)"], index=0)
    format_eksklusif = True if "BTP BD" in instansi else False
    
    if is_admin:
        with st.expander("🛠️ Admin Debug Tools", expanded=False):
            st.info("Mode Admin: Mengecek teks mentah yang dibaca sistem OCR.")
            debug_mode = st.checkbox("Aktifkan Layar Intip", value=False)
    else:
        debug_mode = False

    if "file_uploader_key" not in st.session_state:
        st.session_state["file_uploader_key"] = 0

    if st.button("🗑️ Hapus Semua File", use_container_width=True):
        st.session_state["file_uploader_key"] += 1
        extract_pdf_data.clear()
        st.rerun()

    uploaded_files = st.file_uploader(
        "Upload Semua Jenis PDF Ceklis Anda", 
        type="pdf", 
        accept_multiple_files=True, 
        key=f"uploader_{st.session_state['file_uploader_key']}"
    )

# --- 4. PEMROSESAN & OUTPUT UI ---
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
                progress_text.info(f"🚂 Memeriksa File {idx+1}/{len(uploaded_files)}...")
                
                tgl_full, prefix_periode, kode_ceklis, kategori_nama, assets_found, ocr_error, debug_text = extract_pdf_data(f.name.upper(), f.getvalue())
                
                if debug_mode and debug_text:
                    with st.expander(f"👀 Teks OCR: {f.name}"):
                        st.write(debug_text)
                
                if ocr_error:
                    duplicate_errors.append(f"❌ `{f.name}`: {ocr_error}")
                    continue

                if assets_found:
                    for asset in assets_found:
                        aid_clean = asset["id"].strip()
                        aloc_clean = asset["loc"].strip()
                        
                        if format_eksklusif:
                            new_name = f"{prefix_periode}_Resor 1.21 Boo_{kode_ceklis}_{jenis_kegiatan}_{kategori_nama}_{aid_clean}_{aloc_clean}_{tgl_full}.pdf"
                        else:
                            new_name = f"{jenis_kegiatan.upper()} {kategori_nama} {aid_clean} {aloc_clean} {tgl_full}.pdf"

                        new_name = new_name.replace("__", "_").replace("  ", " ")

                        if new_name not in unique_filenames:
                            zip_f.writestr(new_name, f.getvalue())
                            processed_files.append(new_name)
                            unique_filenames.add(new_name)
                        else:
                            duplicate_errors.append(f"⚠️ `{f.name}`: ID `{aid_clean}` duplikat.")
                else:
                    duplicate_errors.append(f"🔍 `{f.name}`: Gagal identifikasi ID Aset.")

        status_container.empty()

        if processed_files:
            with btn_col:
                st.download_button(label="📥 DOWNLOAD ZIP", data=zip_buffer.getvalue(), file_name="Hasil_Rename_Sintelis_BOO.zip", mime="application/zip", use_container_width=True, type="primary")

        with st.expander(f"✅ Sukses Teridentifikasi ({len(processed_files)})", expanded=True):
            if processed_files:
                with st.container(height=150):
                    for p_file in processed_files: st.write(f"📄 `{p_file}`")
            else:
                st.write("Belum ada file yang berhasil diproses.")

        with st.expander(f"❌ Gagal Diproses ({len(duplicate_errors)})", expanded=True):
            if duplicate_errors:
                with st.container(height=150):
                    for err in duplicate_errors: st.warning(err)
            else:
                st.write("Tidak ada kendala pada file.")

st.markdown("---")
st.markdown("<div style='text-align: center; color: grey;'>Developed by <b>Dika Armansyah</b> | Sintelis 1.21 BOO Utility</div>", unsafe_allow_html=True)