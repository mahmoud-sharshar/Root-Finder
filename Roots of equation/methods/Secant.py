import sympy as sp
import numpy as np
import time


class Secant:
    # solving using secant method
    def __init__(self, fun, x0, x1, e=0.05, max_it=300):
        self.currentX = x1
        self.x = sp.symbols('x')
        self.e = sp.symbols('e')
        self.prevX = x0
        self.function = sp.sympify(fun)
        self.max_iteration = int(max_it)
        self.eps = float(e)
        self.taken_iteration = 0
        self.max_x = max(x0, x1)
        self.table = []
        self.time = 0
        self.points = []  # to represent currentx and prevx in each iteration
        self.errors = []  # hold error in each iteration
        self.roots = []  # STORE ALL VALUES OF ROOT IN EACH ITERATION
        # self.step = 0  # indicate number of current step in method

    # calculate all requirements of the method
    def calculate(self):
        time_begin = time.time()
        error = self.get_error()
        iteration = 0
        while abs(error) > self.eps and iteration < self.max_iteration:
            self.points.append([self.currentX, self.prevX])
            arr = [self.prevX, self.currentX]
            fun_prev = float(
                "%0.10f" % self.function.subs(self.x, self.prevX).subs(self.e, 2.71828182846))
            fun_curr = float(
                "%0.10f" % self.function.subs(self.x, self.currentX).subs(self.e, 2.71828182846))
            next_x = float(
                "%0.10f" % (self.currentX - ((fun_curr * (self.prevX - self.currentX))
                                             / (fun_prev - fun_curr))))

            if self.max_x < next_x:
                self.max_x = next_x
            arr.append(next_x)
            self.roots.append(next_x)
            self.prevX = self.currentX
            self.currentX = next_x
            error = self.get_error()
            arr.append(fun_prev)
            arr.append(fun_curr)
            arr.append(error)
            self.table.append(arr)
            self.errors.append(error)
            iteration += 1

            self.points.append([self.currentX, self.prevX])
            self.taken_iteration = iteration
            self.time = float("%0.10f" % (time.time() - time_begin))

            # plot all curves related to all iteration in single figure

    def plot(self, canvas):
        canvas.ax.clear()
        range_x = self.max_x + 2
        x_axis = np.linspace(-1 * range_x, range_x, ((2 * range_x) / 10) * 100)
        y_axis = [self.function.subs(self.x, a).subs(self.e, 2.71828182846) for a in x_axis]
        canvas.ax.plot(x_axis, y_axis, 'r', label="Function")
        i = 0
        canvas.ax.plot([-1 * range_x, range_x], [0, 0], 'black', label="x-axis")
        while i < len(self.table):
            y = [self.function.subs(self.x, self.table[i][0]).subs(self.e, 2.71828182846),
                 self.function.subs(self.x, self.table[i][1]).subs(self.e, 2.71828182846), 0]
            y1 = self.function.subs(self.x, self.table[i][2]).subs(self.e, 2.71828182846)
            canvas.ax.plot([self.table[i][0], self.table[i][1], self.table[i][2]], y, label="iteration" + str(i + 1))
            canvas.ax.plot([self.table[i][2], self.table[i][2]], [0, y1], 'b')
            # canvas.ax.plot([self.points[i][0], self.points[i][0]], [0, y[0]], 'b')
            # canvas.ax.plot([self.points[i][1], self.points[i][1]], [0, y[1]], 'b')
            i += 1

        canvas.ax.legend()
        canvas.ax.figure.canvas.draw()

    # return error of specific  iteration
    def get_error(self):
        return float("%0.10f" % (self.currentX - self.prevX))

    # return root of given function after solution
    def get_root(self):
        return self.currentX

    # return maximum number of iteration
    def get_max_iteration(self):
        return self.max_iteration

    # return total number of iteration taken to implement method
    def get_taken_iteration(self):
        return self.taken_iteration

    # return the table of the details of each iteration
    def get_table(self):
        return self.table

    def is_converge(self):
        return self.get_error() <= self.eps

    def perform_iteration(self, canvas, step):
        canvas.ax.clear()
        range_x = self.max_x + 2
        x_axis = np.linspace(-1 * range_x, range_x, ((2 * range_x) / 10) * 100)
        y_axis = [self.function.subs(self.x, a).subs(self.e, 2.71828182846) for a in x_axis]
        canvas.ax.plot(x_axis, y_axis, 'r', label="Function")
        # plot line between two points corresponding to this iteration
        y = [self.function.subs(self.x, self.table[step][0]).subs(self.e, 2.71828182846),
             self.function.subs(self.x, self.table[step][1]).subs(self.e, 2.71828182846), 0]
        y1 = self.function.subs(self.x, self.table[step][2]).subs(self.e, 2.71828182846)
        canvas.ax.plot([self.table[step][0], self.table[step][1], self.table[step][2]], y,
                       label="iteration" + str(step + 1))
        canvas.ax.plot([self.table[step][2], self.table[step][2]], [0, y1], 'b')
        # plot boundries of line of two points
        # canvas.ax.plot([self.points[step][0], self.points[step][0]], [0, y[0]], 'b')
        # canvas.ax.plot([self.points[step][1], self.points[step][1]], [0, y[1]], 'b')
        # plot x-axis in the middle of figure
        canvas.ax.plot([-5, 5], [0, 0], 'black', label="x-axis")
        canvas.ax.legend()
        canvas.ax.figure.canvas.draw()
        text = "    iteration " + str(step + 1) + "\n\n" + "X(i-1) : " + str(
            self.table[step][0]) + "\n" + "X(i) : " + str(
            self.table[step][1]) + "\n" + "X(i+1) : " + str(
            self.table[step][2]) + "\n" + "F( x(i-1) )  : " + str(
            self.table[step][3]) + "\n" + "F( x(i) )  : " + str(
            self.table[step][4]) + "\n" "Error : " + str(self.errors[step])
        return text

    def get_time(self):
        return self.time

    def method_name(self):
        return "secant"

    def write_into_file(self, sourcefile):
        print("write file !")
        my_file = open(sourcefile, 'w')
        print("file opened")
        my_file.write(
            '{0:10}  {1:20}  {2:20}   {3:20}{4:20}\n'.format("iter", "x(i-1)", "x(i)", "x(i+1)", "absolute error"))
        print("write first")
        for i in range(len(self.table)):
            my_file.write(
                '{0:10}  {1:20}  {2:20}   {3:20}{4:20}\n'.format(str(i + 1), str(self.table[i][0]),
                                                                 str(self.table[i][1]),
                                                                 str(self.table[i][2]), str(self.table[i][3])))
        my_file.close()

    def get_all_errors(self):
        return self.errors

    def get_all_roots(self):
        return self.roots


if __name__ == "__main__":
    s = Secant("x^2-2", 0.5, 1)
    s.calculate()
