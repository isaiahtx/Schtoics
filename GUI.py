import tkinter as tk
import tkinter.messagebox, tkinter.filedialog, tkinter.font
from tkmacosx import Button
from PIL import Image, ImageTk
from runprogram import mainFunction
import time
import os
# import main

BLUE='#13223a'
YELLOW='#dbb91f'

# Initialization
root = tk.Tk()
root.geometry("900x700")
root.title("Schtoics")
root.minsize(350, 300)

title = tk.Canvas(root, bg=YELLOW, highlightthickness=0)
frame = tk.Frame(root, bg=BLUE)

# Change default font
default_font = tk.font.nametofont("TkDefaultFont")
default_font.configure(size=48, family='Myriad Pro')
# Ensure font change for all widgets
root.option_add("*Font", default_font) 
# List of fonts:
# print(tk.font.families())

filename = ""

def getFile():	
	filename =  tk.filedialog.askopenfilename(title = "Select WebReg file",filetypes = (("jpeg files","*.html"),("all files","*.*")))
	print(filename)
	inputYear = int(getDropdownValue(year))
	inputQuarter = int(getDropdownValue(quarter))

	print("running program with ", inputYear, inputQuarter, filename)
	mainFunction(inputQuarter, inputYear, filename)
	print("finished running oooooohh")
	location = os.getcwd() + "/Calendar.ics"
	tkinter.messagebox.showinfo("Completed", "Successfully wrote .ics file to " + location) # get the location of file output

def getDropdownValue(var):
	value = var.get()
	print("var: ", value)
	return value

# Place Logo and title TODO! Doesnt work!
logo = Image.open('./cal.jpeg') # seems to only work with jpg
tklogo = ImageTk.PhotoImage(logo)
size = logo.size
title.create_image(30, 30, anchor='center', image=tklogo)

text = tk.Text(frame)
text.insert('1.0', 'uh no longer needed')
text.place(relx=0.6, rely=0.2, relheight=0.3, relwidth=0.3)

var = tk.StringVar()
label = tk.Label(title, textvariable=var, bg=YELLOW)
var.set("Schtoics")
label.pack()



# select file button TODO: if windows use tk.Button
button = Button(frame, text="choose file",  padx=10, pady=1, bg=YELLOW, fg=BLUE, borderless=1, highlightthickness=0, activebackground='#fa0', activeforeground='black', command=getFile)
button.place(relx=0.2, rely=0.2, relheight=0.3, relwidth=0.3)



year = tk.StringVar(frame)
quarter = tk.StringVar(frame)

# default value
year.set("2020") 
quarter.set("1") #TODO: get based on the system current date and times. also autogenerate the years options based on date.

dropdownFont = tk.font.Font(family="Myriad Pro", size=20)
yearDropdown = tk.OptionMenu(frame, year, "2020", "2", "3") 
yearDropdown.config(bg = BLUE, width=20, font=dropdownFont)
menu = root.nametowidget(yearDropdown.menuname)
menu.config(font=dropdownFont)
yearDropdown.place(relx=0.6, rely=0.05, relwidth=0.3)
quarterDropdown = tk.OptionMenu(frame, quarter, "1", "2", "3")
quarterDropdown.config(bg = BLUE, font=dropdownFont)
menu = root.nametowidget(quarterDropdown.menuname)
menu.config(font=dropdownFont)
quarterDropdown.place(relx=0.1, rely=0.05, relwidth=0.3)




# final render
title.place(relwidth=1, relheight=0.1)
frame.place(rely=0.1, relwidth=1, relheight=1)


root.mainloop()

