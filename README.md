# Sublock
A Python-based tool to discover subdomains for a given domain using crt.sh certificate transparency logs and check their HTTP status codes. The tool filters subdomains based on valid DNS records and displays the HTTP response status for each.

![sublock](https://github.com/user-attachments/assets/d6631915-0311-4ef3-a37d-f61d14383a0c)

     Fetches subdomains from the crt.sh certificate transparency log database.
     Filters out invalid subdomains using DNS resolution.
     Checks and displays the HTTP status code for each valid subdomain.
    


# Requirements

To use this tool, ensure you have the following Python libraries installed:



    pip install -r requirements.txt

# Dependencies

    requests: For making HTTP requests.
    dnspython: For DNS resolution of subdomains.
    

# Usage

    Clone the repository or download the script.
    Install the required dependencies:
    pip install -r requirements.txt

Run the script with a specified domain:

bash

    python subdomain_finder.py example.com

Command-line Arguments

    domain: The target domain to find subdomains for.
    threads (optional): Number of threads for parallel status checking (default: 10).
