import requests
import re
from colorama import Fore, Style, init
import os
from tqdm import tqdm

init(autoreset=True)

def colored_text(text, color):
    return f"{color}{text}{Style.RESET_ALL}"

def grab_domains_from_archive(start_page, end_page, save_file):
    domains = set()

    print(colored_text(f"\n🔍 Fetching domains from archive page {start_page} to {end_page}...\n", Fore.CYAN))

    for page in tqdm(range(start_page, end_page + 1), desc="Scraping Progress", unit="page"):
        url = f"https://mirror-h.org/archive/page/{page}"

        try:
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
            if response.status_code != 200:
                print(colored_text(f"❌ Failed to fetch page {page}. Skipping...", Fore.RED))
                continue

            found_domains = re.findall(r'https?://[a-zA-Z0-9.-]+(?:\.[a-zA-Z]{2,})+', response.text)
            
            for domain in found_domains:
                if "mirror-h.org" not in domain:
                    domains.add(domain)

        except requests.exceptions.RequestException as e:
            print(colored_text(f"⚠️ Error fetching page {page}: {e}", Fore.RED))

    if domains:
        with open(save_file, 'w', encoding='utf-8') as file:
            file.write("\n".join(sorted(domains)))

        print(Fore.GREEN + f"\n✅ Successfully grabbed {len(domains)} domains! Saved to {save_file}\n")
    else:
        print(Fore.YELLOW + "\n⚠️ No domains found in the selected page range.\n")

def banner():
    print(Fore.CYAN + """
  
  __  __ _                          _   _ 
 |  \/  (_)_ __ _ __ ___  _ __     | | | |
 | |\/| | | '__| '__/ _ \| '__|____| |_| |
 | |  | | | |  | | | (_) | | |_____|  _  |
 |_|  |_|_|_|  |_|  \___/|_|       |_| |_|
     """ + Fore.MAGENTA + "XenpaiBot -" + Fore.WHITE + " Mirror-H Automation")

def main():
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
        banner()

        end_page = int(input(colored_text("\n📌 Up to which page? : ", Fore.YELLOW)).strip())

        save_file = input(colored_text("📄 Save results to (ex: domains.txt): ", Fore.YELLOW)).strip()

        grab_domains_from_archive(1, end_page, save_file)

    except KeyboardInterrupt:
        print(colored_text("\nOperation interrupted by user.", Fore.RED))

if __name__ == "__main__":
    main()
