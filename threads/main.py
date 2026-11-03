import time
import threading

def calculate_square(number):
    sum_squares = 0
    for i in range(number):
        sum_squares += i ** 2
    print(sum_squares)


def sleep_a_little(seconds):
    time.sleep(seconds)


def main():
    calc_start_time = time.time()
    current_thread = []

    for i in range(5):
        max_value = (i + 1) * 1000000
        t = threading.Thread(target=calculate_square, args=(max_value, ))
        t.start()
        # t.join()
        # current_thread.append(t)

    # for i in range(len(current_thread)):
    #     current_thread[i].join()

    print('Calculating sum of squares took: ', round(time.time() - calc_start_time, 1))
    
    sleep_start_time = time.time()
    current_thread = []
    for seconds in range(1, 6):
        t = threading.Thread(target=sleep_a_little, args=(seconds, ))
        t.start()
        # t.join()
        # current_thread.append(t)
    
    # for i in range(len(current_thread)):
    #     current_thread[i].join()

    print('Sleeping took: ', round(time.time() - sleep_start_time, 1))


if __name__ == "__main__":
    main()