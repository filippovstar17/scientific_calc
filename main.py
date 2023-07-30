from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from functools import partial
from tkinter import Tk
from math import log, sin, cos, tan, factorial, sqrt
import math
import sys


class Window(QMainWindow):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.setWindowTitle('Научный калькулятор')
        self.setFixedSize(500, 265)  # Фиксированные размеры окна
        self.setWindowIcon(QIcon('icons/sci_calc.png'))  # Установка иконки приложения

        # Глобальный элемент управления
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)
        # Глобальный макет
        global_vbox = QVBoxLayout(main_widget)
        vbox = QVBoxLayout()
        grid = QGridLayout()

        # Добавление элементов управления для локального макета
        self.main_text = QLabel(self)
        self.main_text.setText("0")
        self.main_text.setMargin(10)  # Отступы 10 пикселей
        self.main_text.setStyleSheet("QLabel{\
                                font-size: 15pt;\
                                font-weight: bold;\
                                background-color: rgb(169,166,170);\
                                color: rgb(255,255,255);}")  # Стили css
        self.main_text.setGeometry(0, 0, 300, 50)  # Ширина и высота текста
        vbox.addWidget(self.main_text, alignment=Qt.AlignVCenter)

        names = ['MC', 'MR', 'MS', 'M+', 'M-', '←',
                 '1/x', 'log', 'ln', 'Exp', 'mod', 'C',
                 'sin', 'cos', 'tan', 'cot', 'n!', 'sqrt',
                 'pi', '7', '8', '9', '/', 'x^2',
                 'e', '4', '5', '6', '*', 'x^3',
                 '(', '1', '2', '3', '-', 'x^y',
                 ')', '+-', '0', '.', '+', '=']

        positions = [(i, j) for i in range(7) for j in range(6)]

        for position, name in zip(positions, names):
            if name == '':
                continue
            button = QPushButton(name)
            grid.addWidget(button, *position)
            button.clicked.connect(partial(self.on_clicked, name))

        # Добавляем локальный макет в макет global_vbox
        global_vbox.addLayout(vbox)
        global_vbox.addLayout(grid)

        # Память калькулятора
        self.memory = "0"

        # Показываем окно приложения
        self.show()

    def on_clicked(self, name):
        try:
            text = self.main_text.text()
            possible_functions = "pie-+*/()"
            if str(name).isdigit() or name in possible_functions:  # если ввели число или знаки
                if name == "pi":
                    name = str(math.pi)
                if name == "e":
                    name = str(math.e)
                if text == "0" and name not in possible_functions:  # если изначально был 0
                    self.main_text.setText("" + name)
                elif text[-1] in possible_functions[:-1] and name in possible_functions[:-2]:  # замена знаков и скобок
                    self.main_text.setText(text[:-1] + name)
                else:  # проверка для того, чтобы нельзя было ввести константу несколько раз подряд
                    if (name == str(math.pi) or name == str(math.e)) and text[-1] not in possible_functions:
                        tk = Tk()
                        tk.bell()
                    else:
                        self.main_text.setText(text + name)
            elif name == "MC":
                self.memory = "0"
            elif name == "MR":
                if text == "0":
                    self.main_text.setText(self.memory)
                elif text[-1] in possible_functions[:-1]:
                    self.main_text.setText(text + self.memory)
                else:
                    self.main_text.setText(self.memory)
            elif name == "MS":
                self.memory = self.main_text.text()
            elif name == "M+":
                self.memory = str(round(eval(self.memory)+eval(self.main_text.text()), 12))
            elif name == "M-":
                self.memory = str(round(eval(self.memory)-eval(self.main_text.text()), 12))
            elif name == "1/x":
                self.main_text.setText(str(round(1 / eval(text), 12)))
            elif name == "log":
                res = eval(text)
                if res <= 0:
                    msg = QMessageBox()
                    msg.setWindowTitle("Ошибка")
                    msg.setText("Введите положительное число!")
                    msg.setIcon(QMessageBox.Critical)
                    msg.exec_()
                else:
                    self.main_text.setText(str(round(log(res, 10), 12)))
            elif name == "ln":
                res = eval(text)
                if res <= 0:
                    msg = QMessageBox()
                    msg.setWindowTitle("Ошибка")
                    msg.setText("Введите положительное число!")
                    msg.setIcon(QMessageBox.Critical)
                    msg.exec_()
                else:
                    self.main_text.setText(str(round(log(res), 12)))
            elif name == "Exp":
                res = str(eval(text))
                self.main_text.setText(res + "e+")
            elif name == "mod":
                res = str(eval(text))
                self.main_text.setText(res + "mod")
            elif name == "x^2":
                self.main_text.setText(str(round(eval(text) ** 2, 12)))
            elif name == "x^3":
                self.main_text.setText(str(round(eval(text) ** 3, 12)))
            elif name == "x^y":
                res = str(eval(text))
                self.main_text.setText(res + "^")
            elif name == "sin":
                self.main_text.setText(str(round(sin(eval(text)), 12)))
            elif name == "cos":
                self.main_text.setText(str(round(cos(eval(text)), 12)))
            elif name == "tan":
                self.main_text.setText(str(round(tan(eval(text)), 12)))
            elif name == "cot":
                self.main_text.setText(str(round(1 / tan(eval(text)), 12)))
            elif name == "n!":
                self.main_text.setText(str(round(factorial(eval(text)), 12)))
            elif name == "sqrt":
                self.main_text.setText(str(round(sqrt(eval(text)), 12)))
            elif name == ".":
                a = text.rfind("+")
                b = text.rfind("-")
                c = text.rfind("*")
                d = text.rfind("/")
                e = text.rfind("%")
                f = text.rfind("^")
                m = max(a, b, c, d, e, f)
                if text.rfind(".") != -1 and m == -1 or text.rfind(".") > m or text[-1] in ".-+*/()%^":
                    tk = Tk()
                    tk.bell()
                else:
                    self.main_text.setText(text + name)
            elif name == "+-":
                a = text.rfind("+")
                b = text.rfind("-")
                c = text.rfind("*")
                d = text.rfind("/")
                e = text.rfind("%")
                m = max(a, b, c, d, e)
                if m == -1 or m == 0:
                    if text[1:].isdigit() or text[1:] == "":
                        self.main_text.setText(str(int(text) * -1))
                    else:
                        self.main_text.setText(str(float(text) * -1))
                else:
                    new_text1 = text[:m + 1]
                    new_text2 = text[m:]
                    if new_text2[1:].isdigit():
                        new_text2 = str(int(new_text2) * -1)
                    else:
                        new_text2 = str(float(new_text2) * -1)
                    if new_text1.endswith("+-"):
                        self.main_text.setText(new_text1[:-1] + new_text2)
                    else:
                        self.main_text.setText(new_text1[:-1] + "+" + new_text2)
            elif name == "←":
                if len(text) == 1:
                    self.main_text.setText("0")
                else:
                    self.main_text.setText(text[:-1])
            elif name == "C":
                self.main_text.setText("0")
            elif name == "=":
                if text.find("mod") != -1:
                    text = text.replace("mod", "%")
                if text.find("^") != -1:
                    text = text.replace("^", "**")
                self.main_text.setText(str(round(eval(text), 12)))  # Считаем и округляем до 12 значащих цифр
            else:
                tk = Tk()
                tk.bell()
        except ZeroDivisionError:
            msg = QMessageBox()
            msg.setWindowTitle("Ошибка")
            msg.setText("На ноль делить нельзя!")
            msg.setIcon(QMessageBox.Critical)
            msg.exec_()
        except Exception:
            msg = QMessageBox()
            msg.setWindowTitle("Ошибка")
            msg.setText("Неизвестная ошибка!")
            msg.setIcon(QMessageBox.Critical)
            msg.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Window()
    sys.exit(app.exec_())
