import sympy as sp
import matplotlib.pyplot as plt
from sympy import sympify, Symbol
import numpy as np
import time


class Bisection:

    def __init__(self, func, x1, x2, maxError, maxIteration):
        self.curr_pos = 0
        self.x = sp.Symbol('x')
        self.e = sp.Symbol('e')
        self.y = sp.Symbol('y')
        self.table = []
        self.time = 0
        self.upper = max(x1, x2)
        self.x1 = []
        self.y1 = []
        self.xu = []
        self.xl = []
        self.xks = []
        self.ys = []
        self.errors = []
        self.roots = []
        self.plots = []
        self.st = ""
        self.maxnum = 50
        self.maxer = 0
        self.xlf = 0
        self.xuf = 0
        self.st = func
        self.maxnum = maxIteration
        self.maxer = maxError
        self.xlf = x1
        self.xuf = x2
        self.H = sympify(self.st)

    # calculate all requirements of the method
    def calculate(self):
        time_begin = time.time()
        self.ys.append(float("%0.10f" % self.H.subs(self.x, self.xuf).subs(self.e, 2.71828182846)))
        self.ys.append(float("%0.10f" % self.H.subs(self.x, self.xlf).subs(self.e, 2.71828182846)))
        i = 0.0
        err = 1
        maxsize = self.maxnum
        if self.ys[1] > 0.0 and self.ys[0] < 0.0:
            temp = self.xlf
            self.xlf = self.xuf
            self.xuf = temp
        if self.is_converge() == False:
            return False
        # print(self.maxnum)
        for i in range(0, maxsize, 1):
            self.xl.append(self.xlf)
            self.xu.append(self.xuf)
            # print('xl =' + str(self.xlf))
            # print('xu =' + str(self.xuf))
            if (err <= self.maxer):
                break
            self.xk = self.xlf + self.xuf
            self.xk = self.xk / 2
            # print('self.xk =' + str(self.xk))
            x2 = [self.xk, self.xk]
            y2 = [-100, 100]
            self.plots.append((x2, y2))
            self.xks.append(self.xk)
            self.roots.append(self.xk)
            if i == 0:
                self.errors.append(1.0)
                # print(i)
            else:
                err = abs(self.xks[i] - self.xks[i - 1])  # edited
                self.errors.append(err)
            f = float("%0.10f" % self.H.subs(self.x, self.xk).subs(self.e, 2.71828182846))
            # print("fk =" + str(f))
            f2 = float("%0.10f" % self.H.subs(self.x, self.xlf).subs(self.e, 2.71828182846))
            # print("fl =" + str(f2))
            f3 = f * f2
            self.ys.append(f)
            # print(self.xl[0], self.xu[0])
            # print(f)
            self.table.append([self.xuf, self.xlf, self.xk, f, f2, err])
            if f3 < 0:
                self.xuf = self.xk
            else:
                self.xlf = self.xk
        i = min([self.xl[0], self.xu[0]])
        add = (abs((self.xu[0]) - (self.xl[0])) / 100)
        print("min = " + str(i) + " add = " + str(add) + "max = " + str(max([self.xl[0], self.xu[0]])))
        while i <= max([self.xl[0], self.xu[0]]):
            self.x1.append(i)
            # print("self.x=" + str(i) + " y = " + str(float((H.subs(self.x, i)).subs(self.e, 2.71828182846))))
            self.y1.append(float("%0.10f" % self.H.subs(self.x, i).subs(self.e, 2.71828182846)))
            i = i + add
        self.time = float("%0.10f" % (time.time() - time_begin))
        return True

    # plot all curves related to all iteration in single figure
    def plot(self, canvas):
        self.perform_iteration(canvas, 0)

    # return error of specific  iteration
    def get_error(self):
        return self.errors[-1]

    # set maximum number of iteration
    def set_max_it(self, max_it):
        return self.maxnum

    # return root of given function after solution
    def get_root(self):
        return self.xks[-1]

    # return maximum number of iteration
    def get_max_iteration(self):
        return self.maxnum

    # return total number of iteration taken to implement method
    def get_taken_iteration(self):
        return len(self.xks)

    # return the table of the details of each iteration
    def get_table(self):
        return self.table

    # determine if this method is converge or diverge
    def is_converge(self):
        if self.ys[0] * self.ys[1] > 0.0:
            print("error wrong interval")
            return False
        return True

    def get_time(self):
        return self.time

    def write_into_file(self, sourceFile):
        self.file1 = open(sourceFile, "w")
        teams_list = ["          xu      ", "       xl      ", "   Xr      ", "   F(Xr)      ",
                      "   F(self.xl)      ", "   Error      "]
        row_format = "{:>10}  " * (len(teams_list) + 1)
        row_format2 = "{:>10.10f}  " * (len(teams_list) + 1)
        self.file1.write(row_format.format("iteration", *teams_list))
        self.file1.write("\n")
        print(row_format.format(0, *teams_list))
        number = 1
        for row in self.table:
            print(row_format2.format(0, *row))
            self.file1.write(row_format2.format(number, *row))
            number = number + 1
            self.file1.write("\n")
        self.file1.close()
        return

    def perform_iteration(self, canvas, step):
        canvas.ax.clear()
        range_x = abs(self.upper) + 2
        x_axis = np.linspace(-1 * range_x, range_x, 100)
        y_axis = [self.H.subs(self.x, a) for a in x_axis]
        canvas.ax.plot([self.xl[step], self.xl[step]], [0, self.H.subs(self.x, self.xl[step])], 'r', x_axis, y_axis,
                       'g',
                       [self.xu[step], self.xu[step]], [0, self.H.subs(self.x, self.xu[step])], 'b',
                       [-1 * range_x, range_x],
                       [0, 0], 'y')
        canvas.ax.figure.canvas.draw()
        text = "\titeration :" + str(step + 1) + "\n\n" + "Xu = " + str(
            self.table[step][0]) + "\n" + "Xl = " + str(
            self.table[step][1]) + "\n" + "Xr = " + str(
            self.table[step][2]) + "\n" + "F(xr) = " + str(
            self.table[step][3]) + "\n" + "F(xl) = " + str(
            self.table[step][4]) + "\n" + " relative error = " + str(self.table[step][5])

        return text

    def method_name(self):
        return "bisection"

    def get_all_errors(self):
        return self.errors

    def get_all_roots(self):
        return self.roots
