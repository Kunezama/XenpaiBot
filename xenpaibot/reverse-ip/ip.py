from threading import Thread
from queue import Queue
import json
import requests
import os
import time
import sys
from colorama import Fore, Style, init

init(autoreset=True)

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    print(Fore.RED + r"""
     (                                      (    (     
     )\ )                                   )\ ) )\ )  
    (()/(   (    )      (   (          (   (()/((()/(  
     /(_)) ))\  /((    ))\  )(   (    ))\   /(_))/(_)) 
    (_))  /((_)(_))\  /((_)(()\  )\  /((_) (_)) (_))   
    | _ \(_))  _)((_)(_))   ((_)((_)(_))   |_ _|| _ \  
    |   // -_) \ V / / -_) | '_|(_-</ -_)   | | |  _/  
    |__|_\\___|  \_/  \___| |_|  /__/\___|  |___||_|    
    """ + Style.RESET_ALL)
    print("\033[94mXenpaiBot - The Ultimate Pentesting Bot \033[97m")
    print("Author : \033[1;93mKanezama")

def get_input_file():
    try:
        input_file = input(Fore.YELLOW + "[*] Input Domain/IP File: " + Style.RESET_ALL).strip()
        if os.path.isfile(input_file):
            return input_file
        else:
            print(Fore.RED + f"[!] File '{input_file}' not found.")
            return None
    except KeyboardInterrupt:
        print(Fore.RED + "\n[!] Process interrupted by user.")
        return None

def get_number_of_threads():
    return 5

def get_request_delay():
    return 1

class ReverseIP(Thread):
    def __init__(self, address_q, delay):
        super().__init__()
        self.address_q = address_q
        self.delay = delay

    def run(self):
        while not self.address_q.empty():
            ipaddy = self.address_q.get()
            self.address_q.task_done()
            self.reverse_ip(ipaddy)
            time.sleep(self.delay)

    def reverse_ip(self, ipaddy):
        session = requests.Session()
        try:
            session.headers.update({
                'authority': 'domains.yougetsignal.com',
                'accept': 'application/json',
                'user-agent': 'Mozilla/5.0',
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'referer': 'https://www.yougetsignal.com/tools/web-sites-on-web-server/',
            })

            response = session.post('https://domains.yougetsignal.com/domains.php', data={'remoteAddress': ipaddy})
            if 'Fail' in response.text:
                print(Fore.RED + f'[*] Limit reached for {ipaddy}. Change your IP or try again later.')
                return 

            try:
                loaded_json = json.loads(response.text).get('domainArray', [])
            except json.JSONDecodeError:
                print(Fore.YELLOW + f"[*] No domains found for {ipaddy}")
                return 

            if loaded_json:
                print(Fore.GREEN + f"[*] {len(loaded_json)} domains found for {ipaddy}")
                with open('results.txt', 'a') as output_file:
                    output_file.write(f'Results for {ipaddy}:\n')
                    for domain in loaded_json:
                        output_file.write(domain[0] + '\n')
        except Exception:
            pass

def main():
    clear_console()
    print_banner()
    
    input_file = get_input_file()
    if not input_file:
        return
    
    try:
        with open(input_file, "r") as f:
            addresses = [line.strip() for line in f.readlines()]
    except Exception:
        return

    if not addresses:
        return

    threads_count = get_number_of_threads()
    delay = get_request_delay()
    address_q = Queue()
    for address in addresses:
        address_q.put(address)
    threads = [ReverseIP(address_q, delay) for _ in range(threads_count)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    print(Fore.YELLOW + "[*] Scan completed. Output: results.txt")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(Fore.RED + "\n[!] Process interrupted by user.")
