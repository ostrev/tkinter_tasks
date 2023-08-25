from tkinter import *
from tkinter import ttk


def calculate():
    try:
        height_value = float(height.get())
        weight_value = float(weight.get())
        bmi.set(round(weight_value / height_value ** 2, 2))

        bmi_value = float(bmi.get())

        if bmi_value < 20:
            index.set('Underweight')
        elif bmi_value < 25:
            index.set('Normal weight')
        elif bmi_value < 30:
            index.set('Overweight')
        elif bmi_value < 40:
            index.set('Obesity')
        else:
            index.set('Extreme Obesity')

    except ValueError:
        pass


root = Tk()
root.title('Calculator of BMI')

ttk.Label(root, text='Enter your height and weight and press calculate button').grid(row=0, column=0,columnspan=6)
ttk.Label(root, text='').grid(row=1, column=2, sticky='W')
height = ttk.Entry(root, width=5)
height.grid(row=2, column=1, sticky='E')
ttk.Label(root, text='Height').grid(row=2, column=0, sticky='W')
ttk.Label(root, text='m').grid(row=2, column=2, sticky='W')

weight = ttk.Entry(root, width=5)
weight.grid(row=3, column=1, sticky='E')
ttk.Label(root, text='Weight').grid(row=3, column=0, sticky='W')
ttk.Label(root, text='kg').grid(row=3, column=2, sticky='W')

bmi = StringVar()
index = StringVar()

ttk.Button(root, text='Calculate', command=calculate).grid(row=5, column=4, sticky='W')


ttk.Label(root, text='Your BMI is: ').grid(row=4, column=0, sticky='W')
ttk.Label(root, textvariable=bmi).grid(row=4, column=1, sticky='E')

ttk.Label(root, textvariable=index).grid(row=4, column=2, sticky='W')
for child in root.winfo_children():
    child.grid_configure(padx=10, pady=10)

root.bind('<Return>', calculate)
root.mainloop()
