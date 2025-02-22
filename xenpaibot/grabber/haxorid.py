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
    # ADD MORE USER AGENT / TAMBAHKAN USER AGENT JIKA KENA BLOCKS
]

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def colored_text(text, color):
    return f"{color}{text}{Style.RESET_ALL}"

def scrape_domains(base_url, first_page, last_page, attacker=None, mode=None):
    domains = set()
    try:
        for page in tqdm(range(first_page, last_page + 1), desc=colored_text(f"Scraping {mode} pages", Fore.YELLOW), unit="page"):
            current_url = base_url.format(page=page)
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
                            if attacker:
                                print(colored_text(f"Found {domain} from {attacker}", Fore.GREEN))
                            elif mode:
                                print(colored_text(f"Found {domain} from {mode} Page {page}", Fore.MAGENTA))

                time.sleep(random.uniform(1, 3))  # Rate limiting
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

  _    _                    _____ _____     _____           _     _               
 | |  | |                  |_   _|  __ \   / ____|         | |   | |              
 | |__| | __ ___  _____  _ __| | | |  | | | |  __ _ __ __ _| |__ | |__   ___ _ __ 
 |  __  |/ _` \ \/ / _ \| '__| | | |  | | | | |_ | '__/ _` | '_ \| '_ \ / _ \ '__|
 | |  | | (_| |>  < (_) | | _| |_| |__| | | |__| | | | (_| | |_) | |_) |  __/ |   
 |_|  |_|\__,_/_/\_\___/|_||_____|_____/   \_____|_|  \__,_|_.__/|_.__/ \___|_|   
                 """ + Fore.MAGENTA + "XenpaiBot -" + Fore.WHITE + "The Ultimate Pentesting Bot. ")

def main():
    try:  # Tangani KeyboardInterrupt di level teratas
        while True:
            clear_screen()
            banner_x()
            print(colored_text("\nHaxor.id Domain Scraper", Fore.BLUE))
            print(colored_text("\n1. Grab from Attacker", Fore.CYAN))
            print(colored_text("2. Grab from Archive", Fore.CYAN))
            print(colored_text("3. Grab from Special", Fore.CYAN))
            print(colored_text("4. Exit", Fore.CYAN))

            try:
                choice = input(colored_text("\nEnter your choice: ", Fore.YELLOW))
            except KeyboardInterrupt:
                print(colored_text("\nProgram interrupted.", Fore.RED))
                break  

            if choice == "1":
                while True:  
                    clear_screen()
                    banner_x()
                    try:
                        mode = input(Fore.CYAN + "\n1. MANUAL\n2. FILE\n" + Fore.WHITE + "\nChoose mode (or Ctrl+C to cancel): ")
                    except KeyboardInterrupt:
                        print(colored_text("\nOperation cancelled.", Fore.RED))
                        break  

                    if mode == "1":
                        try:
                            attacker = input(colored_text("Enter Attacker Username: ", Fore.CYAN))
                            first_page = int(input(colored_text("Enter first page number: ", Fore.WHITE)))
                            last_page = int(input(colored_text("Enter last page number: ", Fore.WHITE)))
                            filename = input(colored_text("Save results in (ex. results.txt): ", Fore.WHITE)).strip()
                            overwrite = input(colored_text("Overwrite existing file? (y/n): ", Fore.WHITE)).lower() == 'y'
                        except KeyboardInterrupt:
                            print(colored_text("\nOperation cancelled.", Fore.RED))
                            break

                        base_url = f"https://haxor.id/archive/attacker/{attacker}&page={{page}}"
                        domains = scrape_domains(base_url, first_page, last_page, attacker, mode="Manual")
                        all_domains = set()
                        save_results(filename, all_domains, overwrite)
                        print(colored_text("Operation completed.", Fore.GREEN))
                        break  
                    elif mode == "2":
                        try:
                            filename_input = input(colored_text("Enter File List With Attacker Username: ", Fore.CYAN))
                            first_page = int(input(colored_text("Enter first page number: ", Fore.WHITE)))
                            last_page = int(input(colored_text("Enter last page number: ", Fore.WHITE)))
                            filename = input(colored_text("Save results in (ex. results.txt): ", Fore.WHITE)).strip()
                            overwrite = input(colored_text("Overwrite existing file? (y/n): ", Fore.WHITE)).lower() == 'y'
                        except KeyboardInterrupt:
                            print(colored_text("\nOperation cancelled.", Fore.RED))
                            break

                        try:
                            with open(filename_input, "r") as file:
                                attackers = [line.strip() for line in file]
                                all_domains = set()
                                for attacker in attackers:
                                    base_url = f"https://haxor.id/archive/attacker/{attacker}&page={{page}}"
                                    domains = scrape_domains(base_url, first_page, last_page, attacker, mode="File")
                                    all_domains.update(domains)
                                save_results(filename, all_domains, overwrite)
                                print(colored_text("Operation completed.", Fore.GREEN))
                                break
                        except FileNotFoundError:
                            print(colored_text(f"File '{filename_input}' not found.", Fore.RED))
                            break 
                    else:
                        print(colored_text("Invalid mode. Please try again.", Fore.YELLOW))

            elif choice in ["2", "3"]:
                try:
                    first_page = int(input(colored_text("Enter first page number: ", Fore.WHITE)))
                    last_page = int(input(colored_text("Enter last page number: ", Fore.WHITE)))
                    filename = input(colored_text("Save results in (ex. results.txt): ", Fore.WHITE)).strip()
                    overwrite = input(colored_text("Overwrite existing file? (y/n): ", Fore.WHITE)).lower() == 'y'
                except KeyboardInterrupt:
                    print(colored_text("\nOperation cancelled.", Fore.RED))
                    continue

                base_url = "https://haxor.id/archive?page={page}" if choice == "2" else "https://haxor.id/archive/special?page={page}"
                domains = scrape_domains(base_url, first_page, last_page, mode="Archive" if choice == "2" else "Special")
                save_results(filename, domains, overwrite)
                print(colored_text("Operation completed.", Fore.GREEN))
                break

            elif choice == "4":
                break  

    except KeyboardInterrupt: 
        print(colored_text("\nProgram interrupted.", Fore.RED))

if __name__ == "__main__":
    main()