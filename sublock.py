import requests
import concurrent.futures
import dns.resolver
import argparse
from colorama import Fore, Style, init

# Initialize colorama to auto-reset color styles after each print
init(autoreset=True)

# Function to display an ASCII logo
def display_ascii_logo():
    logo = """
     ____        _     _            _         
    / ___| _   _| |__ | | ___   ___| | __     
    \___ \| | | | '_ \| |/ _ \ / __| |/ /     
     ___) | |_| | |_) | | (_) | (__|   <      
    |____/ \__,_|_.__/|_|\___/ \___|_|\_\     
                                            
    Subdomain Finder             By:F3b!n
    """
    print(logo)

# Function to fetch subdomains from crt.sh
def fetch_subdomains(domain):
    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            subdomains = set()
            for entry in data:
                name_value = entry['name_value']
                subdomains.update(name_value.splitlines())
            return sorted(subdomains)
        else:
            print(f"Failed to fetch subdomains from crt.sh. Status code: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error fetching subdomains: {e}")
        return []

# Function to check the status of a subdomain
def check_subdomain(subdomain):
    url = f"http://{subdomain}"
    try:
        response = requests.get(url, timeout=3)
        status_code = response.status_code
        return (subdomain, status_code)
    except requests.ConnectionError:
        return (subdomain, "Connection Failed")
    except requests.Timeout:
        return (subdomain, "Timeout")

# Function to filter subdomains with valid DNS records
def resolve_dns(subdomains):
    valid_subdomains = []
    resolver = dns.resolver.Resolver()
    for subdomain in subdomains:
        try:
            resolver.resolve(subdomain, 'A')
            valid_subdomains.append(subdomain)
        except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.LifetimeTimeout):
            pass
    return valid_subdomains

# Main function to find and check subdomains
def find_and_check_subdomains(domain, threads=10):
    print(f"Fetching subdomains for: {domain}")
    subdomains = fetch_subdomains(domain)
    
    if not subdomains:
        print("No subdomains found.")
        return
    
    print(f"Resolving DNS for found subdomains...")
    valid_subdomains = resolve_dns(subdomains)
    
    if not valid_subdomains:
        print("No valid subdomains with DNS resolution.")
        return
    
    print(f"Found {len(valid_subdomains)} valid subdomains. Checking HTTP status...")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        results = executor.map(check_subdomain, valid_subdomains)
    
    for subdomain, status in results:
        if isinstance(status, int) and 200 <= status < 300:
            # Status is 2xx (OK): print in green
            print(f"{subdomain} - {Fore.GREEN}{[status]}{Style.RESET_ALL}")
        else:
            # Status is not OK: print in default color
            print(f"{subdomain} - {[status]}")

# Parse command-line arguments
def main():
    # Display ASCII logo when the program loads
    display_ascii_logo()
    
    parser = argparse.ArgumentParser(description="Automated Subdomain Finder and Status Checker")
    parser.add_argument('domain', help="The target domain to find subdomains for")
    parser.add_argument('--threads', type=int, default=10, help="Number of threads for parallel checking (default: 10)")
    
    args = parser.parse_args()
    find_and_check_subdomains(args.domain, args.threads)

if __name__ == "__main__":
    main()
