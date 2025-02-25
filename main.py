import time
import os
import subprocess
import sys
import signal
import importlib
import base64
from typing import Dict

# XenpaiBot Is Number One 😎🔥
REQUIRED_PACKAGES = ["colorama", "requests", "tqdm", "beautifulsoup4"]

def handle_exit(signum, frame):
    """Handle exit signal."""
    print("\n\033[1;92mGoodbye, have a nice day!\033[0m")
    sys.exit(0)

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def execute_script(script_path: str):
    """Execute a script based on its file extension."""
    if not os.path.exists(script_path):
        print("\033[1;91mError: Script not found.\033[0m")
        return
    
    ext = os.path.splitext(script_path)[-1].lower()
    cmd_map = {".py": "python", ".js": "node", ".sh": "bash"}
    
    if ext in cmd_map:
        try:
            subprocess.run([cmd_map[ext], script_path], check=True)
        except subprocess.CalledProcessError:
            print("\033[1;91mError executing script.\033[0m")
    else:
        print("\033[1;91mUnsupported file format!\033[0m")

def open_whatsapp():
    """Open WhatsApp link in the default browser."""
    url = base64.b64decode('aHR0cHM6Ly93YS5tZS8rNjI4NTY5NTQ1MDIwMw==').decode('utf-8')    
    if os.name == 'nt':
        os.system(f"start {url}")
    elif os.name == 'posix':
        os.system(f"xdg-open {url}")
    else:
        os.system(f"open {url}")

def display_banner():
    """Display the banner."""
    print("""
    \033[1;93m
    $$\   $$\                                         $$\ $$$$$$$\             $$\     
    $$ |  $$ |                                        \__|$$  __$$\            $$ |    
    \$$\ $$  | $$$$$$\  $$$$$$$\   $$$$$$\   $$$$$$\  $$\ $$ |  $$ | $$$$$$\ $$$$$$\   
     \$$$$  / $$  __$$\ $$  __$$\ $$  __$$\  \____$$\ $$ |$$$$$$$\ |$$  __$$\\_$$  _|  
     $$  $$<  $$$$$$$$ |$$ |  $$ |$$ /  $$ | $$$$$$$ |$$ |$$  __$$\ $$ /  $$ | $$ |    
    $$  /\$$\ $$   ____|$$ |  $$ |$$ |  $$ |$$  __$$ |$$ |$$ |  $$ |$$ |  $$ | $$ |$$\ 
    $$ /  $$ |\$$$$$$$\ $$ |  $$ |$$$$$$$  |\$$$$$$$ |$$ |$$$$$$$  |\$$$$$$  | \$$$$  |
    \__|  \__| \_______|\__|  \__|$$  ____/  \_______|\__|\_______/  \______/   \____/  \033[1;96mV1.2\033[1;93m
                                  $$ |                                                 
                                  $$ |                                                 
                                  \__|     
 
                     \033[0;101m   \033[94mXenpaiBot \033[1;97m- The Ultimate Pentesting Bot.   \033[0m
 """)
 
def menu():
    """Display the main menu and handle user input."""
    signal.signal(signal.SIGINT, handle_exit)
    actions: Dict[str, str] = {
        "1": "xenpaibot/bruteforce/bruteforce.py",
        "2": "xenpaibot/dmain/search.js",
        "3": "xenpaibot/quotes-generator/quotes.py",
        "4": "xenpaibot/reverse-ip/ip.py",
        "5": "xenpaibot/grabber/hypestat.py",
        "6": "xenpaibot/grabber/haxorid.py"
    }

    while True:
        clear_screen()
        display_banner()
        print("Author : \033[1;93mKanezama")
        print("\033[1;97mSupport : \033[1;92mSABUN BOLONG CYBER CLUB \033[1;93m[ \033[1;92mSBCC \033[1;93m]")
        print("\033[97mNote : \033[1;96mUse responsibly, open source for learning.\033[1;97m\n")
        print("[ \033[1;96m1 \033[1;97m] BRUTE FORCE WORDPRESS")
        print("[ \033[1;96m2 \033[1;97m] GRAB DOMAIN BY DORKING V1 [ \033[1;95mJavaScript \033[97m]")
        print("[ \033[1;96m3 \033[1;97m] GENERATES QUOTES")
        print("[ \033[1;96m4 \033[1;97m] MASS REVERSE IP")
        print("[ \033[1;96m5 \033[1;97m] GRABBER HYPESTAT [ \033[1;91mUpdate PerMinute \033[1;97m]")
        print("[ \033[1;96m6 \033[1;97m] GRABBER HAXOR.ID")
        print("[ \033[1;96m99 \033[1;97m] Report Bug (Redirects to WhatsApp)")
        print("[ \033[1;96m0 \033[1;97m] Quit\n")
        
        choice = input("\033[1;94mr00t@XenpaiBot~ \033[0m").strip()
        
        if choice in actions:
            print(f"You selected: {choice}")
            time.sleep(1)
            clear_screen()
            execute_script(actions[choice])
        elif choice == "99":
            print("Redirecting to WhatsApp support...")
            time.sleep(1)
            open_whatsapp()
        elif choice == "0":
            print("Exiting...")
            break
        else:
            print("\033[1;91mInvalid choice! Please try again.\033[0m")
            time.sleep(1)

        if input("\nReturn to main menu? (y/n): ").strip().lower() != 'y':
            print("Exiting...")
            break

if __name__ == "__main__":
    menu()
