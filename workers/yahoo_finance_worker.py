from csv import Error
import requests
from lxml import html
import time

class YahooFinanceWorker():
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (compatible; MiApp/1.0)"
    }
    BASE_URL = 'https://finance.yahoo.com/quote/'
    # def __init__(self):
        # self._symbol = symbol
        # self._headers = {
        #     "User-Agent": "Mozilla/5.0 (compatible; MiApp/1.0)"
        # }
        # self._base_url = 'https://finance.yahoo.com/quote/'
        # self._url = f'{base_url}{self._symbol}'
        # self._base_url = 'https://finance.yahoo.com/quote/'
        
        # self.start()


    # def run(self):
    #     r = requests.get(self._url, headers=self._headers)
    #     page_contents = html.fromstring(r.text)
    #     price = float(page_contents.xpath('//span[@data-testid="qsp-price"]/text()')[0])
    #     print(f'The price of {self._symbol} is: {price}')

    # Private method
    @classmethod
    def __fetch_price(cls, symbol):
        for attempt in range(3):
            try:
                url = f'{cls.BASE_URL}{symbol}'
                response = requests.get(url, headers=cls.HEADERS, timeout=10000)
                
                if response.status_code == 429:
                    time.sleep(2 ** attempt)
                    continue

                response.raise_for_status()

                if response.status_code != 200:
                    raise Exception(f'The status code was: {response.status_code}')

                return response
            except Error as err:
                raise Exception(f'Exception in the __fetch_price: {err}')

    @classmethod
    def get_price(cls, symbol):
        tree = cls.__fetch_price(symbol)
        page_contents = html.fromstring(tree.text)
        price_object = page_contents.xpath('//span[@data-testid="qsp-price"]/text()')

        if len(price_object) <= 0 or not price_object:
            return symbol, 0.0
        
        print(symbol, float(price_object[0].replace(',', '')))
        return symbol, float(price_object[0].replace(',', ''))