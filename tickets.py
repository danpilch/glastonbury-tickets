from selenium.webdriver.common.proxy import *
from selenium import webdriver
import threading
from concurrent.futures import ThreadPoolExecutor

class GlastonburyTickets(threading.Thread):

    def __init__(self, base_url, proxy_file, thread_pool):
        self.threads = []
        self.thread_pool = thread_pool
        self.base_url = base_url
        self.proxy_list = [line.strip() for line in open(proxy_file, 'r')]
        self.proxy_efficieny = {}
        self.proxy_efficieny_semaphore = threading.BoundedSemaphore()
        self.found_valid_proxy = False

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

        print("Running FF instance for proxy: {!s}".format(proxy))

        # Load page in Firefox and extract HTML
        proxy_instance = self.proxy_manager(proxy)
        driver = webdriver.Firefox(proxy=proxy_instance)
        driver.get(self.base_url)

        return driver

    def spawn_browsers(self):

        print("\nSpawning browsers for each proxy: {:d} browsers will be loaded simultaneously".format(len(self.proxy_list)))

        for proxy in self.proxy_list:
            t = threading.Thread(target=self.calc_proxy_efficiency, args=(proxy,))
            self.threads.append(t)
            t.start()

    def find_successful_host_from_proxies(self):

        print("\nSpawning browsers for each proxy: {:d} browsers will be loaded simultaneously".format(len(self.proxy_list)))

        with ThreadPoolExecutor(max_workers=self.thread_pool) as executor:
            for proxy in self.proxy_list:
                future = executor.submit(self.find_successful_host, proxy)

    def calc_efficiency_for_hosts(self):

        print("\nSpawning browsers for each proxy: {:d} browsers will be loaded simultaneously".format(len(self.proxy_list)))

        with ThreadPoolExecutor(max_workers=self.thread_pool) as executor:
            for proxy in self.proxy_list:
                future = executor.submit(self.calc_proxy_efficiency, proxy)

    def find_successful_host(self, proxy):

        print("Will now check if connection is successful for proxy {!s}".format(proxy))

        if self.found_valid_proxy == True:
            return

        # Get the HTML of the page
        driver = self.get_webdriver(proxy)
        html = driver.page_source

        # If we appear to be on the holding page we'll close the browser
        if "holding page" in html or "processing the maximum" in html or "now sold out" in html:
            driver.quit()
        else:
            self.found_valid_proxy = True


    def calc_proxy_efficiency(self, proxy):

        try_count = 5

        print("Will now try and load the site {:d} times for proxy {!s}".format(5, proxy))

        # Set initial success count to 0
        self.proxy_efficieny_semaphore.acquire()
        self.proxy_efficieny[proxy] = 0
        self.proxy_efficieny_semaphore.release()

        # Try via proxy consecuitively {try_count} times in a row
        for x in range(0, 5):

            # Get the HTML of the page
            driver = self.get_webdriver(proxy)
            html = driver.page_source
            driver.quit()

            # If we are not on the holding page, we'll increment the success count for this proxy
            if "holding page" not in html and "processing the maximum" not in html:
                self.proxy_efficieny_semaphore.acquire()
                self.proxy_efficieny[proxy] += 1
                self.proxy_efficieny_semaphore.release()

        print("\nSuccess count for each proxy:")
        print(self.proxy_efficieny)
