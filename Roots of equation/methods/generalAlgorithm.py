import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import matplotlib.pyplot as plt
from sympy import sympify, Symbol

curr_pos = 0
import numpy as np
import os.path
import sys


class General:
    def __init__(self, func, maxError, maxIteration):
        self.x = sp.Symbol('x')
        self.H = sympify(func)
        self.e = sp.symbols('e')
        self.x_neg = 0
        self.x_pos = 0
        self.time = 0
        self.H = self.H.subs(self.e, 2.71828182846)
        self.x_neg_boolean = False
        self.x_pos_boolean = False
        self.xb = 0
        self.xbs = []
        self.xas = []
        self.xrs = []
        self.fb1s = []
        self.fb2s = []
        self.fxrs = []
        self.errors = []
        self.err = 100
        self.num = 0
        self.maxnum = maxIteration
        self.maxerr = maxError
        self.table = []
        # calculate all requerments of the method

    def getPoints(self):
        while (not self.x_neg_boolean or not self.x_pos_boolean):
            ynew = float("%0.10f" % self.H.subs(self.x, self.xb))
            if (ynew < 0):
                self.x_neg = self.xb
                self.x_neg_boolean = True
            elif (ynew > 0):
                self.x_pos = self.xb
                self.x_pos_boolean = True
            self.xb = self.xb + 0.1
            ynew = float("%0.10f" % self.H.subs(self.x, self.xb))
            if (ynew < 0):
                self.x_neg = self.xb
                self.x_neg_boolean = True
            elif (ynew > 0):
                self.x_pos = self.xb
                self.x_pos_boolean = True
            self.xb = self.xb - 0.2
            ynew = float("%0.10f" % self.H.subs(self.x, self.xb))
            if (ynew < 0):
                self.x_neg = self.xb
                self.x_neg_boolean = True
            elif (ynew > 0):
                self.x_pos = self.xb
                self.x_pos_boolean = True
        print(self.x_neg)
        print(self.x_pos)

    def calculate(self):
        self.getPoints()
        self.xbs.append(self.x_pos)
        self.xas.append(self.x_neg)
        while self.num < self.maxnum and self.err > self.maxerr:
            self.xb = self.xbs[-1]
            xa = self.xas[-1]
            xnum = 0
            if (len(self.xbs) == 1):
                xbLast = self.xas[0]
            else:
                xbLast = self.xbs[-2]
            fb1 = float("%0.10f" % self.H.subs(self.x, self.xb))
            self.fb1s.append(fb1)
            fb2 = float("%0.10f" % self.H.subs(self.x, xbLast))
            self.fb1s.append(fb2)
            print("self.xb= " + str(self.xb) + " self.xb-1= " + str(xbLast))
            if (self.xb != xbLast and fb1!=fb2):
                xr1 = ((self.xb - xbLast) / fb1 - fb2) * (fb1)
                xr1 = (self.xb - xr1)
                print("self.xb = " + str(self.xb) + " xbLast = " + str(xbLast) + " xr1= " + str(xr1))
                m = (xa + self.xb) / 2
                print("m = " + str(m))
                if ((xr1 < m and xr1 > self.xb) or (xr1 > m and xr1 < self.xb)):
                    xnum = xr1
                else:
                    xnum = m
            else:
                xnum = ((xa + self.xb) / 2)
            self.xrs.append(xnum)
            fxr = float("%0.10f" % self.H.subs(self.x, xnum))
            self.fxrs.append(fxr)
            print("xr=" + str(xnum))
            print("fxr=" + str(fxr))
            print("fxb=" + str(fb1))
            if (fxr * fb1 < 0):
                self.xas.append(self.xb)
                self.xbs.append(xnum)
            else:
                self.xas.append(xa)
                self.xbs.append(xnum)
            print("self.xb+1 = " + str(self.xbs[-1]) + " xa+1 = " + str(self.xas[-1]))
            self.num = self.num + 1
            if (len(self.xrs) < 2):
                self.errors.append(100)
            else:
                self.err = float("%0.10f" % abs(self.xrs[-1] - self.xrs[-2]))
                self.errors.append(self.err)
                self.table.append([xa, self.xb, xnum, fxr, fb1, fb2, self.errors[-1]])
                print("error = ", self.err)
            print("end1")
                # plot all curves related to all iteration in single figure

    def plot(self, canvas):
        self.perform_iteration(canvas, 0)
        return

    # return error of specific  iteration
    def get_error(self):
        print(self.errors[-1])
        return self.errors[-1]

    # set maximum number of iteration
    def set_max_it(self, max_it):
        self.maxnum = max_it

    # return root of given function after solution
    def get_root(self):
        print(len(self.xrs))
        print(self.xrs[-1])
        return self.xrs[-1]

    # return maximum number of iteration
    def get_max_iteration(self):
        return self.maxnum

    # return total number of iteration taken to implement method
    def get_taken_iteration(self):
        return len(self.xrs)-1

    # return the self.table of the details of each iteration
    def get_table(self):
        return self.table

    # determine if this method is converge or diverge
    def is_converge(self):
        return True

    def get_time(self):
        return self.time

    def write_into_file(self, sourceFile):
        file1 = open(sourceFile, "w")
        teams_list = ["        xa      ", "   xb      ", "   Xr      ", "   F(Xr)      ", "   F(xb1)     ",
                      "   F(xb2)     ", "   Error      "]
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
        return "general"

    def perform_iteration(self, canvas, step):
        canvas.ax.clear()
        print("ksdfalc")
        x_axis = np.linspace(-1 * 5, 5, 100)
        y_axis = [self.H.subs(self.x, a) for a in x_axis]
        canvas.ax.plot(x_axis, y_axis, label="Function")
        canvas.ax.plot([self.xas[step], self.xas[step]], [0, self.H.subs(self.x, self.xas[step])])
        canvas.ax.plot([self.xbs[step], self.xbs[step]], [0, self.H.subs(self.x, self.xbs[step])])
        canvas.ax.plot([-5, 5], [0, 0], label="x_axis")
        canvas.ax.legend()
        canvas.ax.figure.canvas.draw()
        text = "\titeration :" + str(step + 1) + "\n\n" + "Xa = " + str(
            self.table[step][0]) + "\n" + "Xb = " + str(
            self.table[step][1]) + "\n" + "Xr = " + str(
            self.table[step][2]) + "\n" + "F(xr) = " + str(
            self.table[step][3]) + "\n" + "F(xa) = " + str(
            self.table[step][4]) + "\n" + "F(xb) = " + str(
            self.table[step][4]) + "\n" + " relative error = " + str(self.table[step][6])

        return text
