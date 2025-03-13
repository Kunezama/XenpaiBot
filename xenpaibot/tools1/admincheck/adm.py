import requests
from colorama import Fore, init
import sys
import os

init(autoreset=True)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))


SEARCH_DIRS = [
    BASE_DIR,  
    os.path.join(BASE_DIR, "xenpaibot", "tools1", "admincheck"),  
]

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    try:
        clear_screen()
        print(Fore.CYAN + r"""
              
              _           _          _____ _               _    
     /\      | |         (_)        / ____| |             | |   
    /  \   __| |_ __ ___  _ _ __   | |    | |__   ___  ___| | __
   / /\ \ / _` | '_ ` _ \| | '_ \  | |    | '_ \ / _ \/ __| |/ /
  / ____ \ (_| | | | | | | | | | | | |____| | | |  __/ (__|   < 
 /_/    \_\__,_|_| |_| |_|_|_| |_|  \_____|_| |_|\___|\___|_|\_\\
                                                             
           """ + Fore.MAGENTA + "XenpaiBot -" + Fore.WHITE + " Admin Panel Checker")
    except Exception as e:
        print(Fore.RED + f"[ERROR] Failed to display banner: {e}")

def find_file(filename):
    for directory in SEARCH_DIRS:
        file_path = os.path.join(directory, filename)
        print(Fore.YELLOW + f"[DEBUG] Checking: {file_path}")  # Debug untuk cek lokasi file
        
        if os.path.exists(file_path):
            print(Fore.BLUE + f"[DEBUG] Found '{filename}' in {directory}")
            return file_path
    return None

def load_list(filename):
    """Membaca file dari direktori yang ditemukan"""
    file_path = find_file(filename)

    if file_path:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = [line.strip() for line in f if line.strip()]
            if lines:
                print(Fore.GREEN + f"[DEBUG] '{filename}' loaded successfully ({len(lines)} entries)")
            else:
                print(Fore.RED + f"[ERROR] '{filename}' is empty!")
            return lines
        except Exception as e:
            print(Fore.RED + f"[ERROR] Gagal membaca '{filename}': {e}")
            return []
    else:
        print(Fore.RED + f"[ERROR] File '{filename}' tidak ditemukan di lokasi yang dicari.")
        return []

def save_result(url):
    result_file = os.path.join(BASE_DIR, "Results-adminpanel.txt")
    try:
        with open(result_file, "a", encoding="utf-8") as f:
            f.write(url + "\n")
        print(Fore.GREEN + f"[SAVED] Successfully saved: {url}")
    except Exception as e:
        print(Fore.RED + f"[ERROR] Failed to save result: {e}")

def check_admin_panel(targets, admin_paths):
    print(Fore.CYAN + "\n[INFO] Starting admin panel check...\n")
    
    try:
        for target in targets:
            print(Fore.YELLOW + f"\n[TARGET] {target}")
            
            for path in admin_paths:
                url = f"{target.rstrip('/')}/{path.lstrip('/')}"
                try:
                    response = requests.get(url, timeout=5)
                    
                    if response.status_code == 200:
                        print(Fore.GREEN + f"  ✔ Found Admin Panel in {url}")
                        save_result(url)
                    else:
                        print(Fore.RED + f"  ❌ Not Found Admin Panel in {url}")
                
                except requests.RequestException as e:
                    print(Fore.RED + f"  [ERROR] Unable to access {url}: {e}")

            print(Fore.BLUE + "-" * 50)
    
    except KeyboardInterrupt:
        print(Fore.RED + "\n[EXIT] Program terminated by user (Ctrl + C)")
        sys.exit(0)

if __name__ == "__main__":
    try:
        banner()
        
        
        input_file = input(Fore.CYAN + "Input File: \033[0m").strip()
        admin_list_file = "list.txt"

        targets = load_list(input_file)
        admin_paths = load_list(admin_list_file)

        if not targets:
            print(Fore.RED + f"[ERROR] Target file '{input_file}' tidak ditemukan atau kosong!")
        if not admin_paths:
            print(Fore.RED + f"[ERROR] Admin list file '{admin_list_file}' tidak ditemukan atau kosong!")

        if targets and admin_paths:
            print(Fore.BLUE + "[DEBUG] Admin List Checker Founded!")
            check_admin_panel(targets, admin_paths)

    except KeyboardInterrupt:
        print(Fore.RED + "\n[EXIT]" + Fore.CYAN + " Program terminated by user (Ctrl + C)")
        sys.exit(0)
