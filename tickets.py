from selenium.webdriver.common.proxy import *
from selenium import webdriver
import threading

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
 

    def get_webdriver(self, proxy):

        print "Running FF instance for proxy: {0}".format(proxy)

        # Load page in Firefox and extract HTML
        proxy_instance = self.proxy_manager(proxy)
        driver = webdriver.Firefox(proxy=proxy_instance)
        driver.get(self.base_url)

        return driver

    def spawn_browsers(self):

        print "\nSpawning browsers for each proxy: {0} browsers will be loaded simultaneously".format(len(self.proxy_list))

        for proxy in self.proxy_list:
            t = threading.Thread(target=self.calc_proxy_efficiency, args=(proxy,))
            self.threads.append(t)
            t.start()

    def find_successful_host_from_proxies(self):

        print "\nSpawning browsers for each proxy: {0} browsers will be loaded simultaneously".format(len(self.proxy_list))

        for proxy in self.proxy_list:
            t = threading.Thread(target=self.find_successful_host, args=(proxy,))
            self.threads.append(t)
            t.start()

    def calc_efficiency_for_hosts(self):

        print "\nSpawning browsers for each proxy: {0} browsers will be loaded simultaneously".format(len(self.proxy_list))

        for proxy in self.proxy_list:
            t = threading.Thread(target=self.calc_proxy_efficiency, args=(proxy,))
            self.threads.append(t)
            t.start()

    def find_successful_host(self, proxy):

        print "Will now check if connection is successful for proxy {0}".format(proxy)

        # Get the HTML of the page
        driver = self.get_webdriver(proxy)
        html = driver.page_source

        # If we appear to be on the holding page we'll close the browser
        if "holding page" in html or "processing the maximum" in html or "now sold out" in html:
            driver.quit()

    def calc_proxy_efficiency(self, proxy):

        try_count = 5

        print "Will now try and load the site {0} times for proxy {1}".format(5, proxy)

        # Set initial success count to 0
        self.proxy_efficieny[proxy] = 0

        # Try via proxy consecuitively {try_count} times in a row
        for x in range(0, 5):

            # Get the HTML of the page
            driver = self.get_webdriver(proxy)
            html = driver.page_source
            driver.quit()

            # If we are not on the holding page, we'll increment the success count for this proxy
            if "holding page" not in html and "processing the maximum" not in html:
                self.proxy_efficieny[proxy] += 1

        print "\nSuccess count for each proxy:"
        print self.proxy_efficieny