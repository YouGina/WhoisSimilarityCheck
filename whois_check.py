import whois, sys, argparse
from difflib import SequenceMatcher

def get_domain_info(domain):
    try:
        domain_info = whois.whois(domain)
        return domain_info
    except whois.parser.PywhoisError:
        return None

def compare_domains(bl_whois_data, target_whois_data):
    debug = False

    if bl_whois_data is None or target_whois_data is None:
        return None

    if debug:
        print(bl_whois_data.name + " " + bl_whois_data.registrar + " " + str(bl_whois_data.emails), file=sys.stderr)
        print(target_whois_data.name + " " + target_whois_data.registrar + " " + str(target_whois_data.emails), file=sys.stderr)
        print("________________________________")

    # Compare relevant fields to determine similarity
    name_similarity = SequenceMatcher(None, bl_whois_data.name, target_whois_data.name).ratio()
    registrar_similarity = SequenceMatcher(None, bl_whois_data.registrar, target_whois_data.registrar).ratio()

    email_similarity = 0.0
    if bl_whois_data.emails and target_whois_data.emails:
        email_similarity = SequenceMatcher(None, str(bl_whois_data.emails), str(target_whois_data.emails)).ratio()

    # Calculate an overall similarity score
    overall_similarity = (name_similarity + registrar_similarity) / 2

    return overall_similarity

def read_domains_from_file(filename):
    with open(filename, 'r') as file:
        domains = [line.strip() for line in file.readlines() if line.strip()]
    return domains

def main():
    parser = argparse.ArgumentParser(description="Compare domain information.")
    parser.add_argument("-t", "--threshold", type=float, default=1.0, help="Threshold for similarity score (default is 1.0, exact match)")
    parser.add_argument("-b", "--baseline", required=True, help="Baseline domain list file, used to get baseline", default="baseline_domains.txt")
    parser.add_argument("-dl", "--domain-list", required=True, help="Domain list file with target domains to check if whois is similar to baseline domains", default="test_domains.txt")

    args = parser.parse_args()

    baseline_domains_list = read_domains_from_file(args.baseline)
    test_domains = read_domains_from_file(args.domain_list)

    baseline_domains = []
    for bl in baseline_domains_list:
        baseline_domains.append(get_domain_info(bl))



    for test_domain in test_domains:
        try:
            test_domain_whois = get_domain_info(test_domain)
            for baseline_domain in baseline_domains:
                similarity_score = compare_domains(test_domain_whois, baseline_domain)
                if similarity_score is not None and similarity_score >= args.threshold:
                    print(f"Similarity between {test_domain} and {baseline_domain.domain_name[0]}: {similarity_score}")
        except KeyboardInterrupt:
            sys.exit()
        except:
            print("Domain: "+test_domain+" likely not registered", file=sys.stderr)

if __name__ == "__main__":
    main()
