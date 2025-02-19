import time
import os
import subprocess
import sys
import signal
import importlib
import requests

# List Package Required
REQUIRED_PACKAGES = ["colorama", "requests"]

def install_packages():
    for package in REQUIRED_PACKAGES:
        try:
            importlib.import_module(package)
        except ImportError:
            print(f"\033[1;91mYou Not Installed, Package: {package}\033[0m")
            print(f"\033[1;93mInstalling {package}, Please Wait...\033[0m")
            subprocess.run([sys.executable, "-m", "pip", "install", package], check=True)

def handle_exit(signum, frame):
    print("\n\033[1;92mGoodBye, Have a nice day!\033[0m")
    os._exit(0)

def clear_screen():
    if os.name == 'nt':
        subprocess.run('cls', shell=True)
    else:
        subprocess.run('clear', shell=True)

def display_banner():
    print("""
    \033[1;93m
    $$\   $$\                                         $$\ $$$$$$$\             $$\     
    $$ |  $$ |                                        \__|$$  __$$\            $$ |    
    \$$\ $$  | $$$$$$\  $$$$$$$\   $$$$$$\   $$$$$$\  $$\ $$ |  $$ | $$$$$$\ $$$$$$\   
     \$$$$  / $$  __$$\ $$  __$$\ $$  __$$\  \____$$\ $$ |$$$$$$$\ |$$  __$$\\_$$  _|  
     $$  $$<  $$$$$$$$ |$$ |  $$ |$$ /  $$ | $$$$$$$ |$$ |$$  __$$\ $$ /  $$ | $$ |    
    $$  /\$$\ $$   ____|$$ |  $$ |$$ |  $$ |$$  __$$ |$$ |$$ |  $$ |$$ |  $$ | $$ |$$\ 
    $$ /  $$ |\$$$$$$$\ $$ |  $$ |$$$$$$$  |\$$$$$$$ |$$ |$$$$$$$  |\$$$$$$  | \$$$$  |
    \__|  \__| \_______|\__|  \__|$$  ____/  \_______|\__|\_______/  \______/   \____/  v1.1
                                  $$ |                                                 
                                  $$ |                                                 
                                  \__|      
""")

def display_menu():
    print("\033[94mXenpaiBot - The Ultimate Pentesting Bot \033[97m")
    print("Author : \033[1;93mKanezama")
    print("\033[97mVersion : \033[1;92m1.1")
    print("\033[97mNote : \033[1;96mUse responsibly, open source for learning.")
    print()
    print(''' 
    \033[1;97m1. Brute Force WordPress
    2. WebShell Finder
    3. Checker XSS [ \033[1;93mMaintenance For Next Update \033[97m]
    4. Grabber Domain By Date v1 [ \033[1;93mMaintenance For Next Update \033[97m]
    5. Grabber Domain By Search [ \033[1;93mMaintenance For Next Update \033[97m]
    6. Generate Quotes [ \033[1;96mRandom Generates \033[97m]
    7. Marshal Encrypt/Decrypt [ \033[1;93mMaintenance For Next Update \033[97m]
    8. Reverse IP
    9. Domain To IP [ \033[1;93mMaintenance For Next Update \033[97m]
    99. Report Bug (Redirects to WhatsApp)
    0. Quit
    ''')

def execute_script(script_path):
    try:
        subprocess.run(["python", script_path], check=True)
    except FileNotFoundError:
        print("\033[1;91mError: Script not found.\033[0m")
    except subprocess.CalledProcessError:
        pass  # Suppress error message

def menu():
    signal.signal(signal.SIGTSTP, handle_exit)
    signal.signal(signal.SIGINT, handle_exit)

    while True:
        clear_screen()
        display_banner()
        display_menu()

        choice = input("\033[1;94mr00t@XenpaiBot~ \033[0m")

        if choice == '1':
            print("You selected: Brute Force WordPress")
            time.sleep(1)
            clear_screen()
            execute_script("xenpaibot/bruteforce/bruteforce.py")
        elif choice == '2':
            print("You selected: WebShell Finder")
            time.sleep(1)
            clear_screen()
            execute_script("xenpaibot/shell-finder/shell.py")
        elif choice == '5':
            print("You selected: Domain Search")
            time.sleep(1)
            clear_screen()
            execute_script("xenpaibot/domain-grabber/domain-search.py")
        elif choice == '6':
            print("You selected: Generate Quotes")
            time.sleep(0.5)
            execute_script("xenpaibot/quotes-generator/quotes.py")
        elif choice == '8':
            print("You selected: Reverse IP")
            time.sleep(0.5)
            execute_script("xenpaibot/reverse-ip/ip.py")
        elif choice == '99':
            print("Redirecting to WhatsApp support...")
            time.sleep(1)
            os.system("xdg-open https://wa.me/+6285695450203")
        elif choice == '0':
            print("Exiting...")
            break
        else:
            print("\033[1;91m{-} Invalid choice!\033[0m")
            time.sleep(1)

        if input("\nReturn to main menu? (y/n): ").lower() != 'y':
            print("Exiting...")
            break

if __name__ == "__main__":
    install_packages()
    menu()
