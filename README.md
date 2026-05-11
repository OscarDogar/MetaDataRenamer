<div align="center">
  <img width="250" src="https://github.com/OscarDogar/MetaDataRenamer/assets/60854050/5c157e98-daea-47cc-88fc-791b1f222074"/>
  
  <h1>🏷️ MetaDataRenamer</h1>
  <h3>Advanced MKV Metadata Editing Tool</h3>
  <p>A powerful utility to rename, replace, or clean metadata in audio tracks, subtitles, attachments, and video titles.</p>

  <img src="https://img.shields.io/github/stars/OscarDogar/MetaDataRenamer?style=for-the-badge&color=facc15" />
  <img src="https://img.shields.io/github/downloads/OscarDogar/MetaDataRenamer/total?style=for-the-badge&color=38bdf8" />
  <img src="https://img.shields.io/badge/MKVToolNix-required-blue?style=for-the-badge" />
  <img src="https://img.shields.io/badge/license-GPL--3.0-green?style=for-the-badge" />
</div>

---

# 🚀 Overview

MetaDataRenamer helps you **automate and simplify MKV metadata editing**.

It allows you to:
- 🎧 Rename audio track titles  
- 📝 Modify subtitle names  
- 📎 Edit attachments metadata  
- 🎬 Replace embedded titles  
- 📁 Process entire folders in batch  

---

# 🧩 Requirements

## 🛠️ System Requirements

- 👉 [MKVToolNix](https://mkvtoolnix.download/downloads.html)
- 👉 Add MKVToolNix to system PATH (Windows)

## 📦 Python Dependencies

```bash
pip install -r requirements.txt
```

---

# ⚙️ Setup

1. Install **MKVToolNix**
2. Add it to system PATH
3. Install Python dependencies
4. Run the program

---

# 🎯 How It Works

## 1️⃣ Define Keywords

Edit your `.env` file:

```env
KEYWORDS=test
```

This defines the metadata text you want to search and replace.

---

## 2️⃣ Run the Program

When you run it, it will ask:

### 📂 Folder Path
```txt
C:\Users\myuser\Videos\
```

### ✏️ Replacement Text
```txt
new name
```

---

## 3️⃣ Processing Flow

The tool will:
- Scan all `.mkv` files in the folder
- Detect matching metadata fields
- Replace keyword occurrences
- Apply changes automatically

---

# 🧪 Example

## Before
```txt
test subtitle track
test audio title
```

## Configuration
```env
KEYWORDS=test
```

## After
```txt
new name subtitle track
new name audio title
```

---

# 🎬 Visual Example

<div align="center">

### 🔎 Before
<img src="https://github.com/OscarDogar/MetaDataRenamer/assets/60854050/3ad36852-c737-44c9-9b77-52b6c5fcab43" width="650"/>

### ⚡ After
<img src="https://github.com/OscarDogar/MetaDataRenamer/assets/60854050/6a2b417b-162d-47da-a108-b375258d6067" width="650"/>

</div>

---

# 🧠 Supported Metadata Types

- 🎧 Audio track names  
- 📝 Subtitle track titles  
- 📎 Attachments  
- 🎬 Video titles  
- 🏷️ MKV metadata fields  

---

# 📂 Use Cases

Perfect for:

- 🎥 Media library organization (Plex / Jellyfin / Kodi)
- 📺 Subtitle cleanup
- 🎧 Audio track standardization
- 📦 Bulk MKV metadata fixing
- 🗂️ Downloaded content organization

---

# ⚠️ Important Notes

- MKVToolNix must be installed and accessible via PATH  
- Use precise keywords to avoid unintended replacements  
- Always backup files before batch processing  
- Only supports `.mkv` files  

---

# 🔥 Features

- ⚡ Fast batch processing  
- 🧩 Keyword-based replacement system  
- 📁 Folder-wide automation  
- 🎯 Precise metadata targeting  
- 🧠 Smart MKV stream detection  
- 🔄 Safe repeatable operations  

---

# 🤝 Contributing

Contributions are welcome:

- 🐛 Report bugs  
- 💡 Suggest features  
- 🔧 Submit pull requests  

---

# ❤️ Support

If this project helps you, consider supporting it:

<div align="center">

<a href="https://github.com/sponsors/OscarDogar">
  <img src="https://img.shields.io/badge/Sponsor%20on%20GitHub-EA4AAA?style=for-the-badge&logo=githubsponsors&logoColor=white" />
</a>

</div>

---

# 📜 License

This project is licensed under the **GNU General Public License v3.0 (GPL-3.0)**.

You are free to:
- ✔️ Use  
- ✔️ Modify  
- ✔️ Distribute  

But:
- 🔒 Must keep source open when distributing  
- 🔒 Derivatives must use GPL-3.0  
- 🔒 License must be preserved  

👉 https://www.gnu.org/licenses/gpl-3.0.html

---

<div align="center">

### ⭐ If you like this project, consider giving it a star!

</div>
