import requests
from bs4 import BeautifulSoup
import os
import time
from tqdm import tqdm
from pathlib import Path

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    banner = """
\033[93m_  _ _   _ ___  ____ ____ ___ ____ ___ 
|__|  \_/  |__] |___ [__   |  |__|  |  
|  |   |   |    |___ ___]  |  |  |  |  
\033[0m"""
    author = "\033[96mAuthor : Kanezama\033[0m"
    bot_info = "\033[95mXenpaiBot - The Ultimate Pentesting Bot.\033[0m"
    print(banner + "\n" + author + "\n" + bot_info + "\n")

def get_domains_from_page(page):
    url = f"https://hypestat.com/recently-updated/{page}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
    except requests.exceptions.RequestException as e:
        print(f"\033[1;91m[\033[1;97m!\033[1;91m] Failed to retrieve page {page}: {e} \033[0m")
        return []
    
    soup = BeautifulSoup(response.text, "html.parser")
    domain_elements = soup.select("a[href^='https://hypestat.com/info/']")
    domains = [a['href'].split("/")[-1] for a in domain_elements]
    
    return domains

if __name__ == "__main__":
    clear_screen()
    print_banner()

    try:
        while True:  
            try:
                first_page = int(input("\n\033[1;93mEnter First Page number: \033[0m").strip())
                if first_page > 0: 
                    break
                else:
                    print("\033[1;91m[\033[1;97m!\033[1;91m] First page number must be greater than 0. \033[0m")
            except ValueError:
                print("\033[1;91m[\033[1;97m!\033[1;91m] Invalid input. Please enter a valid integer. \033[0m")

        while True:  
            try:
                last_page = int(input("\n\033[1;93mEnter Last Page number: \033[0m").strip())
                if last_page >= first_page:  
                    break
                else:
                    print("\033[1;91m[\033[1;97m!\033[1;91m] Last page number must be greater than or equal to the first page number. \033[0m")
            except ValueError:
                print("\033[1;91m[\033[1;97m!\033[1;91m] Invalid input. Please enter a valid integer. \033[0m")

    except KeyboardInterrupt:
        print("\n\033[1;91m[\033[1;97m!\033[1;91m] Process interrupted by user. Exiting gracefully. \033[0m")
        exit()


    all_domains = []
    try:
        for page in tqdm(range(first_page, last_page + 1), desc="Scraping Pages"):
            time.sleep(1)  
            domains = get_domains_from_page(page)
            for domain in domains:
                print(f"Grabbing {domain} from Page {page}")
            all_domains.extend(domains)

        all_domains = list(set(all_domains))  

        if all_domains:
            while True:
                filename = input("\nThe results will be saved as (ex. Results.txt) : ").strip() or "results.txt"
                file_path = Path(filename)
                if file_path.exists():
                    overwrite = input(f"File '{filename}' already exists. Overwrite? (y/n): ").lower()
                    if overwrite != 'y':
                        continue  
                try:
                    with open(file_path, "w", encoding="utf-8") as file:
                        file.write("\n".join(all_domains) + "\n")
                    print(f"\nResults saved in {filename}")
                    break  
                except OSError as e:
                    print(f"\033[1;91m[\033[1;97m!\033[1;91m] Error saving file: {e} \033[0m")
        else:
            print("\n\033[1;91m[\033[1;97m!\033[1;91m] No domains found. \033[0m")

    except requests.exceptions.RequestException as e:
        print(f"\033[1;91m[\033[1;97m!\033[1;91m] A request error occurred: {e} \033[0m")
    except KeyboardInterrupt:
        print("\n\033[1;91m[\033[1;97m!\033[1;91m] Process interrupted by user. Exiting gracefully. \033[0m")