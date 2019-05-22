import sympy as sp
import numpy as np
import time
import math


class FixedPoint:
    def __init__(self, fun, x0, es=0.00001, iter_max=50):
        self.x = sp.symbols('x')
        self.function = sp.simplify(fun)
        self.e = sp.symbols('e')
        self.g = self.function + self.x
        self.initialX = x0
        self.xr = float("%0.10f" % x0)
        self.xr_old = 0
        self.eps = float("%0.10f" % es)  # absolute error
        self.time = 0
        self.max_iteration = iter_max
        self.taken_iteration = 0
        self.table = []  # hold information of each iteration [xr_old,xr,error]
        self.errors = []
        self.roots = []

    # calculate all requirements of the method
    def calculate(self):
        print("G(x) : ", self.g)
        time_begin = time.time()
        error = 100
        iteration = 0
        while error > self.eps and iteration < self.max_iteration:
            self.xr_old = self.xr
            self.xr = float("%0.10f" % self.g.subs(self.x, self.xr_old).subs(self.e, 2.71828182846))
            error = float("%0.10f" % self.get_error())
            self.errors.append(error)
            self.roots.append(self.xr)
            iteration += 1
            info = [self.xr_old, self.xr, error]
            self.table.append(info)

        self.taken_iteration = iteration
        self.time = time.time() - time_begin

    # return error of specific  iteration
    def get_error(self):
        return abs(self.xr - self.xr_old)

    # plot all curves related to all iteration in single figure
    def plot(self, canvas):
        canvas.ax.clear()
        # plot basic function
        range_x = self.initialX + 2
        if range_x < 5:
            range_x = 5
        x_axis = np.linspace(-1 * range_x, range_x, ((2 * range_x) / 10) * 100)
        y_axis = [float("%0.10f" % self.function.subs(self.x, a).subs(self.e, 2.71828182846)) for a in x_axis]
        canvas.ax.plot(x_axis, y_axis, 'r', label="Function")
        print("function ploteed")
        # plot G(x)
        y1_axis = [float("%0.10f" % self.g.subs(self.x, a).subs(self.e, 2.71828182846)) for a in x_axis]
        canvas.ax.plot(x_axis, y1_axis, 'y', label="G(x)")
        print("Gx")
        # plot line y= x
        y1_axis = [self.x.subs(self.x, a) for a in x_axis]
        canvas.ax.plot(x_axis, y1_axis, 'b', label="y = x")
        # plot x-axis
        canvas.ax.plot([-1 * range_x, range_x], [0, 0], 'black', label="x-axis")
        canvas.ax.legend()
        canvas.ax.figure.canvas.draw()

    # determine if this method is converge or diverge
    def is_converge(self):
        return float(
            "%0.10f" % abs(sp.diff(self.g, self.x).subs(self.x, self.initialX).subs(self.e, 2.71828182846))) <= 1

    # return the table of the details of each iteration
    def get_table(self):
        return self.table

    # return maximum number of iteration
    def get_max_iteration(self):
        return self.max_iteration

    # return total number of iteration taken to implement method
    def get_taken_iteration(self):
        return self.taken_iteration

    # return root of given function after solution
    def get_root(self):
        return self.xr

    # set maximum number of iteration
    def set_max_it(self, max_it):
        self.max_iteration = max_it

    def perform_iteration(self, canvas, step):
        self.plot(canvas)
        text = "\titeration :" + str(step + 1) + "\n\n" + "X " + str(step) + " = " + str(
            self.table[step][0]) + "\n\n" + "X " + str(step + 1) + " = " + str(
            self.table[step][1]) + "\n\n" + " relative error = " + str(self.table[step][2])
        return text

    # return time taken to implement method
    def get_time(self):
        return self.time

    def method_name(self):
        return "fixed point"


# write results in file in tabular format
def write_into_file(self, sourcefile):
    print("write file !")
    my_file = open(sourcefile, 'w')
    print("file opened")
    my_file.write('{0:10}  {1:20}  {2:20}   {3:20}\n'.format("iter", "xr_prev", "xr", "absolute error"))
    print("write first")
    for i in range(len(self.table)):
        my_file.write(
            '{0:10}  {1:20}  {2:20}   {3:20}\n'.format(str(i + 1), str(self.table[i][0]), str(self.table[i][1]),
                                                       str(self.table[i][2])))
    my_file.close()


def get_all_errors(self):
    return self.errors


def get_all_roots(self):
    return self.roots
