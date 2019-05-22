from PyQt5 import QtWidgets, QtCore
from view import Ui_MainWindow
from methods.FalsePosition import FalsePosition
from methods.fixed_point import FixedPoint
from methods.birge_vieta import BirgeVieta
from methods.Secant import Secant
from methods.Bisection import Bisection
from methods.Newton import newton
from methods.generalAlgorithm import General
from solution_table import SolutionTable
import sys


# main window of application
class MainApp(QtWidgets.QMainWindow):
    # constructor
    def __init__(self):
        super(MainApp, self).__init__()
        self.ui = Ui_MainWindow()
        self.method = None
        self.methodNum = 0
        self.mode = False
        self.step = 0
        self.all_method_order = 0  # hold which method to be selected
        self.all_method = []  # hold objects of all methods in case of this mode
        self.ui.setupUi(self)
        self.eps = 0.00001
        self.max_iter = 50
        self.x0 = 0
        self.x1 = 0
        self.function = ""
        self.setWindowTitle("Root Finder")
        self.ui.modeCombo.activated.connect(self.mode_changed)
        self.ui.methodCombo.activated.connect(self.method_changed)
        self.ui.solveBtn.clicked.connect(self.solve_btn_action)
        self.ui.prevBtn.clicked.connect(self.prev_btn_action)
        self.ui.nextBtn.clicked.connect(self.next_btn_action)
        self.ui.tableButton.clicked.connect(self.show_table)
        self.ui.fileSaveBtn.clicked.connect(self.save_into_file)
        self.ui.fileReadBtn.clicked.connect(self.read_file)
        self.table = SolutionTable()

    # handle the event of selection specific mode of solution(single mode , Direct Solution)
    def mode_changed(self):
        self.mode = bool(self.ui.modeCombo.currentIndex())
        # print(self.mode)
        if not self.mode:
            self.ui.nextBtn.setEnabled(False)
            self.ui.prevBtn.setEnabled(False)

    # handle the event of selection specific method
    def method_changed(self):
        self.ui.fileSaveBtn.setEnabled(False)
        self.ui.tableButton.setEnabled(False)
        self.methodNum = self.ui.methodCombo.currentIndex()
        self.ui.solveBtn.setText("Solve")
        self.ui.X0lineEdit.setEnabled(True)
        self.ui.labelX0.setText("X0")
        if self.methodNum == 0:
            self.ui.solveBtn.setEnabled(False)
            self.ui.method_name_label.setText("Select Method to solve")
            return
        elif self.methodNum == 3 or self.methodNum == 4 or self.methodNum == 6:
            self.ui.X1lineEdit.setEnabled(False)
            self.ui.labelX1.setText("  ")
            self.ui.solveBtn.setEnabled(True)
        elif self.methodNum == 7:
            self.ui.X1lineEdit.setEnabled(False)
            self.ui.labelX1.setText("  ")
            self.ui.X0lineEdit.setEnabled(False)
            self.ui.labelX0.setText("  ")
            self.ui.solveBtn.setEnabled(True)
        elif self.methodNum == 8:
            self.ui.solveBtn.setText("Next method")
            self.all_method_order = 1
            self.ui.X1lineEdit.setEnabled(True)
            self.ui.labelX1.setText("X1")
            self.ui.method_name_label.setText("Bisection method")
            self.ui.solveBtn.setEnabled(True)
            return
        else:
            self.ui.X1lineEdit.setEnabled(True)
            self.ui.labelX1.setText("X(1)")
            self.ui.solveBtn.setEnabled(True)
        self.ui.mplGraph.n2.setVisible(False)
        self.ui.mplGraph.canvas2.setVisible(False)
        self.ui.method_name_label.setText("")
        self.all_method_order = 0

    def take_method_input(self):
        if self.all_method_order == 1:  # bisection
            self.all_method_order += 1
            self.ui.method_name_label.setText("False position method")
            self.all_method.append(Bisection(self.function, self.x0, self.x1, self.eps, self.max_iter))
        elif self.all_method_order == 2:  # false position
            self.all_method_order += 1
            self.ui.method_name_label.setText("Fixed Point method")
            self.all_method.append(FalsePosition(self.function, self.x0, self.x1, self.eps, self.max_iter))
            self.ui.X1lineEdit.setEnabled(False)
            self.ui.labelX1.setText("  ")
        elif self.all_method_order == 3:  # Fixed Point
            self.all_method_order += 1
            self.ui.method_name_label.setText("Newton method")
            self.all_method.append(FixedPoint(self.function, self.x0, self.eps, self.max_iter))
            self.ui.X1lineEdit.setEnabled(False)
            self.ui.labelX1.setText("  ")
        elif self.all_method_order == 4:  # Newton
            self.all_method_order += 1
            self.ui.method_name_label.setText("Secant method")
            self.all_method.append(newton(self.function, self.x0, self.eps, self.max_iter))
            self.ui.X1lineEdit.setEnabled(True)
            self.ui.labelX1.setText("X1")
        elif self.all_method_order == 5:  # Secant
            self.all_method_order += 1
            self.ui.method_name_label.setText("Birge Vieta method")
            self.ui.solveBtn.setText("Solve")
            self.all_method.append(Secant(self.function, self.x0, self.x1, self.eps, self.max_iter))
            self.ui.X1lineEdit.setEnabled(False)
            self.ui.labelX1.setText("  ")
        elif self.all_method_order == 6:  # Birge VIeta
            self.all_method_order += 1
            self.all_method.append(BirgeVieta(self.function, self.x0, self.eps, self.max_iter))
        self.ui.X0lineEdit.setText("")
        self.ui.X1lineEdit.setText("")

    def excute_all_method(self):
        self.ui.mplGraph.canvas2.ax.clear()
        self.ui.mplGraph.canvas.ax.clear()
        print("enterd")
        print(len(self.all_method))
        self.ui.mplGraph.n2.setVisible(True)
        self.ui.mplGraph.canvas2.setVisible(True)
        for i in range(len(self.all_method)):
            if i == 2 and not self.all_method[i].is_converge():
                continue
            print("before calculate")
            self.all_method[i].calculate()
            print("calculte :" + self.all_method[i].method_name())
            x_axis = [c for c in range(1, self.all_method[i].get_taken_iteration() + 1)]
            print(self.all_method[i].get_taken_iteration())
            print(len(self.all_method[i].get_all_roots()))
            print(self.all_method[i].method_name())
            self.ui.mplGraph.canvas.ax.plot(x_axis, self.all_method[i].get_all_roots(),
                                            label=self.all_method[i].method_name())
            self.ui.mplGraph.canvas2.ax.plot(x_axis, self.all_method[i].get_all_errors(),
                                             label=self.all_method[i].method_name())
            print("ploted :" + self.all_method[i].method_name())
        print("exit")
        self.ui.mplGraph.canvas2.ax.legend()
        self.ui.mplGraph.canvas2.ax.figure.canvas.draw()
        self.ui.mplGraph.canvas.ax.legend()
        self.ui.mplGraph.canvas.ax.figure.canvas.draw()

        return

    def validate_input(self, method_num):
        self.function = self.ui.functionLineEdit.text()
        flagx1 = True
        if self.function == "":
            return False
        # take value of initial point if exist
        print("function : ", self.function)
        flag_x0 = True
        try:
            self.x0 = float(self.ui.X0lineEdit.text())
            # print(x0)
        except:
            flag_x0 = False

        if not flag_x0 and method_num != 7:
            return
        print("x0 : ", self.x0)
        # take value of second point if exict
        try:
            self.x1 = float(self.ui.X1lineEdit.text())
            # print(x1)
        except:
            flagx1 = False
        if (method_num == 1 or method_num == 2 or method_num == 5) and not flagx1:
            print(self.methodNum)
            return False
        print("x1 : ", self.x1)
        # take value of eps
        try:
            self.eps = float(self.ui.EpslineEdit.text())
        except:
            self.eps = 0.00001
        # take value of max iteration
        try:
            self.max_iter = float(self.ui.iterlineEdit.text())
        except:
            self.max_iter = 50

        print("eps : ", self.eps)
        return True

    # handle the event of solve button
    def solve_btn_action(self):
        if self.all_method_order == 6:
            print("valid :", self.all_method_order)
            if not self.validate_input(self.all_method_order):
                return
            self.take_method_input()
            self.excute_all_method()
            return
        elif self.all_method_order > 0:
            if not self.validate_input(self.all_method_order):
                return
            print("valid :", self.all_method_order)
            self.take_method_input()
            return
        if not self.validate_input(self.methodNum):
            return

        self.ui.mplGraph.n2.setVisible(False)
        self.ui.mplGraph.canvas2.setVisible(False)
        if self.methodNum == 1:  # Bisection
            self.method = Bisection(self.function, self.x0, self.x1, self.eps, self.max_iter)
            flag = self.method.calculate()
            if not flag:
                self.ui.solutionText.setText(
                    "Bisection method fails \ninterval is invalid \n select interval that contains odd number of roots")
                return
            print("bisection")
        elif self.methodNum == 2:  # False Position
            self.method = FalsePosition(self.function, self.x0, self.x1, self.eps, self.max_iter)
            flag = self.method.calculate()
            if not flag:
                self.ui.solutionText.setText(
                    "False Position method fails \ninterval is invalid \n select interval that contains odd number of roots")
                return
            print("FalsePosition")
        elif self.methodNum == 3:
            self.method = FixedPoint(self.function, self.x0, self.eps, self.max_iter)
            if not self.method.is_converge():
                self.method.plot(self.ui.mplGraph.canvas)
                self.ui.solutionText.setText(
                    "\n\n  Fixed Point iteration wiil diverge for this function under this initial point " +
                    "\n, you can try another point or another method")
                return
            self.method.calculate()
        elif self.methodNum == 4:
            self.method = newton(self.function, self.x0, self.eps, self.max_iter)
            flag = self.method.calculate()
            if not flag:
                self.ui.solutionText.setText(
                    "Newton method fails \n\n method will converge for this function and this initial point")
                return
            print("Newton")
        elif self.methodNum == 5:
            self.method = Secant(self.function, self.x0, self.x1, self.eps, self.max_iter)
            self.method.calculate()
        elif self.methodNum == 6:
            self.method = BirgeVieta(self.function, self.x0, self.eps, self.max_iter)
            self.method.calculate()
        elif self.methodNum == 7:
            self.method = General(self.function, self.eps, self.max_iter)
            self.method.calculate()

        print("calculated", self.method.get_taken_iteration())
        self.ui.tableButton.setEnabled(True)
        self.ui.fileSaveBtn.setEnabled(True)
        if self.mode:
            self.single_mode()
        else:
            self.direct_solution_mode()

    # actions performed in case of direct solution display
    def direct_solution_mode(self):
        print("before plotted")
        self.method.plot(self.ui.mplGraph.canvas)
        print("plotted")
        text = "\tSolution\n\n" + " estimate Root = " + str(self.method.get_root()) + "\n\n" + " absolute Error = "
        text += str(self.method.get_error()) + "\n\n" + " # Iterations = " + str(
            self.method.get_taken_iteration()) + "\n\n" + "Time : " + str(self.method.get_time()) + "\n"
        self.ui.solutionText.setText(text)

    # actions performed in case of direct solution display
    def single_mode(self):
        self.ui.nextBtn.setEnabled(True)
        self.one_iteration()
        self.step += 1
        self.ui.prevBtn.setEnabled(True)

    # handle the event of next button
    def next_btn_action(self):
        self.one_iteration()
        # print("iteration : " + self.method.get_taken_iteration())
        self.step += 1
        if self.step >= self.method.get_taken_iteration():
            self.ui.nextBtn.setEnabled(False)
        else:
            self.ui.prevBtn.setEnabled(True)

    # handle the event of prev button
    def prev_btn_action(self):
        self.step -= 1
        self.one_iteration()
        if self.step == 0:
            self.ui.prevBtn.setEnabled(False)
        else:
            self.ui.nextBtn.setEnabled(True)

    def one_iteration(self):
        text = self.method.perform_iteration(self.ui.mplGraph.canvas, self.step)
        self.ui.solutionText.setText(text)

    def show_table(self):
        self.table.fill_table(self.method)
        self.table.show()

    # enable saving results into file
    def save_into_file(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'QFileDialog.getSaveFileName()', '/home',
                                                         "text Files (*.txt)", options=options)
        print(filename)
        if filename[0]:
            print(filename[0])
            self.method.write_into_file(filename[0])

    # handle read input from file
    def read_file(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'QFileDialog.getOpenFileName', '/home',
                                                         "text Files (*.txt)", options=options)
        print(filename)
        if filename[0]:
            print(filename[0])
            f = open(filename[0], 'r')
            print(f)
            # first line --->equation
            self.ui.functionLineEdit.setText(f.readline())
            # ----------------------------------
            # second line ---> method name
            method_name = f.readline().lower().capitalize()
            print(method_name)
            index = self.ui.modeCombo.findText(method_name, QtCore.Qt.MatchFixedString)
            print(index)
            if index > 0:
                self.ui.modeCombo.setCurrentIndex(index)
                self.method_changed()
            else:
                self.ui.modeCombo.setCurrentIndex(0)
                self.method_changed()
            # ----------------------------------
            # third line ---> parameters
            par = f.readline().split(" ")
            if len(par) == 2:
                self.ui.X0lineEdit.setText(par[0])
                self.ui.X1lineEdit.setText(par[1])
            elif len(par) == 1:
                self.ui.X0lineEdit.setText(par[0])
            # ---------------------------------
            # forth line ---> eps or max iteration
            num = f.readline()
            try:
                number = int(num)
                self.ui.iterlineEdit.setText(num)
            except:
                self.ui.EpslineEdit.setText(num)
            f.close()


def main():
    app = QtWidgets.QApplication([])
    application = MainApp()
    application.show()
    sys.exit(app.exec())


# x^3-0.165*x^2+3.993*10^-4


if __name__ == '__main__':
    main()
