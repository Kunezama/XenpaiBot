import time
import os
import subprocess
import sys
import signal
import base64
from typing import Dict
import colorama
from colorama import Fore, Back, Style

colorama.init(autoreset=True)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
wordlist_path = os.path.join(BASE_DIR, "xenpaibot/bruteforce/pwd.txt")
admin_list_path = os.path.join(BASE_DIR, "xenpaibot/tools1/admincheck/list.txt")

def handle_exit(signum, frame):
    print(f"\n{Fore.GREEN}Goodbye, have a nice day!{Style.RESET_ALL}")
    sys.exit(0)

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def execute_script(script_path: str):
    full_script_path = os.path.join(BASE_DIR, script_path)
    if not os.path.exists(full_script_path):
        print(f"{Fore.RED}Error: Script not found at {full_script_path}.{Style.RESET_ALL}")
        return

    ext = os.path.splitext(full_script_path)[-1].lower()
    cmd_map = {".py": "python", ".js": "node", ".sh": "bash"}

    if ext in cmd_map:
        try:
            subprocess.run(f"{cmd_map[ext]} {full_script_path}", shell=True, check=True)
        except subprocess.CalledProcessError:
            print(f"{Fore.RED}Error executing script.{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Unsupported file format!{Style.RESET_ALL}")

def open_whatsapp():
    try:
        obfuscated = b'YUhSMGNITTZMeTkzWVM1dFpTOHJOakk0TlRZNU5UUTFNREl3TXc9PQ=='
        decoded_once = base64.b64decode(obfuscated).decode('utf-8')
        url = base64.b64decode(decoded_once).decode('utf-8')

        print(f"{Fore.GREEN}[INFO] Opening WhatsApp contact...{Style.RESET_ALL}")
        os.system(f"start {url}" if os.name == "nt" else f"xdg-open {url}")

    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")

def display_banner():
    print(f"""{Fore.YELLOW}
    $$\   $$\                                         $$\ $$$$$$$\             $$\     
    $$ |  $$ |                                        \__|$$  __$$\            $$ |    
    \$$\ $$  | $$$$$$\  $$$$$$$\   $$$$$$\   $$$$$$\  $$\ $$ |  $$ | $$$$$$\ $$$$$$\   
     \$$$$  / $$  __$$\ $$  __$$\ $$  __$$\  \____$$\ $$ |$$$$$$$\ |$$  __$$\\_$$  _|  
     $$  $$<  $$$$$$$$ |$$ |  $$ |$$ /  $$ | $$$$$$$ |$$ |$$  __$$\ $$ /  $$ | $$ |    
    $$  /\$$\ $$   ____|$$ |  $$ |$$ |  $$ |$$  __$$ |$$ |$$ |  $$ |$$ |  $$ | $$ |$$\ 
    $$ /  $$ |\$$$$$$$\ $$ |  $$ |$$$$$$$  |\$$$$$$$ |$$ |$$$$$$$  |\$$$$$$  | \$$$$  |
    \__|  \__| \_______|\__|  \__|$$  ____/  \_______|\__|\_______/  \______/   \____/  {Fore.CYAN}V1.3{Fore.YELLOW}
                                  $$ |                                                 
                                  $$ |                                                 
                                  \__|     
 
                     {Back.RED}{Fore.BLUE} XenpaiBot {Fore.WHITE}- The Ultimate Pentesting Bot. {Back.RESET}
    """)

def menu():
    signal.signal(signal.SIGINT, handle_exit)

    actions: Dict[str, str] = {
        "1": "xenpaibot/bruteforce/bf2.py",
        "2": "xenpaibot/dmain/search.js",
        "3": "xenpaibot/quotes-generator/quotes.py",
        "4": "xenpaibot/reverse-ip/ip.py",
        "5": "xenpaibot/grabber/hypestat.py",
        "6": "xenpaibot/grabber/haxorid.py",
        "7": "xenpaibot/grabber/defacernet.py",
        "8": "xenpaibot/grabber/mirror-horg.py",
        "9": "xenpaibot/tools1/admincheck/adm.py",
        "10": "xenpaibot/tools1/z1/env-.py",
        "11": "xenpaibot/tools1/z1/cmswp.py"
    }

    while True:
        clear_screen()
        display_banner()
        print(f"\033[1;97m{Fore.WHITE}Author : {Fore.YELLOW}Kanezama")
        print(f"\033[1;97m{Fore.WHITE}Support : {Fore.GREEN}SABUN BOLONG CYBER CLUB {Fore.MAGENTA}[ {Fore.GREEN}SBCC {Fore.MAGENTA}] {Fore.WHITE}| {Fore.GREEN}JABAR ERROR SYSTEM {Fore.MAGENTA}[ {Fore.GREEN}JES {Fore.MAGENTA}]")
        print(f"\033[1;97m{Fore.WHITE}Telegram : {Fore.YELLOW}t.me/@TitanSi_KangWebShell")
        print(f"\033[1;97m{Fore.WHITE}Note : {Fore.CYAN}Use responsibly, open source for learning.{Fore.WHITE}\n")
        print(f"\033[1;97m{Fore.WHITE}[ {Fore.CYAN}1 {Fore.WHITE}] Bruteforce Attack {Fore.BLACK}[ {Fore.MAGENTA}V3 {Fore.BLACK}] {Style.RESET_ALL}{Fore.WHITE}→ {Fore.YELLOW} Update!")
        print(f"\033[1;97m{Fore.WHITE}[ {Fore.CYAN}2 {Fore.WHITE}] Domain Search")
        print(f"\033[1;97m{Fore.WHITE}[ {Fore.CYAN}3 {Fore.WHITE}] Quotes Generator")
        print(f"\033[1;97m{Fore.WHITE}[ {Fore.CYAN}4 {Fore.WHITE}] Reverse IP Lookup")
        print(f"\033[1;97m{Fore.WHITE}[ {Fore.CYAN}5 {Fore.WHITE}] Grabber (Hypestat) {Style.RESET_ALL}{Fore.CYAN}→ {Fore.BLUE}Update Perminute!")
        print(f"\033[1;97m{Fore.WHITE}[ {Fore.CYAN}6 {Fore.WHITE}] Grabber (HaxorID)")
        print(f"\033[1;97m{Fore.WHITE}[ {Fore.CYAN}7 {Fore.WHITE}] Grabber (DefacerNet)")
        print(f"\033[1;97m{Fore.WHITE}[ {Fore.CYAN}8 {Fore.WHITE}] Grabber (Mirror-H)")
        print(f"\033[1;97m{Fore.WHITE}[ {Fore.CYAN}9 {Fore.WHITE}] Admin Page Checker {Fore.YELLOW}[ \033[1;30mMASS TARGET {Fore.YELLOW}] {Style.RESET_ALL}{Fore.CYAN}→ {Fore.YELLOW} With Panel List 2.5k!!")
        print(f"\033[1;97m{Fore.WHITE}[ {Fore.CYAN}10 {Fore.WHITE}] .ENV Variable Checker {Fore.BLACK}[ {Fore.BLUE}MANUAL & FILE {Fore.BLACK}] ")
        print(f"\033[1;97m{Fore.WHITE}[ {Fore.CYAN}11 {Fore.WHITE}] CMS WordPress Detector {Fore.YELLOW}[ \033[1;30mMASS TARGET {Fore.YELLOW}]  {Style.RESET_ALL}{Fore.CYAN}→ {Fore.YELLOW}Super Fast!")
        print(f"\033[1;97m{Fore.WHITE}[ {Fore.CYAN}99 {Fore.WHITE}] Report Bug (Redirects to WhatsApp)")
        print(f"\033[1;97m{Fore.WHITE}[ {Fore.CYAN}0 {Fore.WHITE}] Quit\n")

        choice = input(f"{Fore.BLUE}r00t@XenpaiBot~ ").strip()

        if choice in actions:
            print(f"You selected: {actions[choice]}")
            time.sleep(1)
            clear_screen()
            execute_script(actions[choice])
        elif choice == "99":
            open_whatsapp()
        elif choice == "0":
            print("Exiting...")
            break
        else:
            print(f"{Fore.RED}Invalid choice! Please try again.{Style.RESET_ALL}")
            time.sleep(1)

        if input("\nReturn to main menu? (y/n): ").strip().lower() != "y":
            print("Exiting...")
            break

if __name__ == "__main__":
    menu()
