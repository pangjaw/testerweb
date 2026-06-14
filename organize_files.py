#!/usr/bin/env python3
"""
DIKO File Organizer v2 - Extract ZIP/RAR dan organize files by BTP format & asset type
Usage: python3 organize_files.py
"""

import os
import shutil
import zipfile
import subprocess
from pathlib import Path

def extract_zip(zip_path, extract_to):
    """Extract ZIP file"""
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        print(f"   ✅ Extracted: {os.path.basename(zip_path)}")
        return True
    except Exception as e:
        print(f"   ❌ Error extracting ZIP: {str(e)}")
        return False

def extract_rar(rar_path, extract_to):
    """Extract RAR file using WinRAR or 7z"""
    try:
        # Try WinRAR first
        result = subprocess.run(
            ['unrar', 'x', '-y', rar_path, extract_to],
            capture_output=True,
            timeout=60
        )
        if result.returncode == 0:
            print(f"   ✅ Extracted: {os.path.basename(rar_path)}")
            return True
    except:
        pass
    
    try:
        # Try 7z
        result = subprocess.run(
            ['7z', 'x', f'-o{extract_to}', rar_path],
            capture_output=True,
            timeout=60
        )
        if result.returncode == 0:
            print(f"   ✅ Extracted: {os.path.basename(rar_path)}")
            return True
    except:
        pass
    
    print(f"   ⚠️  Could not extract RAR: {os.path.basename(rar_path)}")
    print(f"      (Install 7z or WinRAR for RAR support)")
    return False

def extract_asset_type(filename):
    """Extract asset type from renamed PDF filename"""
    filename_upper = filename.upper()
    
    # Format: {periode}_Resor 1.21 Boo_{kode}_{jenis}_{identitas}_{tanggal}.pdf
    parts = filename.split('_')
    if len(parts) >= 5:
        identitas = parts[4]
    else:
        return "Unknown"
    
    identitas_upper = identitas.upper()
    
    # Asset type detection
    if 'AXLE' in identitas_upper or 'ZP' in identitas_upper:
        return 'Axle Counter'
    elif 'SINYAL' in identitas_upper or 'PERAGA' in identitas_upper or 'BLK' in identitas_upper:
        return 'Peraga Sinyal Elektrik'
    elif 'PDSE' in identitas_upper or 'PERSINYALAN' in identitas_upper:
        return 'PDSE'
    elif 'WESEL' in identitas_upper or 'W' in identitas_upper:
        return 'Wesel'
    elif 'CATU DAYA' in identitas_upper or 'DAYA' in identitas_upper:
        return 'Catu Daya'
    elif 'SERAT OPTIK' in identitas_upper or 'SO' in identitas_upper or 'JPL' in identitas_upper:
        return 'Serat Optik'
    elif 'PTDS' in identitas_upper or 'STASIUN' in identitas_upper:
        return 'PTDS'
    elif 'PTLS' in identitas_upper or 'LUAR STASIUN' in identitas_upper:
        return 'PTLS'
    elif 'PTPP' in identitas_upper or ('PINTU PERLINTASAN' in identitas_upper and 'TELEKOM' in filename.upper()):
        return 'PTPP'
    elif 'PINTU PERLINTASAN' in identitas_upper:
        return 'Pintu Perlintasan'
    else:
        return 'Unknown'

def organize_files():
    """Extract archives and organize files"""
    
    base_folder = r"C:\Users\SINTEL 1.21 BOO\Downloads\6. JUNI\hasil download"
    
    print("🤖 DIKO File Organizer v2.0")
    print("="*70)
    print("🔍 Phase 1: Scanning for ZIP/RAR archives...")
    print("="*70)
    
    # First, extract all ZIP/RAR files
    for btp_format in ['BTP JAK', 'BTP BD']:
        btp_folder = os.path.join(base_folder, btp_format)
        
        if not os.path.exists(btp_folder):
            print(f"⚠️  Folder not found: {btp_folder}")
            continue
        
        print(f"\n📁 Processing {btp_format}:")
        print("-"*70)
        
        # Look for ZIP files
        for filename in os.listdir(btp_folder):
            file_path = os.path.join(btp_folder, filename)
            
            if filename.lower().endswith('.zip'):
                print(f"   📦 Found ZIP: {filename}")
                extract_zip(file_path, btp_folder)
                # Delete ZIP after extraction
                try:
                    os.remove(file_path)
                    print(f"   🗑️  Deleted: {filename}")
                except:
                    pass
            
            elif filename.lower().endswith('.rar'):
                print(f"   📦 Found RAR: {filename}")
                extract_rar(file_path, btp_folder)
                # Delete RAR after extraction
                try:
                    os.remove(file_path)
                    print(f"   🗑️  Deleted: {filename}")
                except:
                    pass
    
    print("\n" + "="*70)
    print("🔍 Phase 2: Organizing extracted files...")
    print("="*70)
    
    # Now organize all PDF files
    for btp_format in ['BTP JAK', 'BTP BD']:
        btp_folder = os.path.join(base_folder, btp_format)
        
        if not os.path.exists(btp_folder):
            continue
        
        print(f"\n📁 Organizing {btp_format}:")
        print("-"*70)
        
        file_count = 0
        
        for filename in os.listdir(btp_folder):
            if not filename.lower().endswith('.pdf'):
                continue
            
            file_path = os.path.join(btp_folder, filename)
            
            # Skip if it's in a subfolder already
            if os.path.isfile(file_path):
                asset_type = extract_asset_type(filename)
                asset_folder = os.path.join(btp_folder, asset_type)
                os.makedirs(asset_folder, exist_ok=True)
                
                destination = os.path.join(asset_folder, filename)
                
                if os.path.exists(destination):
                    print(f"   ⚠️  {filename} → {asset_type}/ (exists)")
                else:
                    try:
                        shutil.move(file_path, destination)
                        print(f"   ✅ {filename} → {asset_type}/")
                        file_count += 1
                    except Exception as e:
                        print(f"   ❌ {filename} → ERROR: {str(e)}")
        
        if file_count > 0:
            print(f"\n   📊 Organized {file_count} files in {btp_format}")
    
    print("\n" + "="*70)
    print("✅ Organization complete!")
    print("="*70)

if __name__ == "__main__":
    organize_files()
