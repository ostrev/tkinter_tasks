import math
import tkinter as tk
from tkinter import *
from tkinter import ttk

"""
simple calculator, only for 2 operands and 1 operator in expression, only for correct input
for more complex expressions need to use eval, or RPN
after calculation, if I want to start new calculation must press AC
better to be in one class

"""

class CalculatorLogic:
    def __init__(self):
        self.memory = 0

    def calculate(self, expression):
        if '+' in expression:
            nums = expression.split('+')
            return float(nums[0]) + float(nums[1])
        elif '-' in expression:
            nums = expression.split('-')
            return float(nums[0]) - float(nums[1])
        elif '*' in expression:
            nums = expression.split('*')
            return float(nums[0]) * float(nums[1])
        elif '/' in expression:
            nums = expression.split('/')
            return float(nums[0]) / float(nums[1])
        else:
            return expression



class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Calculator')

        self.logic = CalculatorLogic()

        self.create_buttons()

    def create_buttons(self):
        self.display_entry = ttk.Entry(self.root)
        self.display_entry.grid(row=0, column=0, columnspan=4)

        # first row buttons
        btnMC = ttk.Button(self.root, text='mc', command=self.button_press, width=5)
        btnMC.grid(row=1, column=0)

        btnMR = ttk.Button(self.root, text='mr', command=self.button_press, width=5)
        btnMR.grid(row=1, column=1)

        btnMPlus = ttk.Button(self.root, text='m+', command=self.button_press, width=5)
        btnMPlus.grid(row=1, column=2)

        btnMinus = ttk.Button(self.root, text='m-', command=self.button_press, width=5)
        btnMinus.grid(row=1, column=3)


        # second row buttons
        btnCE = ttk.Button(self.root, text='CE', command=self.button_press, width=5)
        btnCE.grid(row=2, column=0)

        btnAC = ttk.Button(self.root, text='AC', command=self.button_press, width=5)
        btnAC.grid(row=2, column=1)

        btnChangeSign = ttk.Button(self.root, text='+/-', command=self.change_sign, width=5)
        btnChangeSign.grid(row=2, column=2)

        btnSqrt = ttk.Button(self.root, text='sqrt', command=self.button_press, width=5)
        btnSqrt.grid(row=2, column=3)

        # third row buttons
        btnSeven = ttk.Button(self.root, text='7', command=self.button_press, width=5)
        btnSeven.grid(row=3, column=0)

        btnEight = ttk.Button(self.root, text='8', command=self.button_press, width=5)
        btnEight.grid(row=3, column=1)

        btnNine = ttk.Button(self.root, text='9', command=self.button_press, width=5)
        btnNine.grid(row=3, column=2)

        btnDiv = ttk.Button(self.root, text='/', command=self.button_press, width=5)
        btnDiv.grid(row=3, column=3)


        # fourth row buttons
        btnFourth = ttk.Button(self.root, text='4', command=self.button_press, width=5)
        btnFourth.grid(row=4, column=0)

        btnFifth = ttk.Button(self.root, text='5', command=self.button_press, width=5)
        btnFifth.grid(row=4, column=1)

        btnSixth = ttk.Button(self.root, text='6', command=self.button_press, width=5)
        btnSixth.grid(row=4, column=2)

        btnMultiplay = ttk.Button(self.root, text='*', command=self.button_press, width=5)
        btnMultiplay.grid(row=4, column=3)


        # fifth row buttons
        btnFourth = ttk.Button(self.root, text='1', command=self.button_press, width=5)
        btnFourth.grid(row=5, column=0)

        btnFifth = ttk.Button(self.root, text='2', command=self.button_press, width=5)
        btnFifth.grid(row=5, column=1)

        btnSixth = ttk.Button(self.root, text='3', command=self.button_press, width=5)
        btnSixth.grid(row=5, column=2)

        btnMultiplay = ttk.Button(self.root, text='-', command=self.button_press, width=5)
        btnMultiplay.grid(row=5, column=3)

        # sixth row buttons
        btnZero = ttk.Button(self.root, text='0', command=self.button_press, width=5)
        btnZero.grid(row=6, column=0)

        btnDot = ttk.Button(self.root, text='.', command=self.button_press, width=5)
        btnDot.grid(row=6, column=1)

        btnPlus = ttk.Button(self.root, text='+', command=self.button_press, width=5)
        btnPlus.grid(row=6, column=2)

        btnFactorial = ttk.Button(self.root, text='!', command=self.button_press, width=5)
        btnFactorial.grid(row=6, column=3)

        # sixth row buttons
        btnEqual = ttk.Button(self.root, text='=', command=self.button_press, width=15)
        btnEqual.grid(row=7, column=0, columnspan=4, sticky='WE')

    def button_press(self):
        char = str(self.root.focus_get()["text"])

        if char == "=":
            expression = self.display_entry.get()
            result = self.logic.calculate(expression)
            output = self.check_int(result)
            self.change_display_entry(output)
        elif char == "AC":
            self.display_entry.delete(0, tk.END)
        elif char == "CE":
            self.display_entry.delete(len(self.display_entry.get()) - 1, tk.END)
        elif char == "sqrt":
            num = float(self.display_entry.get())
            result = math.sqrt(num)
            output = self.check_int(result)
            self.change_display_entry(output)
        elif char == "!":
            num = int(self.display_entry.get())
            result = math.factorial(num)
            self.change_display_entry(result)
        elif char == "mc":
            self.logic.memory = 0
        elif char == "m+":
            self.logic.memory += float(self.display_entry.get())
        elif char == "m-":
            self.logic.memory -= float(self.display_entry.get())
        elif char == "mr":
            output = self.check_int(self.logic.memory)
            self.change_display_entry(output)
        elif char == "+/-":
            self.change_sign()
        else:
            self.display_entry.insert(tk.END, char)

    def change_sign(self):
        current_value = self.display_entry.get()
        if current_value and current_value != '0':
            if current_value[0] == '-':
                self.display_entry.delete(0)
            else:
                self.display_entry.insert(0, '-')

    def change_display_entry(self, text):
        self.display_entry.delete(0, tk.END)
        self.display_entry.insert(0, str(text))

    def check_int(self, result):
        return str(result).rstrip('.0')


if __name__ == "__main__":
    root = Tk()
    app = CalculatorApp(root)
    for child in root.winfo_children():
        child.grid_configure(padx=10, pady=10)
    root.mainloop()


