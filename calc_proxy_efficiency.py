from selenium.webdriver.common.proxy import *
from selenium import webdriver
import threading
import argparse
import os

class GlastonburyTickets(threading.Thread):

    def __init__(self, base_url, proxy_file):
        self.threads = []
        self.base_url = base_url
        self.proxy_list = [line.strip() for line in open(proxy_file, 'r')]
        self.proxy_efficieny = {}

    def proxy_manager(self, proxy_host):
        proxy = Proxy({
            'proxyType': ProxyType.MANUAL,
            'httpProxy': proxy_host,
            'ftpProxy': proxy_host,
            'sslProxy': proxy_host,
            'noProxy': ''
        })
        return proxy
 

    def get_html(self, proxy):

        print "Running FF instance for proxy: {0}".format(proxy)

        # Load page in Firefox and extract HTML
        proxy_instance = self.proxy_manager(proxy)
        driver = webdriver.Firefox(proxy=proxy_instance)
        driver.get(self.base_url)
        source = driver.page_source
        driver.quit()

        return source

    def spawn_browsers(self):

        print "\nSpawning browsers for each proxy: {0} browsers will be loaded simultaneously".format(len(self.proxy_list))

        for proxy in self.proxy_list:
            t = threading.Thread(target=self.calc_proxy_efficiency, args=(proxy,))
            self.threads.append(t)
            t.start()

    def calc_proxy_efficiency(self, proxy):

        try_count = 5

        print "Will now try and load the site {0} times for proxy {1}".format(5, proxy)

        # Set initial success count to 0
        self.proxy_efficieny[proxy] = 0

        # Try via proxy consecuitively {try_count} times in a row
        for x in range(0, 5):

            # Get the HTML of the page
            html = self.get_html(proxy)

            # If we are not on the holding page, we'll increment the success count for this proxy
            if "holding page" not in html:
                self.proxy_efficieny[proxy] += 1

        print "\nSuccess count for each proxy:"
        print self.proxy_efficieny


def main():

    # Get current directory
    dir_path = os.path.dirname(os.path.realpath(__file__))

    # Argument parser
    parser = argparse.ArgumentParser(description="Attempt to get past the great Glastonbury wait")
    parser.add_argument("--base-url", "-u", help="Glastonbury URL", default="http://glastonbury.seetickets.com")
    parser.add_argument("--proxy-file", "-f", help="Path to proxy list", default=dir_path+"/proxy_list.txt")
    args = parser.parse_args()

    # Start the process
    tickets = GlastonburyTickets(base_url=args.base_url, proxy_file=args.proxy_file)
    tickets.spawn_browsers()


if __name__ == "__main__":
    main()
