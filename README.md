# Whois Similarity Check

## Overview

This tool compares the WHOIS information of domains to identify similarities and determine if they likely belong to the same company. It utilizes the python-whois library for fetching WHOIS information and provides a similarity score based on relevant fields.

## Usage

1. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2. Run the script with the following command:
    ```bash
    python whois_check.py -t <threshold> -b <baseline_file> -dl <domain_list_file>
    ```

    - `-t, --threshold`: Threshold for similarity score (default is 1.0, an exact match).
    - `-b, --baseline`: Baseline domain list file, used to establish a baseline for comparison.
    - `-dl, --domain-list`: Domain list file with target domains to check if WHOIS is similar to baseline domains.

3. Example:
    ```bash
    python whois_check.py -t 0.8 -b baseline_domains.txt -dl test_domains.txt
    ```

## Command-line Arguments

- `-t, --threshold`: Set the threshold for the similarity score. Only print results with a score greater than or equal to the threshold.
- `-b, --baseline`: Specify the baseline domain list file.
- `-dl, --domain-list`: Specify the domain list file to check for similarity.

## Output

The tool will print the similarity score between each test domain and the baseline domains, based on the specified threshold.

## Requirements

- python-whois
- difflib
- argparse 

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
