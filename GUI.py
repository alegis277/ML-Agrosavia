import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image


def center(win, windowWidth, windowHeight):
	positionRight = int(win.winfo_screenwidth()/2 - windowWidth/2)
	positionDown = int(win.winfo_screenheight()/2 - windowHeight/2)
	win.geometry("+{}+{}".format(positionRight, positionDown))


def openFileChooser():
	root.filename = filedialog.askopenfilename(initialdir = ".",title = "Select file",filetypes = (("CSV files","*.csv"),("Excel files","*.xls *.xlsx")))
	if root.filename:
		console.insert(END, "\nSelected file: "+root.filename.split("/")[-1])

if __name__ == '__main__':
	root = tk.Tk()

	root.title("Machine Learning - Model Training")
	root.geometry("330x360")
	center(root, windowWidth=330, windowHeight=360)

	Label(root, text = "File:").place(x = 10,y = 100)
	Entry(root, state='disabled', width=24).place(x = 60,y = 100)
	imgSeach = ImageTk.PhotoImage(Image.open("./Data/search.png").resize((20, 20), Image.ANTIALIAS))
	Button(root, command = openFileChooser, image = imgSeach).place(x = 290, y = 102)

	imgLogo = ImageTk.PhotoImage(Image.open("./Data/logo.jpg").resize((209, 50), Image.ANTIALIAS))
	logo = Label(root, image = imgLogo).place(x=60,y=10)

	console = tk.Text(root, height=9, width=43, font=("Monaco", 11), background='black', foreground='white', wrap='none')
	console.insert(END, "Welcome to ML - Model Training")
	console.bindtags((str(console), str(root), "all"))
	console.pack(side=BOTTOM, padx=10, pady=10)

	Button(root, text = "Process data from file", width=20).place(x = 70, y = 150)

	root.mainloop()