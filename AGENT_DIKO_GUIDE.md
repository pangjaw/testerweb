# 🤖 AGENT DIKO - FILE PROCESSOR

**Status:** ✅ Active & Ready
**Job ID:** dde2abeef641
**Created:** 2026-06-14
**Role:** Automated PDF file processing via web app

---

## 📋 DIKO Profile

**Name:** Diko (Dedicated Integration & Knowledge Operations)
**Function:** Process PDF checklist files through tester.sintelboo.my.id
**Availability:** 24/7 (Cronjob-based)
**Capabilities:**
- Navigate web app
- Upload PDF files
- Configure settings (format, activity type)
- Monitor processing
- Download results
- Report status with file listings

---

## 🎯 How to Use Diko

### Option 1: Direct Task Assignment
Send Diko a message with:
```
@diko process-files
Files: [list of PDF paths]
Format: BTP BD (default)
Activity: Perawatan (default)
```

### Option 2: Via Cronjob
```bash
hermes cronjob update dde2abeef641 \
  --prompt "Process files: /path/to/file1.pdf, /path/to/file2.pdf"
```

### Option 3: Scheduled Processing
```bash
hermes cronjob update dde2abeef641 \
  --schedule "0 9 * * *"  # Daily at 9 AM
```

---

## 📝 What Diko Does

### 1. File Upload
- Navigates to web app
- Selects format "BTP BD"
- Uploads PDF files
- Verifies upload success

### 2. Processing
- Waits for OCR completion
- Monitors progress
- Handles errors gracefully

### 3. Download & Report
- Downloads ZIP result
- Extracts file listing
- Reports all output files
- Flags any issues

### 4. Status Report
```
✅ Processing Complete
- Files uploaded: 5
- Files processed: 5
- Output files: 5
- Format: BPBKS17_Resor 1.21 Boo_...
- Download: [link or path]
```

---

## 🔧 Configuration

**Current Settings:**
- Web App: tester.sintelboo.my.id
- Format: BTP BD (Khusus Sintel Boo)
- Activity Type: Perawatan
- Toolsets: browser, file, web
- Deploy: origin (Telegram chat)

**To Change Settings:**
```bash
hermes cronjob update dde2abeef641 \
  --prompt "New instructions here..."
```

---

## 💡 Example Tasks for Diko

### Task 1: Process single file
```
Diko, process this file:
C:\Users\SINTEL 1.21 BOO\Downloads\6. JUNI\12-06-2026_PERAWATAN SERAT OPTIK 1 BULANAN_Bogor.pdf

Format: BTP BD
Wait for completion and download result.
```

### Task 2: Batch process multiple files
```
Diko, process all files in:
C:\Users\SINTEL 1.21 BOO\Downloads\6. JUNI\

Format: BTP BD
Activity: Perawatan
Report all outputs.
```

### Task 3: Daily scheduled processing
```
Diko, set up daily processing at 9 AM for:
C:\Users\SINTEL 1.21 BOO\Downloads\Daily\

Auto-download and save results to:
C:\Users\SINTEL 1.21 BOO\Results\
```

---

## 📊 Job Management

**List Jobs:**
```bash
hermes cronjob list | grep diko
```

**Pause Diko:**
```bash
hermes cronjob pause dde2abeef641
```

**Resume Diko:**
```bash
hermes cronjob resume dde2abeef641
```

**Update Diko:**
```bash
hermes cronjob update dde2abeef641 --schedule "30m"
```

**Remove Diko (if needed):**
```bash
hermes cronjob remove dde2abeef641
```

---

## 🎓 Key Features

✅ **Automated Processing** - No manual web app interaction needed
✅ **Error Handling** - Reports issues clearly
✅ **File Listing** - Shows all output files
✅ **Status Tracking** - Real-time progress updates
✅ **Batch Support** - Process multiple files at once
✅ **Scheduled Tasks** - Set recurring processing times
✅ **Result Delivery** - Saves/downloads results automatically

---

## ⚙️ System Integration

**Diko works with:**
- Web app: tester.sintelboo.my.id
- 38 kode ceklis (9 active + 29 template)
- BTP BD format (Sintel Boo specific)
- OCR detection engine
- Webhook auto-deploy

**Connected to:**
- GitHub: pangjaw/testerweb
- Cloud KAI: Source of truth for kode ceklis
- Telegram: Status delivery

---

## 🚀 Quick Start

1. **Give Diko a file path:**
   ```
   @diko Process: /path/to/checklist.pdf
   ```

2. **Diko will:**
   - Access the web app
   - Upload the file
   - Wait for processing
   - Download results
   - Report completion

3. **You receive:**
   - ✅ Status message
   - 📄 File listing
   - ⚠️ Any errors or warnings

---

**Diko is ready to work! Assign tasks anytime.** 🤖

Job ID: dde2abeef641
Status: ACTIVE
Mode: On-demand & Scheduled
