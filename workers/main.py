from concurrent.futures import ThreadPoolExecutor, as_completed


from squared_sum_workers import SquaredSumWorker
from sleepy_worker import SleepyWorker
from wiki_worker import WikiWorker
from yahoo_finance_worker import YahooFinanceWorker

import time
import os

def primitive_thread_handling():
    current_workers = []
    calc_start_time = time.time()

    for i in range(5):
        max_value = (i + 1) * 1000000
        squared_sum_worker = SquaredSumWorker(number=max_value)
        current_workers.append(squared_sum_worker)

    for i in range(len(current_workers)):
        current_workers[i].join()

    print('Calculating sum of squares took: ', round(time.time() - calc_start_time, 1))

    current_workers = []
    sleep_start_time = time.time()
    for i in range(1, 6):
        sleepy_worker = SleepyWorker(seconds=i)
        current_workers.append(sleepy_worker)

    for i in range(len(current_workers)):
        current_workers[i].join()

    print('Sleeping took: ', round(time.time() - sleep_start_time, 1))


def main():
    # limit = 0
    start_time = time.time()
    wikiWorker = WikiWorker()
    # current_workers = []
    symbols = list(wikiWorker.get_sp_500_companies())
    quote = []
    number_of_workers = min(32, os.cpu_count() + 4)
    print(f'Number of workers: {number_of_workers}')

    with ThreadPoolExecutor(max_workers=number_of_workers) as executor:
        # futures = {executor.submit(YahooFinanceWorker.get_price, symbol): symbol for symbol in symbols}
        futures = {}
        for symbol in symbols:
            future = executor.submit(YahooFinanceWorker.get_price, symbol)
            futures[future] = symbol
            time.sleep(0.1)
        # for i in range(len(current_workers)):
        #     current_workers[i].join()

        for future in as_completed(futures):
            try:
                symbol, price = future.result()
                quote.append({ symbol: price })
            except Exception as err:
                print(f'Error ocurred in a thread: {err}')

    print(f'Extracting time took: {round(time.time() - start_time, 1)}')
    print(quote)

if __name__ == '__main__':
    main()