import requests
import os
import threading
import concurrent.futures
from colorama import Fore, Style, init

init(autoreset=True)

OUTPUT_FILE = "wordpress_sites.txt"
WORDPRESS_PATHS = ["/wp-content/", "/wp-admin/", "/xmlrpc.php"]
TIMEOUT = 2  # Maximum timeout (seconds)
MAX_THREADS = 50  # Number of threads


file_lock = threading.Lock()
wordpress_count = 0 


def check_wordpress(url):
    """Checks if a website is using WordPress."""
    global wordpress_count

    if not url.startswith("http"):
        url = "http://" + url  # Add protocol if missing

    try:
        for path in WORDPRESS_PATHS:
            response = requests.get(url + path, timeout=TIMEOUT)
            if response.status_code == 200:
                with file_lock:
                    with open(OUTPUT_FILE, "a") as f:
                        f.write(url + "\n")
                    wordpress_count += 1  
                print(f"{Fore.GREEN}[SUCCESS!] {url} {Fore.YELLOW}→ CMS WordPress!")
                return  

        
        print(f"{Fore.RED}[FAILED!] {url} {Fore.CYAN}→ Not WordPress!")

    except requests.exceptions.Timeout:
        print(f"{Fore.WHITE}[TIMEOUT!] {url} {Fore.RED}→ Is Dead!")
    except requests.RequestException:
        print(f"{Fore.RED}[ERROR!] {url} {Fore.MAGENTA}→ Cannot be accessed!")


def banner():
    return f"""{Fore.CYAN}
 
 _    _______     ___      _       
| |  | | ___ \   |_  |    | |      
| |  | | |_/ /     | | ___| |_ ____
| |/\| |  __/      | |/ _ \ __|_  /
\  /\  / |     /\__/ /  __/ |_ / / 
 \/  \/\_|     \____/ \___|\__/___|
                                                                                                                    
{Fore.WHITE}Author : Kanezama
"""

def main():
    global wordpress_count
    wordpress_count = 0  # Reset count before each scan

    os.system("cls" if os.name == "nt" else "clear")  # Clear the terminal screen
    print(banner())  # Print the banner correctly

    print(f"{Fore.CYAN}=== Super Fast WordPress Scanner By XenpaiBot ===")
    print(f"{Fore.YELLOW}[1] Enter a website manually")
    print(f"{Fore.YELLOW}[2] Scan websites from a file")
    print(f"{Fore.YELLOW}[0] Exit")

    choice = input(f"\n{Fore.BLUE}Select an option: ").strip()

    if choice == "1":
        url = input(f"{Fore.GREEN}Enter website URL: ").strip()
        check_wordpress(url)
        print(f"{Fore.GREEN}Scan complete! Results saved in {OUTPUT_FILE} with {wordpress_count} Success!")

    elif choice == "2":
        file_path = input(f"{Fore.GREEN}INPUT YOUR FILE: ").strip()

        if not os.path.exists(file_path):
            print(f"{Fore.RED}File {file_path} not found!")
            return

        with open(file_path, "r") as file:
            urls = [line.strip() for line in file if line.strip()]

        print(f"{Fore.CYAN}Starting scan for {len(urls)} websites using {MAX_THREADS} threads...")

        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
            executor.map(check_wordpress, urls)

        print(f"{Fore.GREEN}Scan complete! Results saved in {OUTPUT_FILE} with {wordpress_count} Success!")

    elif choice == "0":
        print(f"{Fore.RED}Exiting...")
        exit()

    else:
        print(f"{Fore.RED}Invalid option!")


if __name__ == "__main__":
    main()
