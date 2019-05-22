import sympy as sp
import numpy as np
import time


class BirgeVieta:
    def __init__(self, fun, x0, es=0.00001, max_it=50):
        self.function = sp.simplify(fun)
        self.x = sp.symbols('x')
        self.initialX = x0
        self.time = 0
        self.e = sp.symbols('e')
        self.function = self.function.subs(self.e, 2.71828182846)
        self.root = x0
        self.eps = es
        self.max_iteration = max_it
        self.taken_iteration = 0
        self.coefficients = sp.poly(self.function).all_coeffs()
        self.error = 100
        self.errors = []  # hold error of each iteration
        self.roots = []
        self.xValues = [self.initialX]  # hold all values of roots through iterations
        self.B = []  #
        self.C = []  #

    def calculate(self):
        time_begin = time.time()
        size = len(self.coefficients)
        x = self.initialX
        self.xValues.append(x)
        print("Birge entered")
        while self.error > self.eps and self.taken_iteration < self.max_iteration:
            print(self.taken_iteration)
            b = [self.coefficients[0]]
            c = [self.coefficients[0]]
            for i in range(1, size):
                b.append(float("%0.10f" % (self.coefficients[i] + x * b[i - 1])))
                if i != size - 1:
                    c.append(float("%0.10f" % (b[i] + x * c[i - 1])))
            old_x = x
            x = float("%0.10f" % (x - (b[size - 1] / c[size - 2])))
            self.roots.append(x)
            self.error = float("%0.10f" % abs(x - old_x))
            self.errors.append(self.error)
            self.xValues.append(x)
            self.B.append(b)
            self.C.append(c)
            self.taken_iteration += 1
        self.root = x
        self.time = float("%0.10f" % (time.time() - time_begin))

    def plot(self, canvas):
        canvas.ax.clear()
        # plot function
        x_axis = np.linspace(-10, 10, 100)
        y_axis = [self.function.subs(self.x, a) for a in x_axis]
        canvas.ax.plot(x_axis, y_axis, label="Function")
        # plot x-axis
        canvas.ax.plot([-10, 10], [0, 0], 'black', label="x-axis")
        canvas.ax.legend()
        canvas.ax.figure.canvas.draw()

    # return the table of the details of each iteration
    def get_table(self):
        table = [self.coefficients, self.B, self.C, self.xValues, self.errors]
        return table

    # return root of given function after solution
    def get_root(self):
        return float(self.root)

    # set maximum number of iteration
    def set_max_it(self, max_it):
        self.max_iteration = max_it

    # return maximum number of iteration
    def get_max_iteration(self):
        return self.max_iteration

    # return total number of iteration taken to implement method
    def get_taken_iteration(self):
        return self.taken_iteration

    # determine if this method is converge or diverge
    def is_converge(self):
        return self.error > 10 * self.eps

    def get_error(self):
        return self.error

    def perform_iteration(self, canvas, step):
        self.plot(canvas)
        text = " iteration " + str(step + 1) + "\n"
        text += "X" + str(step) + " = " + str(self.xValues[step]) + "\n\n"
        text += "-------------------\n"
        text += "{0:5}{1:5}{2:5}\n".format("a", "b", "c")
        size = len(self.coefficients)
        for i in range(0, size):
            text += "{0:5}{1:5}".format(str(float("%0.3f" % self.coefficients[i])),
                                        str(float("%0.3f" % self.B[step][i])))
            if i < size - 1:
                text += str(float("%0.3f" % self.C[step][i])) + "\n"
            else:
                text += "\n"
        text += "-------------------\n"
        text += "Xr  = " + str(self.xValues[step + 1]) + "\n"
        text += "error = " + str(self.errors[step]) + "\n"
        return text

    def write_into_file(self, sourcefile):
        print("write file !")
        my_file = open(sourcefile, 'w')
        print("file opened")
        for i in range(len(self.errors)):
            my_file.write("iteration " + str(i + 1) + "     x" + str(i) + " = " + str(self.xValues[i]) + "\n")
            my_file.write("{0:21}{1:22}{2:20}\n".format("a", "b", "c"))
            for j in range(len(self.coefficients)):
                my_file.write("{0:20} {1:20}".format(str(self.coefficients[j]), str(self.B[i][j])))
                if j < len(self.coefficients) - 1:
                    my_file.write("{0:20}\n".format(str(self.C[i][j])))
                else:
                    my_file.write("\n")
            my_file.write("xr = " + str(self.xValues[i + 1]) + "\n")
            my_file.write("absolute error = " + str(self.errors[i]) + "\n")
            my_file.write("----------------------------------------\n")
        my_file.close()
        return

    def get_all_errors(self):
        return self.errors

    def get_all_roots(self):
        return self.roots

    def method_name(self):
        return "birge vieta"

    def get_time(self):
        return self.time

# "x^4-9*x^3-2*x^2+120*x-130", -3
