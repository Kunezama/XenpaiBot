import requests
from bs4 import BeautifulSoup
import os
import time
from urllib.parse import urlparse
from tqdm import tqdm
from colorama import Fore, Style, init
import random

init(autoreset=True)

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36", 
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/117.0.1937.63 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; en-US) Gecko/20100101 Firefox/57.1",
]

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def colored_text(text, color):
    return f"{color}{text}{Style.RESET_ALL}"

def scrape_domains(base_url, first_page, last_page, attacker=None, mode=None):
    domains = set()
    try:
        for page in tqdm(range(first_page, last_page + 1), desc=colored_text(f"Scraping {mode} pages", Fore.YELLOW), unit="page"):
            current_url = base_url.format(attacker=attacker, page=page) if attacker else base_url.format(page=page)
            try:
                user_agent = random.choice(USER_AGENTS)
                response = requests.get(current_url, headers={"User-Agent": user_agent}, timeout=10)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, "html.parser")
                links = soup.find_all("a")

                for link in links:
                    href = link.get("href")
                    if href:
                        absolute_url = href if href.startswith("http") else urlparse(current_url)._replace(path=href).geturl()
                        parsed_url = urlparse(absolute_url)
                        if parsed_url.netloc:
                            domain = parsed_url.netloc
                            domains.add(domain)
                            print(colored_text(f"Found {domain} from {mode} Page {page}", Fore.GREEN))

                time.sleep(random.uniform(1, 3))
            except requests.exceptions.RequestException as e:
                print(colored_text(f"Error fetching {current_url}: {e}", Fore.RED))
                continue
    except KeyboardInterrupt:
        print(colored_text("\nScraping interrupted by user.", Fore.RED))
    return domains

def save_results(filename, domains, overwrite=False):
    mode = "w" if overwrite else "a"
    with open(filename, mode) as outfile:
        for domain in sorted(domains):
            outfile.write(domain + "\n")
    print(colored_text(f"Results saved to {filename}.", Fore.GREEN))

def banner_x():
    print(Fore.YELLOW + """ 

  _____        __                    _   _      _      _____           _     
 |  __ \      / _|                  | \ | |    | |    / ____|         | |    
 | |  | | ___| |_ __ _  ___ ___ _ __|  \| | ___| |_  | |  __ _ __ __ _| |__  
 | |  | |/ _ \  _/ _` |/ __/ _ \ '__| . ` |/ _ \ __| | | |_ | '__/ _` | '_ \ 
 | |__| |  __/ || (_| | (_|  __/ |  | |\  |  __/ |_  | |__| | | | (_| | |_) |
 |_____/ \___|_| \__,_|\___\___|_|  |_| \_|\___|\__|  \_____|_|  \__,_|_.__/ 
           """ + Fore.MAGENTA + "XenpaiBot - " + Fore.WHITE + "The Ultimate Pentesting Bot. ")

def main():
    try:
        while True:
            clear_screen()
            banner_x()
            print(colored_text("\nDefacer.net Domain Scraper", Fore.BLUE))
            print(colored_text("\n1. Grab from Attacker", Fore.CYAN))
            print(colored_text("2. Grab from Archive", Fore.CYAN))
            print(colored_text("3. Grab from Special", Fore.CYAN))
            print(colored_text("4. Exit", Fore.CYAN))

            choice = input(colored_text("\nEnter your choice: ", Fore.YELLOW))

            if choice == "1":
                clear_screen()
                banner_x()
                attacker = input(colored_text("Enter Attacker Username: ", Fore.CYAN))
                first_page = int(input(colored_text("Enter first page number: ", Fore.WHITE)))
                last_page = int(input(colored_text("Enter last page number: ", Fore.WHITE)))
                filename = input(colored_text("Save results in (ex. results.txt): ", Fore.WHITE)).strip()
                overwrite = input(colored_text("Overwrite existing file? (y/n): ", Fore.WHITE)).lower() == 'y'

                base_url = "https://defacer.net/user/{attacker}/{page}"
                domains = scrape_domains(base_url, first_page, last_page, attacker, mode="Attacker")
                save_results(filename, domains, overwrite)
                print(colored_text("Operation completed.", Fore.GREEN))

            elif choice == "2":
                first_page = int(input(colored_text("Enter first page number: ", Fore.WHITE)))
                last_page = int(input(colored_text("Enter last page number: ", Fore.WHITE)))
                filename = input(colored_text("Save results in (ex. results.txt): ", Fore.WHITE)).strip()
                overwrite = input(colored_text("Overwrite existing file? (y/n): ", Fore.WHITE)).lower() == 'y'

                base_url = "https://defacer.net/archive/{page}"
                domains = scrape_domains(base_url, first_page, last_page, mode="Archive")
                save_results(filename, domains, overwrite)
                print(colored_text("Operation completed.", Fore.GREEN))

            elif choice == "3":
                first_page = int(input(colored_text("Enter first page number: ", Fore.WHITE)))
                last_page = int(input(colored_text("Enter last page number: ", Fore.WHITE)))
                filename = input(colored_text("Save results in (ex. results.txt): ", Fore.WHITE)).strip()
                overwrite = input(colored_text("Overwrite existing file? (y/n): ", Fore.WHITE)).lower() == 'y'

                base_url = "https://defacer.net/special/{page}"
                domains = scrape_domains(base_url, first_page, last_page, mode="Special")
                save_results(filename, domains, overwrite)
                print(colored_text("Operation completed.", Fore.GREEN))

            elif choice == "4":
                break  

    except KeyboardInterrupt: 
        print(colored_text("\nProgram interrupted.", Fore.RED))

if __name__ == "__main__":
    main()
