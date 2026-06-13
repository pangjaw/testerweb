import streamlit as st
import re
import zipfile
import platform
import pytesseract
import gc 
from io import BytesIO
from pdf2image import convert_from_bytes
from PIL import ImageOps

# --- KONFIGURASI TESSERACT ---
if platform.system() == "Windows":
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
else:
    pytesseract.pytesseract.tesseract_cmd = 'tesseract'

# --- TAMPILAN UTAMA ---
st.set_page_config(page_title="Test PDSE Saja", page_icon="🧪", layout="wide")
st.title("🧪 UJI COBA KHUSUS PDSE")
st.info("Versi Update: Area crop diperluas dan filter kata kunci dibuat lebih fleksibel.")

uploaded_files = st.file_uploader("Upload PDF PDSE", type="pdf", accept_multiple_files=True)

# --- PROSES DATA ---
if uploaded_files:
    zip_buffer = BytesIO()
    processed_files, duplicate_errors = [], []
    
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_f:
        for f in uploaded_files:
            name_only = f.name.upper()
            
            # 1. Ambil Tanggal dari Nama File Asli
            tgl_match = re.search(r'(\d{2})-(\d{2})-(\d{4})', name_only)
            if not tgl_match:
                duplicate_errors.append(f"❌ `{f.name}`: Format tanggal (DD-MM-YYYY) tidak ditemukan.")
                continue
            tgl_full = tgl_match.group(0)

            # 2. Proses OCR
            try:
                images = convert_from_bytes(f.getvalue(), dpi=150, first_page=1, last_page=1)
                img = images[0].convert('L') 
                img = ImageOps.autocontrast(img) 
                
                width, height = img.size
                
                # OPTIMASI 1: Tarik crop mentok sampai ke ujung paling atas (0.0) dan ke bawah (0.35)
                img_cropped = img.crop((0.0, 0.0, width*1.0, height*0.35))
                
                text_crop = pytesseract.image_to_string(img_cropped).upper()
                text_flat = re.sub(r'\s+', ' ', text_crop) # Ratakan spasi & enter
                
                # --- LAYAR INTIP DEBUG ---
                with st.expander(f"👀 Intip Hasil Baca OCR: {f.name}"):
                    st.write(text_flat)
                
                # OPTIMASI 2: Logika deteksi dipisah menjadi dua kata kunci utama untuk menghindari typo tipis OCR
                if "PERALATAN DALAM" in text_flat and "PERSINYALAN" in text_flat:
                    loc_code = "LOKASI"
                    
                    if "BOGOR" in text_flat: loc_code = "BOO"
                    elif "CILEBUT" in text_flat: loc_code = "CLT"
                    elif "BOJONG" in text_flat or "BJD" in text_flat: loc_code = "BJD"
                    elif "CITAYAM" in text_flat: loc_code = "CTA"
                    elif "DEPOK" in text_flat: loc_code = "DP"
                    
                    new_name = f"PERAWATAN PDSE {loc_code} {tgl_full}.pdf"
                    
                    zip_f.writestr(new_name, f.getvalue())
                    processed_files.append(new_name)
                else:
                    duplicate_errors.append(f"⚠️ `{f.name}`: Bukan dokumen PDSE atau gagal terbaca OCR.")
                
                del img, img_cropped, images
                gc.collect() 
                
            except Exception as e:
                duplicate_errors.append(f"❌ `{f.name}`: Error OCR ({str(e)})")

    # --- TAMPILAN HASIL ---
    st.markdown("### 📋 Hasil Proses")
    if processed_files:
        st.download_button(
            label="📥 DOWNLOAD ZIP", 
            data=zip_buffer.getvalue(), 
            file_name="Test_Hasil_PDSE.zip", 
            mime="application/zip", 
            type="primary"
        )
        for p_file in processed_files:
            st.success(f"📄 Berhasil: `{p_file}`")
            
    if duplicate_errors:
        for err in duplicate_errors:
            st.warning(err)