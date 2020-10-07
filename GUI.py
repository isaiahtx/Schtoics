import tkinter as tk
import tkinter.messagebox, tkinter.filedialog
from tkmacosx import Button
import tkinter.font
from PIL import Image, ImageTk
from runprogram import mainFunction
import time
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
	# tkMessageBox.showinfo("hi", "hi")
	filename =  tk.filedialog.askopenfilename(title = "Select WebReg file",filetypes = (("jpeg files","*.html"),("all files","*.*")))
	print (filename)

	print("running program")
	# main()
	mainFunction(1, 2020, filename)
	print("finished running oooooohh")

# Place Logo and title TODO! Doesnt work!
logo = Image.open('./cal.jpeg') # seems to only work with jpg
tklogo = ImageTk.PhotoImage(logo)
size = logo.size
title.create_image(0,0,anchor='nw',image=tklogo)

text = tk.Text(frame)
text.insert('1.0', 'enter the number of quarter')
text.place(relx=0.6, rely=0.2, relheight=0.3, relwidth=0.3)

var = tk.StringVar()
label = tk.Label( title, textvariable=var, bg=YELLOW)
var.set("Schtoics")
label.pack()



# select file button
button = Button(frame, text="choose file",  padx=10, pady=1, bg=YELLOW, fg=BLUE, borderless=1, highlightthickness=0, activebackground='#fa0', activeforeground='black', command=getFile)
button.place(relx=0.2, rely=0.2, relheight=0.3, relwidth=0.3)


# final render
title.place(relwidth=1, relheight=0.1)
frame.place(rely=0.1, relwidth=1, relheight=1)


root.mainloop()

