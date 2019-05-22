import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import matplotlib.pyplot as plt
from sympy import sympify, Symbol

curr_pos = 0
import numpy as np
import time


class newton:
    def __init__(self, func, x1, maxError, maxIteration):
        self.st = func
        self.maxnum = maxIteration
        self.maxer = maxError
        self.xi = x1
        self.time = 0
        self.maxnum = self.maxnum + 1
        self.x = sp.Symbol('x')
        self.e = sp.symbols('e')
        self.H = sympify(self.st)
        # self.x and y for the function to plot it
        self.table = []
        self.x1 = []
        self.y1 = []
        # self.x and y for lower pound
        self.xis = []
        # self.x and y for upper pound
        self.fxi = []
        # different values of xk
        self.dfxi = []
        # different values of ys to determine upper and lower pound for the axis
        # store the value of each error
        self.errors = []
        self.roots = []  # store values of roots in each iteration
        # store self.plots which mean the steps of this method
        self.plots = []
        self.maxx = 0
        self.minx = 0
        self.maxy = 0
        self.miny = 0

    # calculate all requerments of the method
    def calculate(self):
        time_begin = time.time()
        self.xis.append(self.xi)
        self.dif = sp.diff(self.st, self.x)
        print(self.dif)
        i = 0.0
        err = 1
        maxsize = self.maxnum
        # loop to determine the points to draw the function
        if self.is_converge() == False:
            return False
        # loop to get the value of xk
        for i in range(0, maxsize, 1):
            # test the error pound
            fxi_value = float("%0.10f" % self.H.subs(self.x, self.xi).subs(self.e, 2.71828182846))
            self.fxi.append(fxi_value)
            dfxi_value = float("%010f" % self.dif.subs(self.x, self.xi).subs(self.e, 2.71828182846))
            self.dfxi.append(dfxi_value)
            x2 = [self.xi]
            xi_last = self.xi
            self.xi = self.xi - (fxi_value / dfxi_value)
            print(self.xi)
            self.roots.append(self.xi)  # edited
            self.xis.append(self.xi)
            x2.append(self.xi)
            y2 = [fxi_value, 0]
            # add this points to the self.plots
            self.plots.append((x2, y2))
            if i == 0:
                self.errors.append(1.0)
            else:
                err = float("%010f" % abs(self.xis[i] - self.xis[i - 1]))
                self.errors.append(err)
            self.table.append([xi_last, self.xi, fxi_value, dfxi_value, err])
            print("lalalala")
            print(err)
            print(self.maxer)
            if (err <= self.maxer):
                break
            i = i + 1
            print("lalalala2")
            self.minx = min(self.xis) - abs(min(self.xis)) * 0.3
            self.maxx = max(self.xis) + abs(max(self.xis)) * 0.3
            extra_ymin = float("%0.10f" % self.H.subs(self.x, self.minx).subs(self.e, 2.71828182846))
            extra_ymax = float("%0.10f" % self.H.subs(self.x, self.maxx).subs(self.e, 2.71828182846))
            self.maxy = max(self.fxi)
            self.miny = min(self.fxi)
            self.maxy = max([self.maxy, extra_ymax]) * 1.3
            self.miny = min([self.miny, extra_ymin])
            if (self.miny < 0.05):
                self.miny = -0.1 * self.maxy
        # function to move between self.plots
        addition = (self.maxx - self.minx) / 100
        i = self.minx
        while i <= self.maxx:
            self.x1.append(i)
            self.y1.append(float("%0.10f" % self.H.subs(self.x, i).subs(self.e, 2.71828182846)))
            i = i + addition
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
        return self.xis[-1]

    # return maximum number of iteration
    def get_max_iteration(self):
        return self.maxnum

    # return total number of iteration taken to implement method
    def get_taken_iteration(self):
        return len(self.xis) - 1

    # return the self.self.table of the details of each iteration
    def get_table(self):
        return self.table

    # determine if this method is converge or diverge
    def is_converge(self):

        dfxi_value = float("%0.10f" % self.H.subs(self.x, self.xis[0]).subs(self.e, 2.71828182846))
        if dfxi_value == 0:
            print("Slope = zero choose another point")
            return False
        ddfxi_value = float("%0.10f" % self.dif.subs(self.x, self.xis[0]).subs(self.e, 2.71828182846))
        if ddfxi_value == 0:
            print("reflection point will diverge")
            return False
        return True

    def write_into_file(self, sourceFile):
        file1 = open(sourceFile, "w")
        teams_list = ["        xi           ", "   xi+1        ", "   F(xi)          ", "   F'(xi)         ",
                      "   Error      "]
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

    def method_name(self):
        return "newton"

    def get_all_errors(self):
        return self.errors

    def get_all_roots(self):
        return self.roots

    def perform_iteration(self, canvas, step):
        canvas.ax.clear()
        plots2 = [(self.x1, self.y1), (self.x1, self.y1)]
        x_axis = np.linspace(-5, 5, 100)
        y_axis = [float("%0.10f" % self.H.subs(self.x, a).subs(self.e, 2.71828182846)) for a in x_axis]
        canvas.ax.plot(x_axis, y_axis, label="Function")
        # the same function to draw the self.plots
        canvas.ax.plot(self.plots[step][0], self.plots[step][1], 'r', self.plots[step][0],
                       self.plots[step][1],
                       'ro', plots2[1][0], plots2[1][1], 'g', [-5, 5], [0, 0], 'y',
                       )
        canvas.ax.legend()
        canvas.ax.figure.canvas.draw()
        text = "\titeration :" + str(step + 1) + "\n\n" + "X " + str(step) + "= " + str(
            self.table[step][0]) + "\n" + "X " + str(step + 1) + "= " + str(
            self.table[step][1]) + "\n" + "F" + "(X" + str(step) + ") = " + str(
            self.table[step][2]) + "\n" + "F'" + "(X" + str(step) + ") = " + str(
            self.table[step][3]) + "\n" + " absolute error = " + str(self.table[step][4])
        return text

    def get_time(self):
        return self.time
