from tickets import GlastonburyTickets
import argparse
import os

def main():

    # Get current directory
    dir_path = os.path.dirname(os.path.realpath(__file__))

    # Argument parser
    parser = argparse.ArgumentParser(description="Attempt to get past the great Glastonbury wait")
    parser.add_argument("--base-url", "-u", help="Glastonbury URL", default="http://glastonbury.seetickets.com")
    parser.add_argument("--proxy-file", "-f", help="Path to proxy list", default=dir_path+"/proxy_list.txt")
    args = parser.parse_args()

    # Start the process
    tickets = GlastonburyTickets(base_url=args.base_url, proxy_file=args.proxy_file, thread_pool=5)
    tickets.calc_efficiency_for_hosts()

if __name__ == "__main__":
    main()
