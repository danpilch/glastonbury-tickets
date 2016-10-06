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

    def proxy_manager(self, proxy_host):
        proxy = Proxy({
            'proxyType': ProxyType.MANUAL,
            'httpProxy': proxy_host,
            'ftpProxy': proxy_host,
            'sslProxy': proxy_host,
            'noProxy': ''
        })
        return proxy
 

    def browser(self, proxy, base_url):
        print "Running FF instance for proxy: {0}".format(proxy)
        proxy_instance = self.proxy_manager(proxy)
        driver = webdriver.Firefox(proxy=proxy_instance)
        driver.get(base_url)

    def spawn_browsers(self):
        for proxy in self.proxy_list:
            t = threading.Thread(target=self.browser, args=(proxy, self.base_url,))
            self.threads.append(t)
            t.start()

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
