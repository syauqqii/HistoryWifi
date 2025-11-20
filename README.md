# WiFi Password Extractor

Program CLI untuk mengekstrak riwayat koneksi WiFi dan password yang tersimpan di sistem.

**Platform Support:** Windows | Linux | macOS

## Quick Start

```bash
# Clone repository
git clone https://github.com/syauqqii/HistoryWifi
cd HistoryWifi

# Run (Linux/macOS - requires sudo)
sudo python3 wifi_extractor.py

# Run (Windows - run as Administrator)
python wifi_extractor.py
```

## Requirements

- Python 3.6+
- Linux: NetworkManager (pre-installed di most distros)
- Akses root/Administrator

## How It Works

| Platform | Method |
|----------|--------|
| Windows | `netsh wlan` commands |
| Linux | NetworkManager CLI (`nmcli`) or config files (`/etc/NetworkManager/system-connections/`) |
| macOS | Keychain access (`security` command) |

Program otomatis mendeteksi OS dan menggunakan metode yang sesuai.

## Output

Hasil langsung ditampilkan di terminal dalam format tabel:

```
+------------------------------------------------------------------------------+
|                        Found 3 WiFi Credential(s)                            |
+------------------------------------------------------------------------------+
|   # | SSID                 | Password             |
|-----+----------------------+----------------------|
|   1 | HomeNetwork          | mypassword123        |
|   2 | OfficeWiFi           | office2024           |
|   3 | CafeHotspot          | N/A                  |
+------------------------------------------------------------------------------+
```

## Troubleshooting

**Linux: No results found**
```bash
# Pastikan running dengan sudo
sudo python3 wifi_extractor.py

# Check NetworkManager status
systemctl status NetworkManager
```

**macOS: Permission denied**
```bash
# Run dengan sudo
sudo python3 wifi_extractor.py

# Atau grant Terminal access:
# System Preferences > Security & Privacy > Privacy > Full Disk Access > Add Terminal
```

**Windows: No profiles found**
- Run Command Prompt as Administrator
- Check WiFi profiles: `netsh wlan show profiles`

## Features

- Multi-platform support (Windows, Linux, macOS)
- Auto OS detection
- Multiple extraction methods dengan fallback
- Proper error handling
- UTF-8 support

## Security Warning

Program ini hanya untuk recovery password WiFi pribadi. File output berisi password dalam plain text - jaga keamanannya. Jangan gunakan untuk mengakses jaringan tanpa izin.

## License

MIT License

## Author

syauqqii
