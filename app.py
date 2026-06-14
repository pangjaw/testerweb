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
    
    # --- PINTU GERBANG PENENTUAN JENIS DOKUMEN ---
    target_keyword = None
    # "POINT" dipindahkan ke daftar Dokumen Spesial karena formatnya berbeda
    if any(x in name_only for x in ["WESEL", "WLSE"]) and "POINT" not in name_only: 
        target_keyword, kode_ceklis, kategori_nama = "WESEL", "BPBYE1", "WESEL"
    elif any(x in name_only for x in ["AXLE", "COUNTER", "AXL"]): 
        target_keyword, kode_ceklis, kategori_nama = "AXLE", "BPBYE7", "AXC"
    elif any(x in name_only for x in ["SINYAL", "BLOK", "ZP"]): 
        target_keyword, kode_ceklis, kategori_nama = "SINYAL", "BPBYE3", "SINYAL"
    # Buka gerbang khusus untuk dokumen spesial TERMASUK POINT LOCK
    elif any(x in name_only for x in ["TELEKOMUNIKASI", "CATU DAYA", "SERAT OPTIK", "PERSINYALAN ELEKTRIK", "PDSE", "POINT"]):
        target_keyword, kode_ceklis, kategori_nama = "SPESIAL", "", ""

    if target_keyword:
        try:
            images = convert_from_bytes(file_bytes, dpi=150, first_page=1, last_page=1)
            img = images[0].convert('L') 
            img = ImageOps.autocontrast(img) 
            
            width, height = img.size
            img_cropped = img.crop((0.0, 0.0, width*1.0, height*0.35))
            
            text_crop = pytesseract.image_to_string(img_cropped).upper()
            text_flat = re.sub(r'\s+', ' ', text_crop)
            debug_text = text_flat
            
            # --- JALUR A: LOGIKA DOKUMEN SPESIAL BARU ---
            if target_keyword == "SPESIAL":
                aid = "SPESIAL"
                loc_code = "LOKASI"
                
                # --- TAMBAHAN BARU: LOGIKA POINT LOCK ---
                if "POINT LOCK" in text_flat or "PENGAMAN WESEL" in text_flat:
                    # Cari pola W + angka (contoh: W81, W12)
                    match_wesel = re.search(r'W\d+', text_flat)
                    if match_wesel:
                        aid = match_wesel.group(0).strip()
                    else:
                        aid = "WESEL" # Fallback jika gagal baca angka W
                    kode_ceklis = "BPBYE1" # Asumsi kode ceklis sama dengan Wesel biasa, ubah jika perlu
                    kategori_nama = "WPENGAMAN" # Sesuai format file awalmu
                # ----------------------------------------
                elif "TELEKOMUNIKASI DI STASIUN" in text_flat:
                    aid, kode_ceklis = "PTDS", "BPBKS15"
                elif "TELEKOMUNIKASI DI LUAR STASIUN" in text_flat:
                    aid, kode_ceklis = "PTLS", "BPBKS16"
                elif "TELEKOMUNIKASI DI PINTU PERLINTASAN" in text_flat:
                    aid, kode_ceklis = "PTPP", "BPBKS17"
                    match_jpl = re.search(r'JPL\s+\d+\b(?:\s+[A-Z\-]+)?', text_flat)
                    if match_jpl: loc_code = match_jpl.group(0).strip()
                elif "CATU DAYA" in text_flat:
                    aid, kode_ceklis = "CATUDAYA", "BPBYE14"
                elif "PERALATAN DALAM PERSINYALAN ELEKTRIK" in text_flat:
                    aid, kode_ceklis = "PDSE", "BPBYE2"
                elif "SERAT OPTIK" in text_flat:
                    aid, kode_ceklis = "SERAT OPTIK", "BPBKF4"
                    match_jpl = re.search(r'JPL\s+\d+\b(?:\s+[A-Z\-]+)?', text_flat)
                    if match_jpl: 
                        loc_code = match_jpl.group(0).strip()

                if loc_code == "LOKASI":
                    if "PALEDANG" in text_flat: loc_code = "BOP"
                    elif "BOGOR" in text_flat: loc_code = "BOO"
                    elif "CILEBUT" in text_flat: loc_code = "CLT"
                    elif "BATUTULIS" in text_flat: loc_code = "BTT"
                    elif "MASENG" in text_flat: loc_code = "MSG"
                    elif "CIOMAS" in text_flat: loc_code = "COS"
                    elif "CIGOMBONG" in text_flat: loc_code = "CGB"
                    elif "BOJONG" in text_flat or "BJD" in text_flat: loc_code = "BJD"
                    elif "CITAYAM" in text_flat: loc_code = "CTA"
                    elif "DEPOK" in text_flat: loc_code = "DP"

                assets_found.append({"id": aid, "loc": loc_code})

            # --- JALUR B: LOGIKA ORISINAL 100% (WESEL, AXLE, SINYAL) ---
            else:
                lines = [line.strip() for line in text_crop.split('\n') if line.strip()]
                noise = ["PERAWATAN", "PEMERIKSAAN", "MINGGUAN", "BULANAN", "TAHUNAN", "CEKLIS", "ULANG", 
                         "PENGGERAK", "WESEL", "ELEKTRIK", "AXLE", "COUNTER", "SIEMENS", "PERAGA", 
                         "SINYAL", "SAMPEL", "NOMOR", "INTERNAL", "TERLAYAN", "SETEMPAT", "BLOK", 
                         "MASUK", "KELUAR", "MUKA", "DAN", "LANGSIR", "JALAN"]

                for line in lines:
                    if any(k in line for k in ["SINYAL", "BLOK", "WESEL", "AXLE", "COUNTER"]):
                        
                        if any(judul in line for judul in ["BULANAN", "MINGGUAN", "TAHUNAN"]):
                            continue
                        
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
                            
            del img, img_cropped, images
            gc.collect() 
        except Exception as e:
            ocr_error = f"OCR Error ({str(e)})"
    else:
        ocr_error = "Bukan dokumen ceklis yang dikenali."
        
    return tgl_full, prefix_periode, kode_ceklis, kategori_nama, assets_found, ocr_error, debug_text