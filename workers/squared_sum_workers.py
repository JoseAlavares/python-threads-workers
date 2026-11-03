from threading import Thread

class SquaredSumWorker(Thread):
    def __init__(self, number, **kwargs):
        self._number = number
        super(SquaredSumWorker, self).__init__(**kwargs)
        self.start()


    def _calculate_square(self):
        sum_squares = 0
        for i in range(self._number):
            sum_squares += i ** 2
        print(sum_squares)


    def run(self):
        self._calculate_square()