from threading import Thread
from queue import Queue
import json
import requests
import os
import time
import sys
import argparse
from colorama import Fore, Style, init

init(autoreset=True)

class ReverseIPScanner:
    def __init__(self, input_file=None, threads=5, delay=1, output_file="results.txt", verbose=True):
        """Initialize the ReverseIPScanner with configuration parameters."""
        self.input_file = input_file
        self.threads_count = threads
        self.delay = delay
        self.output_file = output_file
        self.verbose = verbose
        self.address_q = Queue()
        self.total_domains_found = 0
        self.scanned_addresses = 0
        self.total_addresses = 0

    def clear_console(self):
        """Clear the console screen."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_banner(self):
        """Display the application banner."""
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
        print(f"{Fore.BLUE}XenpaiBot - The Ultimate Pentesting Bot {Style.RESET_ALL}")
        print(f"Author : {Fore.YELLOW}Kanezama{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Version: 2.0{Style.RESET_ALL}")

    def get_input_file(self):
        """Prompt user for input file if not provided."""
        if self.input_file and os.path.isfile(self.input_file):
            return self.input_file
        
        try:
            while True:
                input_file = input(Fore.YELLOW + "[*] Input Domain/IP File: " + Style.RESET_ALL).strip()
                if os.path.isfile(input_file):
                    self.input_file = input_file
                    return input_file
                else:
                    print(Fore.RED + f"[!] File '{input_file}' not found. Please try again.")
        except KeyboardInterrupt:
            print(Fore.RED + "\n[!] Process interrupted by user.")
            sys.exit(0)

    def load_addresses(self):
        """Load addresses from the input file."""
        try:
            with open(self.input_file, "r") as f:
                addresses = [line.strip() for line in f.readlines() if line.strip()]
            
            self.total_addresses = len(addresses)
            if not addresses:
                print(Fore.RED + "[!] No addresses found in the input file.")
                return False
            
            print(Fore.BLUE + f"[*] Loaded {self.total_addresses} addresses from {self.input_file}")
            for address in addresses:
                self.address_q.put(address)
            return True
        except Exception as e:
            print(Fore.RED + f"[!] Error loading addresses: {str(e)}")
            return False

    def run_scan(self):
        """Run the reverse IP scan with multiple threads."""
        print(Fore.YELLOW + f"[*] Starting scan with {self.threads_count} threads and {self.delay}s delay")
        
        # Create directory for output if it doesn't exist
        os.makedirs(os.path.dirname(self.output_file) if os.path.dirname(self.output_file) else '.', exist_ok=True)
        
        # Initialize or clear the output file
        with open(self.output_file, 'w') as f:
            f.write(f"# XenpaiBot Reverse IP Scan Results\n")
            f.write(f"# Scan started at: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        threads = []
        for i in range(self.threads_count):
            thread = ReverseIPWorker(
                self.address_q, 
                self.delay, 
                self.output_file,
                self.update_progress,
                self.verbose,
                f"Worker-{i+1}"
            )
            threads.append(thread)
            thread.daemon = True
            thread.start()
        
        try:
            # Monitor progress
            while not self.address_q.empty():
                print(f"\r{Fore.CYAN}[*] Progress: {self.scanned_addresses}/{self.total_addresses} addresses scanned, {self.total_domains_found} domains found{Style.RESET_ALL}", end='')
                time.sleep(1)
            
            # Wait for all threads to complete
            self.address_q.join()
            
            print(f"\n{Fore.GREEN}[*] Scan completed. {self.total_domains_found} domains found across {self.scanned_addresses} addresses.")
            print(f"{Fore.YELLOW}[*] Results saved to: {self.output_file}{Style.RESET_ALL}")
            
        except KeyboardInterrupt:
            print(f"\n{Fore.RED}[!] Scan interrupted. Partial results saved to: {self.output_file}{Style.RESET_ALL}")
            sys.exit(0)

    def update_progress(self, domains_found=0):
        """Update the progress counters."""
        self.scanned_addresses += 1
        self.total_domains_found += domains_found

    def run(self):
        """Main execution method."""
        self.clear_console()
        self.print_banner()
        
        if not self.input_file:
            self.get_input_file()
        
        if not self.load_addresses():
            return
        
        self.run_scan()


class ReverseIPWorker(Thread):
    """Worker thread for performing reverse IP lookups."""
    
    def __init__(self, address_q, delay, output_file, progress_callback, verbose, name="Worker"):
        super().__init__(name=name)
        self.address_q = address_q
        self.delay = delay
        self.output_file = output_file
        self.progress_callback = progress_callback
        self.verbose = verbose
        self.session = requests.Session()
        self.session.headers.update({
            'authority': 'domains.yougetsignal.com',
            'accept': 'application/json',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'referer': 'https://www.yougetsignal.com/tools/web-sites-on-web-server/',
            'origin': 'https://www.yougetsignal.com',
        })

    def run(self):
        """Thread execution method."""
        while not self.address_q.empty():
            try:
                ipaddy = self.address_q.get(timeout=1)
                try:
                    domains_found = self.reverse_ip(ipaddy)
                    self.progress_callback(domains_found)
                except Exception as e:
                    if self.verbose:
                        print(f"{Fore.RED}[!] Error processing {ipaddy}: {str(e)}")
                    self.progress_callback(0)
                finally:
                    self.address_q.task_done()
                    # Respect the delay to avoid overloading the server
                    time.sleep(self.delay)
            except Exception:
                pass

    def reverse_ip(self, ipaddy):
        """Perform reverse IP lookup for a given address."""
        try:
            # Add randomization to avoid detection
            jitter = self.delay * 0.5 * (1 + (time.time() % 1))
            time.sleep(jitter)
            
            response = self.session.post(
                'https://domains.yougetsignal.com/domains.php', 
                data={'remoteAddress': ipaddy},
                timeout=10
            )
            
            if 'Fail' in response.text:
                if self.verbose:
                    print(f"{Fore.RED}[!] Limit reached for {ipaddy}. Change your IP or try again later.")
                return 0

            try:
                json_data = json.loads(response.text)
                if json_data.get('status') == 'Fail':
                    if self.verbose:
                        print(f"{Fore.RED}[!] API error for {ipaddy}: {json_data.get('message', 'Unknown error')}")
                    return 0
                    
                loaded_json = json_data.get('domainArray', [])
            except json.JSONDecodeError:
                if self.verbose:
                    print(f"{Fore.YELLOW}[*] No domains found or invalid response for {ipaddy}")
                return 0

            domains_count = len(loaded_json)
            if domains_count > 0:
                if self.verbose:
                    print(f"{Fore.GREEN}[+] {domains_count} domains found for {ipaddy}")
                
                with open(self.output_file, 'a') as output_file:
                    output_file.write(f'\n## Results for {ipaddy}: {domains_count} domains\n')
                    for domain in loaded_json:
                        output_file.write(domain[0] + '\n')
                return domains_count
            else:
                if self.verbose:
                    print(f"{Fore.YELLOW}[*] No domains found for {ipaddy}")
                return 0
                
        except requests.RequestException as e:
            if self.verbose:
                print(f"{Fore.RED}[!] Request error for {ipaddy}: {str(e)}")
            return 0


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="XenpaiBot - Reverse IP Scanner")
    parser.add_argument("-i", "--input", help="Input file containing domains/IPs")
    parser.add_argument("-o", "--output", default="results.txt", help="Output file (default: results.txt)")
    parser.add_argument("-t", "--threads", type=int, default=5, help="Number of threads (default: 5)")
    parser.add_argument("-d", "--delay", type=float, default=1.0, help="Delay between requests in seconds (default: 1.0)")
    parser.add_argument("-q", "--quiet", action="store_true", help="Quiet mode (less output)")
    return parser.parse_args()


def main():
    """Main entry point for the script."""
    try:
        args = parse_arguments()
        scanner = ReverseIPScanner(
            input_file=args.input,
            threads=args.threads,
            delay=args.delay,
            output_file=args.output,
            verbose=not args.quiet
        )
        scanner.run()
    except KeyboardInterrupt:
        print(f"{Fore.RED}\n[!] Process interrupted by user.{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        print(f"{Fore.RED}\n[!] Unexpected error: {str(e)}{Style.RESET_ALL}")
        sys.exit(1)


if __name__ == "__main__":
    main()
