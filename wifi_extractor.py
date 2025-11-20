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
    """WiFi password extraction with elegant terminal display"""

    def __init__(self):
        self.system = platform.system()
        self.wifi_list: List[Dict[str, Optional[str]]] = []

    def clear_screen(self):
        """Clear terminal screen"""
        os.system('cls' if self.system == 'Windows' else 'clear')

    def get_terminal_width(self) -> int:
        """Get terminal width, default to 80"""
        try:
            return os.get_terminal_size().columns
        except:
            return 80

    def print_header(self):
        """Print elegant header"""
        self.clear_screen()
        width = min(self.get_terminal_width(), 80)

        print()
        print("+" + "-" * (width - 2) + "+")
        title = "WiFi Password Extractor"
        padding = (width - 2 - len(title)) // 2
        print("|" + " " * padding + title + " " * (width - 2 - padding - len(title)) + "|")

        subtitle = f"Platform: {self.system}"
        padding = (width - 2 - len(subtitle)) // 2
        print("|" + " " * padding + subtitle + " " * (width - 2 - padding - len(subtitle)) + "|")
        print("+" + "-" * (width - 2) + "+")
        print()

    def print_status(self, message: str, status: str = "info"):
        """Print status message with symbol"""
        symbols = {
            "info": "[*]",
            "success": "[+]",
            "error": "[!]",
            "warning": "[!]"
        }
        print(f"{symbols.get(status, '[*]')} {message}")

    def extract_wifi_passwords(self) -> List[Dict[str, Optional[str]]]:
        """Extract WiFi passwords based on OS"""
        if self.system == "Windows":
            return self._extract_windows()
        elif self.system == "Linux":
            return self._extract_linux()
        elif self.system == "Darwin":
            return self._extract_macos()
        else:
            self.print_status(f"Unsupported OS: {self.system}", "error")
            return []

    def _extract_windows(self) -> List[Dict[str, Optional[str]]]:
        """Extract WiFi passwords on Windows"""
        try:
            output = subprocess.run(
                ["netsh", "wlan", "show", "profiles"],
                capture_output=True, text=True, check=True
            ).stdout

            profiles = re.findall(r"All User Profile\s+:\s+(.*)", output)

            if not profiles:
                return []

            self.print_status(f"Found {len(profiles)} profile(s), extracting...", "info")

            for name in profiles:
                name = name.strip()

                info = subprocess.run(
                    ["netsh", "wlan", "show", "profiles", name],
                    capture_output=True, text=True, check=True
                ).stdout

                if re.search(r"Security key\s+:\s+Absent", info):
                    continue

                info_pass = subprocess.run(
                    ["netsh", "wlan", "show", "profiles", name, "key=clear"],
                    capture_output=True, text=True, check=True
                ).stdout

                match = re.search(r"Key Content\s+:\s+(.*)", info_pass)
                password = match.group(1).strip() if match else None

                self.wifi_list.append({"ssid": name, "password": password})

            return self.wifi_list

        except Exception as e:
            self.print_status(f"Error: {e}", "error")
            return []

    def _extract_linux(self) -> List[Dict[str, Optional[str]]]:
        """Extract WiFi passwords on Linux"""
        # Try nmcli first
        try:
            subprocess.run(["which", "nmcli"], capture_output=True, check=True)

            connections = subprocess.run(
                ["nmcli", "-t", "-f", "NAME,TYPE", "connection", "show"],
                capture_output=True, text=True, check=True
            ).stdout

            wifi_conns = [
                line.split(':')[0]
                for line in connections.strip().split('\n')
                if '802-11-wireless' in line or 'wifi' in line
            ]

            if wifi_conns:
                self.print_status(f"Found {len(wifi_conns)} connection(s) via NetworkManager", "info")

                for conn in wifi_conns:
                    try:
                        psk = subprocess.run(
                            ["nmcli", "-s", "-g", "802-11-wireless-security.psk",
                             "connection", "show", conn],
                            capture_output=True, text=True, check=True
                        ).stdout.strip()

                        self.wifi_list.append({
                            "ssid": conn,
                            "password": psk if psk else None
                        })
                    except:
                        continue

                return self.wifi_list

        except:
            pass

        # Fallback: read config files
        try:
            nm_path = Path("/etc/NetworkManager/system-connections")

            if nm_path.exists() and os.access(nm_path, os.R_OK):
                configs = list(nm_path.glob("*"))

                if configs:
                    self.print_status(f"Found {len(configs)} config file(s)", "info")

                    for cfg in configs:
                        try:
                            content = cfg.read_text()

                            ssid_match = re.search(r'(?:ssid|id)=(.+)', content)
                            if not ssid_match:
                                continue

                            psk_match = re.search(r'psk=(.+)', content)

                            self.wifi_list.append({
                                "ssid": ssid_match.group(1).strip(),
                                "password": psk_match.group(1).strip() if psk_match else None
                            })
                        except:
                            continue

                    return self.wifi_list

        except:
            pass

        self.print_status("Could not extract passwords. Run with sudo.", "error")
        return []

    def _extract_macos(self) -> List[Dict[str, Optional[str]]]:
        """Extract WiFi passwords on macOS"""
        try:
            prefs = subprocess.run(
                ["defaults", "read",
                 "/Library/Preferences/SystemConfiguration/com.apple.airport.preferences",
                 "KnownNetworks"],
                capture_output=True, text=True, check=True
            ).stdout

            ssids = re.findall(r'SSID_STR\s*=\s*"?([^";]+)"?', prefs)

            if not ssids:
                self.print_status("No saved networks found", "warning")
                return []

            self.print_status(f"Found {len(ssids)} network(s), extracting...", "info")

            for ssid in set(ssids):
                try:
                    password = subprocess.run(
                        ["security", "find-generic-password",
                         "-D", "AirPort network password",
                         "-a", ssid, "-w"],
                        capture_output=True, text=True, check=True
                    ).stdout.strip()

                    self.wifi_list.append({
                        "ssid": ssid,
                        "password": password if password else None
                    })
                except:
                    continue

            return self.wifi_list

        except Exception as e:
            self.print_status(f"Error: {e}", "error")
            self.print_status("Grant Terminal access to Keychain in System Preferences", "info")
            return []

    def display_results(self):
        """Display results in elegant table format"""
        if not self.wifi_list:
            print()
            self.print_status("No WiFi credentials found", "warning")
            return

        width = min(self.get_terminal_width(), 80)

        # Calculate column widths
        ssid_width = max(len(w['ssid']) for w in self.wifi_list)
        ssid_width = max(ssid_width, 10)  # minimum width
        pass_width = max(len(w['password'] or 'N/A') for w in self.wifi_list)
        pass_width = max(pass_width, 10)

        # Adjust if too wide
        total = ssid_width + pass_width + 10
        if total > width - 4:
            ssid_width = (width - 14) // 2
            pass_width = (width - 14) // 2

        print()
        print("+" + "-" * (width - 2) + "+")

        header = f" Found {len(self.wifi_list)} WiFi Credential(s) "
        padding = (width - 2 - len(header)) // 2
        print("|" + " " * padding + header + " " * (width - 2 - padding - len(header)) + "|")

        print("+" + "-" * (width - 2) + "+")

        # Table header
        print(f"| {'#':>3} | {'SSID':<{ssid_width}} | {'Password':<{pass_width}} |")
        print("|" + "-" * 5 + "+" + "-" * (ssid_width + 2) + "+" + "-" * (pass_width + 2) + "|")

        # Table rows
        for idx, wifi in enumerate(self.wifi_list, 1):
            ssid = wifi['ssid'][:ssid_width] if len(wifi['ssid']) > ssid_width else wifi['ssid']
            password = wifi['password'] or 'N/A'
            password = password[:pass_width] if len(password) > pass_width else password

            print(f"| {idx:>3} | {ssid:<{ssid_width}} | {password:<{pass_width}} |")

        print("+" + "-" * (width - 2) + "+")
        print()


def main():
    """Main function"""
    extractor = WiFiExtractor()
    extractor.print_header()

    # Check privileges on Unix systems
    if extractor.system in ["Linux", "Darwin"]:
        if os.geteuid() != 0:
            extractor.print_status("Warning: May require sudo for full access", "warning")
            print()

    extractor.print_status("Extracting WiFi credentials...", "info")
    print()

    # Extract and display
    extractor.extract_wifi_passwords()
    extractor.display_results()

    extractor.print_status("Done", "success")
    print()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n")
        print("[!] Interrupted")
        sys.exit(0)
    except Exception as e:
        print(f"\n[!] Error: {e}")
        sys.exit(1)
