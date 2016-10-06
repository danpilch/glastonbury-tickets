from selenium import webdriver
import threading
import argparse
import os


class GlastonburyTickets(threading.Thread):

    def __init__(self, base_url, proxy_file):
        self.threads = []
        self.base_url = base_url
        self.proxy_list = [line.strip() for line in open(proxy_file, 'r')]

    def proxy_manager(self):
        pass

    def get_html(self, proxy):
        print "Running FF instance for proxy: {0}".format(proxy)
        driver = webdriver.Firefox()
        driver.get(self.base_url)
        source = driver.page_source
        driver.quit()
        return source

    def spawn_browsers(self):
        for proxy in self.proxy_list:
            t = threading.Thread(target=self.calc_proxy_efficiency, args=(proxy,))
            self.threads.append(t)
            t.start()

    def calc_proxy_efficiency(self, proxy):
        for x in range(0, 3):
            html = self.get_html(proxy)
            print html

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
