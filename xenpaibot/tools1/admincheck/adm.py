import requests
import logging
import sys
import os
import concurrent.futures
from urllib.parse import urlparse
from colorama import Fore, Style, init
from tqdm import tqdm

# Initialize colorama
init(autoreset=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('admin_check.log')
    ]
)

logger = logging.getLogger(__name__)

# Get script directory path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

# Search directories for configuration files
SEARCH_DIRS = [
    os.path.dirname(os.path.abspath(__file__)),  # Current directory first
    BASE_DIR,
    os.path.join(BASE_DIR, "xenpaibot", "tools1", "admincheck"),
]

# Default files
DEFAULT_ADMIN_LIST = "list.txt"
RESULTS_FILE = "Results-adminpanel.txt"


def clear_screen():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def display_banner():
    """Display the tool banner."""
    try:
        clear_screen()
        print(Fore.CYAN + r"""
              _           _          _____ _               _    
     /\      | |         (_)        / ____| |             | |   
    /  \   __| |_ __ ___  _ _ __   | |    | |__   ___  ___| | __
   / /\ \ / _` | '_ ` _ \| | '_ \  | |    | '_ \ / _ \/ __| |/ /
  / ____ \ (_| | | | | | | | | | | | |____| | | |  __/ (__|   < 
 /_/    \_\__,_|_| |_| |_|_|_| |_|  \_____|_| |_|\___|\___|_|\_\
                                                             
           """ + Fore.MAGENTA + "XenpaiBot -" + Fore.WHITE + " Admin Panel Checker v2.0")
        print(f"{Fore.YELLOW}{'=' * 60}")
    except Exception as e:
        logger.error(f"Failed to display banner: {e}")


def find_file(filename):
    """Find a file in search directories or use absolute path."""
    # Check if it's an absolute path
    if os.path.isabs(filename) and os.path.exists(filename):
        return filename
        
    # Search in directories
    for directory in SEARCH_DIRS:
        file_path = os.path.join(directory, filename)
        logger.debug(f"Checking: {file_path}")
        
        if os.path.exists(file_path):
            logger.debug(f"Found '{filename}' in {directory}")
            return file_path
            
    return None


def load_list(filename):
    """Load list from file with error handling."""
    file_path = find_file(filename)

    if not file_path:
        logger.error(f"File '{filename}' not found in search directories.")
        return []

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = [line.strip() for line in file if line.strip() and not line.startswith('#')]
        
        if lines:
            logger.info(f"✅ '{filename}' loaded successfully ({len(lines)} entries)")
        else:
            logger.error(f"❌ '{filename}' is empty!")
        
        return lines
    except OSError as e:
        logger.error(f"Failed to read '{filename}': {e}")
        return []


def normalize_url(url):
    """Ensure URL has a scheme and proper formatting."""
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    
    return url.rstrip('/')


def save_result(url, result_file=None):
    """Save found admin panel URL to results file."""
    if result_file is None:
        result_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), RESULTS_FILE)
    
    try:
        with open(result_file, "a", encoding="utf-8") as file:
            file.write(url + "\n")
        logger.debug(f"Successfully saved: {url}")
        return True
    except OSError as e:
        logger.error(f"Failed to save result: {e}")
        return False


def check_single_admin_path(args):
    """Check a single admin path for a target."""
    target, path, timeout, user_agent = args
    url = f"{target}/{path.lstrip('/')}"
    
    headers = {
        'User-Agent': user_agent,
        'Accept': 'text/html,application/xhtml+xml,application/xml',
        'Connection': 'keep-alive',
    }
    
    try:
        response = requests.get(url, timeout=timeout, headers=headers, allow_redirects=True)
        
        if response.status_code == 200:
            # Check if it's not a generic 404 page (basic check)
            if len(response.text) > 500:  # Assuming most 404 pages are short
                domain = urlparse(target).netloc
                logger.info(f"{Fore.GREEN}✔ Found Admin Panel: {url}")
                save_result(url)
                return url, True
        
        return url, False
    
    except requests.RequestException:
        return url, False


def check_admin_panel(targets, admin_paths, timeout=5, max_workers=10):
    """Check multiple targets for admin panels using threading for performance."""
    logger.info(f"{Fore.CYAN}Starting admin panel check...")
    
    # Use a custom User-Agent to avoid being blocked
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    
    found_panels = []
    
    # Normalize all target URLs
    normalized_targets = [normalize_url(target) for target in targets]
    
    # Prepare all combinations of targets and paths
    combinations = [(target, path, timeout, user_agent) 
                   for target in normalized_targets 
                   for path in admin_paths]
    
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Use tqdm for progress bar
            results = list(tqdm(
                executor.map(check_single_admin_path, combinations),
                total=len(combinations),
                desc="Checking admin panels",
                unit="request"
            ))
            
            # Filter successful results
            found_panels = [url for url, found in results if found]
        
        logger.info(f"{Fore.CYAN}Admin panel check completed.")
        logger.info(f"{Fore.GREEN}Found {len(found_panels)} admin panels.")
        
        if found_panels:
            print(f"\n{Fore.GREEN}Found Admin Panels:{Style.RESET_ALL}")
            for panel in found_panels:
                print(f"{Fore.YELLOW}➜ {panel}")
        
        return found_panels
    
    except KeyboardInterrupt:
        logger.error(f"{Fore.RED}Program terminated by user (Ctrl + C)")
        sys.exit(0)
    
    except Exception as e:
        logger.error(f"{Fore.RED}An error occurred: {e}")
        return []


def validate_targets(targets):
    """Validate and normalize target URLs."""
    valid_targets = []
    for target in targets:
        target = target.strip()
        if target:
            valid_targets.append(normalize_url(target))
    return valid_targets


def main():
    """Main function to run the script."""
    try:
        display_banner()
        
        print(f"{Fore.CYAN}Enter target file or URL(s) separated by comma:{Style.RESET_ALL}")
        input_value = input(f"{Fore.WHITE}> {Style.RESET_ALL}").strip()
        
        targets = []
        if ',' in input_value:
            # Input contains comma-separated URLs
            targets = [t.strip() for t in input_value.split(',')]
        else:
            # Input is a filename or single URL
            if os.path.exists(input_value) or find_file(input_value):
                targets = load_list(input_value)
            else:
                targets = [input_value]  # Assume it's a single URL
        
        # Validate targets
        targets = validate_targets(targets)
        
        # Get admin paths
        admin_list_file = input(f"{Fore.CYAN}Admin paths file [{DEFAULT_ADMIN_LIST}]: {Style.RESET_ALL}").strip()
        if not admin_list_file:
            admin_list_file = DEFAULT_ADMIN_LIST
        
        admin_paths = load_list(admin_list_file)

        # Get timeout
        try:
            timeout_input = input(f"{Fore.CYAN}Request timeout in seconds [5]: {Style.RESET_ALL}").strip()
            timeout = int(timeout_input) if timeout_input else 5
        except ValueError:
            logger.warning("Invalid timeout value. Using default (5 seconds).")
            timeout = 5
            
        # Get number of threads
        try:
            workers_input = input(f"{Fore.CYAN}Number of concurrent requests [10]: {Style.RESET_ALL}").strip()
            max_workers = int(workers_input) if workers_input else 10
        except ValueError:
            logger.warning("Invalid workers value. Using default (10).")
            max_workers = 10

        if not targets:
            logger.error(f"{Fore.RED}No valid targets specified!")
            return
            
        if not admin_paths:
            logger.error(f"{Fore.RED}Admin paths list '{admin_list_file}' not found or empty!")
            return

        print(f"\n{Fore.YELLOW}Configuration:{Style.RESET_ALL}")
        print(f"  {Fore.WHITE}Targets: {len(targets)}")
        print(f"  {Fore.WHITE}Admin paths: {len(admin_paths)}")
        print(f"  {Fore.WHITE}Total requests: {len(targets) * len(admin_paths)}")
        print(f"  {Fore.WHITE}Timeout: {timeout} seconds")
        print(f"  {Fore.WHITE}Concurrent requests: {max_workers}")
        print(f"{Fore.YELLOW}{'=' * 60}{Style.RESET_ALL}\n")
        
        input(f"{Fore.CYAN}Press Enter to start...{Style.RESET_ALL}")
        
        # Run the check
        check_admin_panel(targets, admin_paths, timeout, max_workers)
        
        print(f"\n{Fore.CYAN}Results saved to: {os.path.abspath(RESULTS_FILE)}")

    except KeyboardInterrupt:
        logger.error(f"{Fore.RED}Program terminated by user (Ctrl + C)")
        sys.exit(0)
        
    except Exception as e:
        logger.error(f"{Fore.RED}An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
