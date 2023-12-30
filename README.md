# Informasi
Program berbasis CLI untuk cek riwayat koneksi wifi.
Hanya untuk WINDOWS. Tidak untuk LINUX.

Alur program :
  - Request cmd -> netsh wlan show profile
  - Kemudian record hasil (disimpan ke variabel)
  - Setelah itu lakukan looping dengan request cmd kembali
  - netsh wlan show profile name="{hasil record poin 2}" key=clear
  - Jika wifi tersebut login via web / key security : absent
  - Maka akan di skip, Program akan mencari wifi yang ada passwordnya
  - Setelah menemukan akan di simpan ke dalam file.

# Instalasi
1. Lakukan update dan upgrade
```bash
apt update && apt upgrade -y
```
2. Install python dan git
```bash
apt install python git -y
```
3. Download repositories dengan command :
```bash
git clone https://github.com/syauqqii/HistoryWifi
```
4. Masuk ke folder HistoryWifi
```bash
cd HistoryWifi
```
5. Run program
```python3
python cek.py
```

# note
Mungkin di beberapa device membutuhkan installasi library subprocess
```python3
pip install subprocess
```
