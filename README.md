# WiFi History & Password Extractor

Program berbasis CLI untuk melihat dan mengekstrak riwayat koneksi WiFi beserta password-nya.

**Multi-Platform Support**: Windows, Linux, macOS

## Fitur

- ✅ **Multi-Platform**: Mendukung Windows, Linux, dan macOS
- ✅ **Otomatis Mendeteksi OS**: Secara otomatis menggunakan metode yang sesuai dengan sistem operasi
- ✅ **Mudah Digunakan**: Interface CLI yang sederhana dan informatif
- ✅ **Export ke File**: Hasil otomatis disimpan ke file `wifi.txt`
- ✅ **Error Handling**: Penanganan error yang lebih baik
- ✅ **Multiple Methods**: Mendukung berbagai metode ekstraksi di Linux

## Cara Kerja

### Windows
- Menggunakan command `netsh wlan show profiles` untuk mendapatkan daftar WiFi
- Mengekstrak password dengan `netsh wlan show profile name="{SSID}" key=clear`

### Linux
- **Metode 1**: Menggunakan `nmcli` (NetworkManager CLI)
- **Metode 2**: Membaca file konfigurasi di `/etc/NetworkManager/system-connections/`
- Mendukung berbagai distro Linux dengan NetworkManager

### macOS
- Menggunakan command `security` untuk mengakses Keychain
- Membaca preferensi WiFi dari system configuration

## Instalasi

### 1. Clone Repository

```bash
git clone https://github.com/syauqqii/HistoryWifi
cd HistoryWifi
```

### 2. Pastikan Python Terinstall

Program ini membutuhkan Python 3.6 atau lebih baru.

**Cek versi Python:**
```bash
python3 --version
```

**Install Python (jika belum ada):**

- **Linux (Debian/Ubuntu):**
  ```bash
  sudo apt update
  sudo apt install python3 python3-pip -y
  ```

- **Linux (Fedora/RHEL):**
  ```bash
  sudo dnf install python3 python3-pip -y
  ```

- **macOS:**
  ```bash
  brew install python3
  ```

- **Windows:**
  Download dari [python.org](https://www.python.org/downloads/)

## Penggunaan

### Windows

```cmd
python cek.py
```

atau

```cmd
python3 cek.py
```

### Linux

**PENTING**: Di Linux, script ini membutuhkan akses root untuk membaca password WiFi.

```bash
sudo python3 cek.py
```

**Catatan untuk Linux:**
- Pastikan NetworkManager terinstall (sudah ada di kebanyakan distro modern)
- Jika menggunakan distro tanpa NetworkManager, password mungkin tidak bisa diekstrak
- Untuk Ubuntu/Debian: `sudo apt install network-manager`

### macOS

```bash
sudo python3 cek.py
```

**Catatan untuk macOS:**
- Anda mungkin perlu memberikan akses Terminal ke Keychain
- Sistem mungkin meminta password administrator
- Buka System Preferences → Security & Privacy jika ada masalah akses

## Output

Program akan:
1. Menampilkan informasi WiFi yang ditemukan di terminal
2. Menyimpan hasil ke file `wifi.txt` di folder yang sama

**Format output `wifi.txt`:**
```
======================================================================
                    WiFi Credentials Export
                      Platform: Linux
======================================================================

[01] WiFi Name : MyHomeWiFi
[01] Password  : mypassword123

[02] WiFi Name : OfficeNetwork
[02] Password  : office2024

```

## Persyaratan Sistem

### Windows
- Windows 7 atau lebih baru
- Python 3.6+
- Akses Administrator (untuk beberapa WiFi profile)

### Linux
- Kernel Linux 2.6+
- Python 3.6+
- NetworkManager (untuk metode nmcli)
- Akses root/sudo

**Distro yang didukung:**
- Ubuntu 16.04+
- Debian 9+
- Fedora 25+
- CentOS 7+
- Arch Linux
- Dan distro lain yang menggunakan NetworkManager

### macOS
- macOS 10.10 (Yosemite) atau lebih baru
- Python 3.6+
- Akses sudo/Administrator

## Troubleshooting

### Tidak Ada Hasil Ditemukan (Linux)

1. **Pastikan menjalankan dengan sudo:**
   ```bash
   sudo python3 cek.py
   ```

2. **Cek apakah NetworkManager berjalan:**
   ```bash
   systemctl status NetworkManager
   ```

3. **Pastikan NetworkManager terinstall:**
   ```bash
   sudo apt install network-manager  # Debian/Ubuntu
   sudo dnf install NetworkManager    # Fedora/RHEL
   ```

### Permission Denied (macOS)

1. Jalankan dengan sudo:
   ```bash
   sudo python3 cek.py
   ```

2. Berikan akses Terminal ke Keychain:
   - Buka System Preferences → Security & Privacy
   - Tab Privacy → Full Disk Access
   - Tambahkan Terminal

### Error di Windows

1. Jalankan Command Prompt sebagai Administrator
2. Pastikan WiFi adapter aktif
3. Cek apakah ada WiFi profile tersimpan:
   ```cmd
   netsh wlan show profiles
   ```

## Keamanan & Privacy

- ⚠️ Program ini hanya mengekstrak WiFi credentials dari komputer Anda sendiri
- ⚠️ File `wifi.txt` berisi password dalam plain text - jaga keamanannya!
- ⚠️ Jangan share file output ke orang lain
- ⚠️ Hapus file `wifi.txt` setelah selesai digunakan
- ✅ Program ini tidak mengirim data ke internet
- ✅ Semua proses dilakukan secara lokal

## Improvements dari Versi Sebelumnya

### Yang Baru:
1. ✅ **Dukungan Multi-Platform** - Windows, Linux, macOS
2. ✅ **Code Structure Lebih Baik** - Menggunakan OOP (Object-Oriented Programming)
3. ✅ **Error Handling** - Penanganan error yang lebih robust
4. ✅ **Type Hints** - Python type annotations untuk kode yang lebih maintainable
5. ✅ **Multiple Extraction Methods** - Fallback ke metode alternatif jika metode utama gagal
6. ✅ **Better User Feedback** - Progress indicator dan pesan yang lebih informatif
7. ✅ **Cross-Platform UI** - Tidak lagi menggunakan Windows-specific commands
8. ✅ **Privilege Detection** - Otomatis cek dan warn jika tidak punya akses yang cukup
9. ✅ **UTF-8 Support** - Mendukung SSID dengan karakter non-ASCII
10. ✅ **Better Documentation** - Komentar kode yang lengkap dan README yang comprehensive

### Perbaikan Teknis:
- Menggunakan `subprocess.run()` dengan proper error handling
- Platform detection menggunakan `platform.system()`
- Modular design dengan method terpisah untuk setiap OS
- Proper exception handling dengan specific error messages
- No more hard-coded Windows commands
- Better regex patterns untuk ekstraksi data
- File I/O dengan context managers (`with` statement)

## Dependencies

Program ini hanya menggunakan Python standard library, tidak ada external dependencies:
- `re` - Regular expressions
- `subprocess` - Menjalankan system commands
- `platform` - Deteksi OS
- `os` - System operations
- `sys` - System-specific parameters
- `typing` - Type hints
- `pathlib` - Object-oriented filesystem paths

## Lisensi

MIT License - Bebas digunakan untuk keperluan personal dan edukasi.

## Kontribusi

Kontribusi sangat welcome! Silakan:
1. Fork repository ini
2. Buat branch baru (`git checkout -b feature/AmazingFeature`)
3. Commit perubahan (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buat Pull Request

## Author

**syauqqii**

## Disclaimer

⚠️ **PENTING**: Program ini dibuat untuk tujuan edukasi dan recovery password WiFi pribadi. Pengguna bertanggung jawab penuh atas penggunaan program ini. Jangan gunakan untuk tujuan ilegal atau mengakses jaringan WiFi tanpa izin.

---

**Star ⭐ repository ini jika bermanfaat!**
