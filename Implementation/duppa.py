from tkinter import *

# Create an instance of tkinter window
win = Tk()
win.geometry("700x350")

# Define a function
def sel():
   selection= "Current Value is: " + str(var.get())
   label.config(text=selection)

# Create a scale widget
var=StringVar()
my_scale=Scale(win, variable=var, orient=HORIZONTAL,cursor="dot")
my_scale.pack(anchor = CENTER)

# Create a label widget
label=Label(win, font='Helvetica 15 bold')
label.pack()

# Create a button to get the value at the scale
button=Button(win, text="Get Value", command=sel)
button.pack()

win.mainloop()