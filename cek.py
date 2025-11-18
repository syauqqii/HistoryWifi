#!/usr/bin/env python3
"""
WiFi History & Password Extractor
Multi-platform support: Windows, Linux, macOS
"""

import re
import subprocess
import platform
import os
import sys
from typing import List, Dict, Optional
from pathlib import Path


class WiFiExtractor:
    """Base class for WiFi password extraction"""

    def __init__(self):
        self.system = platform.system()
        self.wifi_list: List[Dict[str, Optional[str]]] = []

    def clear_screen(self):
        """Clear terminal screen in a cross-platform way"""
        os.system('cls' if self.system == 'Windows' else 'clear')

    def print_banner(self):
        """Print program banner"""
        self.clear_screen()
        print("=" * 70)
        print(" " * 15 + "WiFi History & Password Extractor")
        print(" " * 20 + f"Platform: {self.system}")
        print("=" * 70)
        print()

    def extract_wifi_passwords(self) -> List[Dict[str, Optional[str]]]:
        """Extract WiFi passwords based on the current OS"""
        if self.system == "Windows":
            return self._extract_windows()
        elif self.system == "Linux":
            return self._extract_linux()
        elif self.system == "Darwin":  # macOS
            return self._extract_macos()
        else:
            print(f"[!] Unsupported operating system: {self.system}")
            return []

    def _extract_windows(self) -> List[Dict[str, Optional[str]]]:
        """Extract WiFi passwords on Windows using netsh"""
        try:
            # Get all WiFi profiles
            command_output = subprocess.run(
                ["netsh", "wlan", "show", "profiles"],
                capture_output=True,
                text=True,
                check=True
            ).stdout

            profile_names = re.findall(r"All User Profile\s+:\s+(.*)", command_output)

            if not profile_names:
                print("[!] No WiFi profiles found.")
                return []

            print(f"[+] Found {len(profile_names)} WiFi profile(s). Extracting passwords...")

            for name in profile_names:
                name = name.strip()
                wifi_profile = {}

                # Check if profile has a password
                profile_info = subprocess.run(
                    ["netsh", "wlan", "show", "profiles", name],
                    capture_output=True,
                    text=True,
                    check=True
                ).stdout

                if re.search(r"Security key\s+:\s+Absent", profile_info):
                    continue

                wifi_profile["ssid"] = name

                # Get password
                profile_info_pass = subprocess.run(
                    ["netsh", "wlan", "show", "profiles", name, "key=clear"],
                    capture_output=True,
                    text=True,
                    check=True
                ).stdout

                password_match = re.search(r"Key Content\s+:\s+(.*)", profile_info_pass)
                wifi_profile["password"] = password_match.group(1).strip() if password_match else None

                self.wifi_list.append(wifi_profile)

            return self.wifi_list

        except subprocess.CalledProcessError as e:
            print(f"[!] Error executing command: {e}")
            return []
        except Exception as e:
            print(f"[!] Unexpected error on Windows: {e}")
            return []

    def _extract_linux(self) -> List[Dict[str, Optional[str]]]:
        """Extract WiFi passwords on Linux"""
        # Try multiple methods for Linux
        methods = [
            self._extract_linux_nmcli,
            self._extract_linux_config_files
        ]

        for method in methods:
            try:
                result = method()
                if result:
                    return result
            except Exception as e:
                continue

        print("[!] Could not extract WiFi passwords on Linux.")
        print("[!] Make sure you run this script with sudo/root privileges.")
        print("[!] Supported: NetworkManager, system connection files")
        return []

    def _extract_linux_nmcli(self) -> List[Dict[str, Optional[str]]]:
        """Extract WiFi passwords using nmcli (NetworkManager)"""
        try:
            # Check if nmcli is available
            subprocess.run(["which", "nmcli"], capture_output=True, check=True)

            # Get list of saved connections
            connections = subprocess.run(
                ["nmcli", "-t", "-f", "NAME,TYPE", "connection", "show"],
                capture_output=True,
                text=True,
                check=True
            ).stdout

            wifi_connections = [
                line.split(':')[0]
                for line in connections.strip().split('\n')
                if '802-11-wireless' in line or 'wifi' in line
            ]

            if not wifi_connections:
                return []

            print(f"[+] Found {len(wifi_connections)} WiFi connection(s) using NetworkManager...")

            for conn_name in wifi_connections:
                try:
                    # Get password for each connection
                    conn_details = subprocess.run(
                        ["nmcli", "-s", "-g", "802-11-wireless-security.psk",
                         "connection", "show", conn_name],
                        capture_output=True,
                        text=True,
                        check=True
                    ).stdout.strip()

                    wifi_profile = {
                        "ssid": conn_name,
                        "password": conn_details if conn_details else None
                    }
                    self.wifi_list.append(wifi_profile)
                except:
                    continue

            return self.wifi_list

        except subprocess.CalledProcessError:
            return []
        except FileNotFoundError:
            return []

    def _extract_linux_config_files(self) -> List[Dict[str, Optional[str]]]:
        """Extract WiFi passwords from NetworkManager config files"""
        try:
            nm_connections_path = Path("/etc/NetworkManager/system-connections")

            if not nm_connections_path.exists():
                return []

            # Check if we have read permissions
            if not os.access(nm_connections_path, os.R_OK):
                print("[!] No permission to read NetworkManager files. Try running with sudo.")
                return []

            config_files = list(nm_connections_path.glob("*"))

            if not config_files:
                return []

            print(f"[+] Found {len(config_files)} connection file(s) in NetworkManager...")

            for config_file in config_files:
                try:
                    with open(config_file, 'r') as f:
                        content = f.read()

                    # Extract SSID
                    ssid_match = re.search(r'(?:ssid|id)=(.+)', content)
                    if not ssid_match:
                        continue

                    ssid = ssid_match.group(1).strip()

                    # Extract password (psk)
                    password_match = re.search(r'psk=(.+)', content)
                    password = password_match.group(1).strip() if password_match else None

                    wifi_profile = {
                        "ssid": ssid,
                        "password": password
                    }
                    self.wifi_list.append(wifi_profile)

                except Exception as e:
                    continue

            return self.wifi_list

        except Exception as e:
            return []

    def _extract_macos(self) -> List[Dict[str, Optional[str]]]:
        """Extract WiFi passwords on macOS using security command"""
        try:
            # Get list of preferred WiFi networks
            airport_prefs = subprocess.run(
                ["defaults", "read",
                 "/Library/Preferences/SystemConfiguration/com.apple.airport.preferences",
                 "KnownNetworks"],
                capture_output=True,
                text=True,
                check=True
            ).stdout

            # Extract SSIDs
            ssids = re.findall(r'SSID_STR\s*=\s*"?([^";]+)"?', airport_prefs)

            if not ssids:
                # Alternative method: use airport utility
                airport_output = subprocess.run(
                    ["/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport",
                     "-s"],
                    capture_output=True,
                    text=True
                ).stdout

                # Parse networks (this won't give us saved networks, just visible ones)
                # We'll try to get passwords for common networks
                print("[!] Limited WiFi information available on macOS.")
                print("[!] Trying to extract saved network passwords...")

            print(f"[+] Found {len(ssids)} WiFi network(s). Extracting passwords...")

            for ssid in set(ssids):  # Remove duplicates
                try:
                    # Get password from keychain
                    password_output = subprocess.run(
                        ["security", "find-generic-password",
                         "-D", "AirPort network password",
                         "-a", ssid, "-w"],
                        capture_output=True,
                        text=True,
                        check=True
                    ).stdout.strip()

                    wifi_profile = {
                        "ssid": ssid,
                        "password": password_output if password_output else None
                    }
                    self.wifi_list.append(wifi_profile)

                except subprocess.CalledProcessError:
                    # Password not found or access denied
                    continue

            return self.wifi_list

        except Exception as e:
            print(f"[!] Error on macOS: {e}")
            print("[!] You may need to grant Terminal access to Keychain in System Preferences.")
            return []

    def save_to_file(self, filename: str = "wifi.txt"):
        """Save WiFi credentials to a file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("=" * 70 + "\n")
                f.write(" " * 20 + "WiFi Credentials Export\n")
                f.write(" " * 22 + f"Platform: {self.system}\n")
                f.write("=" * 70 + "\n\n")

                for idx, wifi in enumerate(self.wifi_list, 1):
                    f.write(f"[{idx:02d}] WiFi Name : {wifi['ssid']}\n")
                    f.write(f"[{idx:02d}] Password  : {wifi['password'] or 'N/A'}\n")
                    f.write("\n")

            print(f"\n[+] {len(self.wifi_list)} credential(s) saved to: {filename}")
            return True

        except Exception as e:
            print(f"[!] Error saving to file: {e}")
            return False

    def display_results(self):
        """Display results in terminal"""
        if not self.wifi_list:
            print("\n[!] No WiFi credentials found.")
            return

        print("\n" + "=" * 70)
        print(f" Found {len(self.wifi_list)} WiFi Credential(s)")
        print("=" * 70 + "\n")

        for idx, wifi in enumerate(self.wifi_list, 1):
            print(f"[{idx:02d}] SSID     : {wifi['ssid']}")
            print(f"     Password : {wifi['password'] or 'N/A'}")
            print()


def main():
    """Main function"""
    extractor = WiFiExtractor()
    extractor.print_banner()

    # Check for root/admin privileges on Linux/macOS
    if extractor.system in ["Linux", "Darwin"]:
        if os.geteuid() != 0:
            print("[!] WARNING: This script may require root/sudo privileges.")
            print("[!] If no results are found, try running: sudo python3 cek.py\n")

    print("[*] Extracting WiFi credentials...\n")

    # Extract passwords
    wifi_list = extractor.extract_wifi_passwords()

    # Display results
    extractor.display_results()

    # Save to file
    if wifi_list:
        extractor.save_to_file()

    print("\n[*] Done!")

    # Platform-specific exit prompt
    if extractor.system == "Windows":
        os.system("pause")
    else:
        input("\nPress Enter to exit...")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Interrupted by user. Exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\n[!] Unexpected error: {e}")
        sys.exit(1)
