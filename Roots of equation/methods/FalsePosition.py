import numpy as np
import sympy as sp
from sympy import sympify
import time

curr_pos = 0


class FalsePosition:
    def __init__(self, func, x1, x2, maxError, maxIteration):
        self.maxnum = maxIteration
        self.maxer = maxError
        self.xlf = x1
        self.xuf = x2
        self.upper = max(x1, x2)
        self.st = func
        self.x = sp.Symbol('x')
        self.e = sp.Symbol('e')
        self.H = sympify(self.st)
        # self.x and y for the function to plot it
        self.x1 = []
        self.y1 = []
        # self.x and y for lower pound
        self.xl = []
        self.fl = []
        self.time = 0
        # self.x and y for upper pound
        self.table = []
        self.xu = []
        self.fu = []
        # different values of xk
        self.xks = []
        # different values of self.ys to determine upper and lower pound for the axis
        self.ys = []
        # store the value of each error
        self.errors = []
        self.roots = []
        # store self.plots which mean the steps of this method
        self.plots = []

    # calculate all requerments of the method
    def calculate(self):
        time_begin = time.time()
        self.ys.append(float("%0.10f" % self.H.subs(self.x, self.xuf).subs(self.e, 2.71828182846)))
        self.ys.append(float("%0.10f" % self.H.subs(self.x, self.xlf).subs(self.e, 2.71828182846)))
        i = 0.0
        err = 1
        maxsize = self.maxnum
        # loop to determine the points to draw the function
        # loop to get the value of xk
        if (self.ys[1] > 0.0 and self.ys[0] < 0.0):
            temp = self.xlf
            self.xlf = self.xuf
            self.xuf = temp
        if (self.ys[0] * self.ys[1] > 0.0):
            print("error wrong interval")
            return False
        for i in range(0, maxsize, 1):
            # store the value of self.xl and self.xu
            self.xl.append(self.xlf)
            self.xu.append(self.xuf)
            # test the error pound
            if (err <= self.maxer):
                break
            # make two points that represent the line from self.xl to self.xu
            x2 = [self.xlf, self.xuf]
            flx = float("%0.10f" % self.H.subs(self.x, self.xlf).subs(self.e, 2.71828182846))
            fux = float("%0.10f" % self.H.subs(self.x, self.xuf).subs(self.e, 2.71828182846))
            y2 = [flx, fux]
            # add this points to the self.plots
            self.plots.append((x2, y2))
            # evaluate the value of xk and store it
            xk = self.xlf * fux - self.xuf * flx
            xk = xk / (fux - flx)
            self.xks.append(xk)
            self.roots.append(xk)
            # if this is the first loop put the error is max =1
            if i == 0:
                self.errors.append(1.0)
            else:
                # get the value of error
                err = abs((self.xks[i] - self.xks[i - 1]))
                self.errors.append(err)
            # get the value of y to store it in self.ys
            f = float("%0.10f" % self.H.subs(self.x, xk).subs(self.e, 2.71828182846))
            self.ys.append(f)
            self.table.append([self.xuf, self.xlf, xk, f, flx, fux, err])
            # replace the value of self.xl or self.xu with the new xk
            if f < 0:
                self.xlf = xk
            else:
                self.xuf = xk
                # function to move between self.plots
        i = min([self.xl[0], self.xu[0]])
        add = (abs((self.xu[0]) - (self.xl[0])) / 100)
        print("min = " + str(i) + " add = " + str(add) + "max = " + str(max([self.xl[0], self.xu[0]])))
        while i <= max([self.xl[0], self.xu[0]]):
            self.x1.append(i)
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

    # return the self.table of the details of each iteration
    def get_table(self):
        return self.table

    # determine if this method is converge or diverge
    def is_converge(self):
        if self.ys[0] * self.ys[1] > 0.0:
            print("error wrong interval")
            return False

    def get_time(self):
        return self.time

    def write_into_file(self, sourceFile):
        file1 = open(sourceFile, "w")
        teams_list = ["        xu      ", "     xl      ", "   Xr      ", "   F(Xr)      ",
                      "   F(self.xl)      ", "   F(self.xu)      ", "   Error      "]
        row_format = "{:>10}  " * (len(teams_list) + 1)
        row_format2 = "{:>10.10f}  " * (len(teams_list) + 1)
        file1.write(row_format.format("iteration", *teams_list))
        file1.write("\n")
        print(row_format.format(0, *teams_list))
        number = 1
        for row in self.table:
            print(row_format2.format(0, *row))
            file1.write(row_format2.format(number, *row))
            number = number + 1
            file1.write("\n")
            file1.close()
        return

    def perform_iteration(self, canvas, step):
        canvas.ax.clear()
        plots2 = [(self.x1, self.y1), (self.x1, self.y1)]
        print(self.xl)
        range_x = abs(self.upper) + 2
        x_axis = np.linspace(-1 * range_x, range_x, 100)
        y_axis = [self.H.subs(self.x, a).subs(self.e, 2.71828182846) for a in x_axis]
        canvas.ax.plot(x_axis, y_axis, label="Function")
        canvas.ax.plot(self.plots[step][0], self.plots[step][1], 'r', self.plots[step][0],
                       self.plots[step][1],
                       'ro', plots2[1][0], plots2[1][1], 'g', [-1 * range_x, range_x], [0, 0], 'y')
        canvas.ax.legend()
        canvas.ax.figure.canvas.draw()
        text = "\titeration :" + str(step + 1) + "\n\n" + "Xu = " + str(
            self.table[step][0]) + "\n" + "Xl = " + str(
            self.table[step][1]) + "\n" + "Xr = " + str(
            self.table[step][2]) + "\n" + "F(xr) = " + str(
            self.table[step][3]) + "\n" + "F(xl) = " + str(
            self.table[step][4]) + "\n" + "F(xu) = " + str(
            self.table[step][5]) + "\n" + " relative error = " + str(self.table[step][6])
        return text

    def method_name(self):
        return "false position"

    def get_all_errors(self):
        return self.errors

    def get_all_roots(self):
        return self.roots
