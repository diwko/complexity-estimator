from time import time
import signal
from numpy.polynomial.polynomial import polyfit
from numpy.polynomial.polynomial import polyval
from numpy.polynomial.polynomial import polyroots
import logging


def log_times(f):
    logging.basicConfig(filename='measures.log',
                        format='%(levelname)s:%(message)s',
                        level=logging.INFO)

    def tmp(s, n):
        t = f(s, n)
        logging.info("\tSIZE: {} - TIME: {}".format(n, t))
        return t
    return tmp


class TimeReachedException(Exception):
    def __init__(self, msg):
        self.strerror = msg


class ComplexityEstimator:
    def __init__(self, init_fun=(lambda x: None), main_fun=(lambda x: None),
                 clean_fun=(lambda x: None), time_limit=30):
        self.init_fun = init_fun
        self.main_fun = main_fun
        self.clean_fun = clean_fun
        self.time_limit = time_limit

    @log_times
    def get_exec_time(self, problem_size):
        self.init_fun(problem_size)

        start_time = time()
        self.main_fun(problem_size)
        stop_time = time()

        self.clean_fun(problem_size)

        return stop_time - start_time

    def sig_alrm_handler(self, signum, frame):
        raise TimeReachedException("Time limit was reached")

    def get_run_times(self):
        signal.signal(signal.SIGALRM, self.sig_alrm_handler)
        signal.alarm(self.time_limit)
        run_times = []
        try:
            problem_size = 1
            while problem_size < 10e8:
                run_times.append((problem_size,
                                  self.get_exec_time(problem_size)))
                problem_size *= 2
        except TimeReachedException:
            return run_times

    @staticmethod
    def convert_data(data):
        sizes = [test[0] for test in data]
        times = [test[1] for test in data]
        return sizes, times

    @staticmethod
    def get_polynomial_coefficients(x, y):
        return polyfit(x, y, 3)

    @staticmethod
    def get_time_estimating_fun(coefficients):
        return lambda n: polyval(n, coefficients)

    @staticmethod
    def get_size_estimating_fun(coefficients):
        c = coefficients[:]

        def tmp(t):
            c[0] -= t
            roots = polyroots(c)
            for root in roots:
                if root > 0:
                    return int(root.real)
            return 0
        return tmp

    @staticmethod
    def get_big_o(x, y):
        dydivdx = []
        for i in range(len(x) - 1):
            dydivdx.append((y[i+1] - y[i])/(x[i+1]-x[i]))

        differences = []
        for i in range(len(dydivdx) - 1):
            try:
                differences.append(dydivdx[i + 1] / dydivdx[i])
            except ZeroDivisionError:
                continue

        factor = sum(differences)/len(differences)

        if factor < 0.2:
            return 'O(1)'
        elif factor < 0.6:
            return 'log(N)'
        elif factor < 1.1:
            return 'O(N)'
        elif factor < 1.5:
            return 'O(Nlog(N))'
        elif factor < 2.5:
            return 'O(N^2)'
        elif factor < 4.5:
            return 'O(N^3)'
        elif factor < 8.5:
            return 'O(N^4)'
        elif factor < 16.5:
            return 'O(N^5)'
        else:
            return "Duża złożoność, może nawet wykładnicza :("

    def estimate_complexity(self):
        data = self.convert_data(self.get_run_times())
        o_symbol = self.get_big_o(data[0], data[1])
        coefficients = self.get_polynomial_coefficients(data[0], data[1])
        write_fun_to_file(coefficients)
        estimate_time_fun = self.get_time_estimating_fun(coefficients)
        estimate_size_fun = self.get_size_estimating_fun(coefficients)

        return o_symbol, estimate_time_fun, estimate_size_fun


def estimate_complexity(fun):
    def tmp(n):
        estimator = ComplexityEstimator(main_fun=fun, time_limit=5)
        data = estimator.estimate_complexity()
        print("Szacowana złożoność: {}".format(data[0]))
        return data
    return tmp


def write_fun_to_file(coefficients):
    time_estimate = "from argparse import ArgumentParser\n" \
                    "from numpy.polynomial.polynomial import polyval\n" \
                    "parser = ArgumentParser(description='time estimator')\n" \
                    "parser.add_argument('n', help='problem size')\n" \
                    "args = parser.parse_args()\ncoefficients = __C__\n" \
                    "print(polyval(int(args.n), coefficients))\n"

    size_estimate = "from argparse import ArgumentParser\n" \
                    "from numpy.polynomial.polynomial import polyroots\n" \
                    "parser = ArgumentParser(description='size estimator')\n" \
                    "parser.add_argument('t', help='max time')\n" \
                    "args = parser.parse_args()\n" \
                    "coefficients = __C__\n" \
                    "coefficients[0] -= int(args.t)\n" \
                    "roots = polyroots(coefficients)\n" \
                    "for root in roots:\n" \
                    "\tif root > 0:\n" \
                    "\t\tprint(int(root.real))\n" \
                    "print('Nie udało się obliczyć')\n"

    coefficients_string = "[" + str(coefficients[0])
    for c in range(1, len(coefficients)):
        coefficients_string += ", " + str(coefficients[c])
    coefficients_string += "]"

    time_code = time_estimate.replace("__C__", coefficients_string)
    size_code = size_estimate.replace("__C__", coefficients_string)

    with open("time_estimate_fun.py", "w") as f:
        f.write(time_code)

    with open("size_estimate_fun.py", "w") as f:
        f.write(size_code)
