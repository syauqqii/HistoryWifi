import re, subprocess
from os import system

def main():
	system("cls")
	system("title Program Cek Riwayat Koneksi WiFi")
	system("MODE CON: COLS=70 LINES=5")
	print("$ Program Cek Riwayat Koneksi WiFi")
	command_output 	= subprocess.run(["netsh","wlan","show","profiles"], capture_output=True).stdout.decode()
	profile_names	= (re.findall("All User Profile     : (.*)\r", command_output))
	wifi_list 		= []
	if len(profile_names) != 0:
		for name in profile_names:
			wifi_profile	= {}
			profile_info	= subprocess.run(["netsh","wlan","show","profiles", name], capture_output=True).stdout.decode()
			if re.search("Security key           : Absent", profile_info):
				continue
			else:
				wifi_profile["ssid"]	= name
				profile_info_pass		= subprocess.run(["netsh","wlan","show","profiles", name, "key=clear"], capture_output=True).stdout.decode()
				password				= re.search("Key Content            : (.*)\r", profile_info_pass)
				if password == None:
					wifi_profile["password"] = None
				else:
					wifi_profile["password"] = password[1]
				wifi_list.append(wifi_profile)
	nama_file = "wifi.txt"
	try:
		file_wifi = open(nama_file, "w")
	except:
		system("fsutil file creatnew wifi.txt 555")
		nama_file = "wifi.txt"
		file_wifi = open(nama_file, "w")
	for x in range(len(wifi_list)):
		if (x+1) < 10:
			format_text = f"[0{x+1}] Wifi Name : {wifi_list[x]['ssid']}\n[0{x+1}] Password  : {wifi_list[x]['password']}\n\n"
		else:
			format_text = f"[{x+1}] Wifi Name : {wifi_list[x]['ssid']}\n[{x+1}] Password  : {wifi_list[x]['password']}\n\n"
		file_wifi.write(str(format_text))
	file_wifi.close()
	print(f"$ {len(wifi_list)} data berhasil di simpan ke dalam file : ", end='')
	load(nama_file)
	print("$ Tekan apa saja untuk keluar.\n")
	system("pause > 1")

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		system("cls")
		exit()
