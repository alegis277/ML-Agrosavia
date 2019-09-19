from tkinter import *
from PIL import ImageTk, Image
import tkinter as tk

def center(win, windowWidth, windowHeight):
		positionRight = int(win.winfo_screenwidth()/2 - windowWidth/2)
		positionDown = int(win.winfo_screenheight()/2 - windowHeight/2)
		win.geometry("+{}+{}".format(positionRight, positionDown))


class optionDialog:

	def __init__(self, parent, text, options):

		top = self.top = Toplevel(parent)
		self.top.title("Select option")
		self.top.resizable(False, False)
		self.img_icon = PhotoImage(file='./Resources/icon.png')
		self.top.tk.call('wm', "iconphoto", self.top._w, self.img_icon)
		self.selectedOk = False

		Label(top, text=text).pack(pady=15, padx=7)

		self.v = tk.IntVar()
		self.v.set(0)
		for val, option in enumerate(options):
			tk.Radiobutton(top, text=option, indicatoron = 0, width = 22, padx = 20, variable=self.v, value=val, selectcolor='gray25').pack()

		b = Button(top, text="Continue", command=self.ok, width=10)
		b.pack(pady=15, side=BOTTOM)

		top.wait_visibility()
		top.withdraw()
		center(self.top, windowWidth=self.top.winfo_reqwidth(), windowHeight=self.top.winfo_reqheight())
		top.deiconify()
		top.grab_set()

	def ok(self):
		self.selectedOk = True
		self.top.destroy()

	def getValue(self):
		if self.selectedOk:
			return self.v.get()
		else:
			return -1

	

class randomForestConfigDialog:

	def __init__(self, parent, nModules):

		top = self.top = Toplevel(parent)
		self.top.title("Random Forest configuration")
		self.top.resizable(False, False)
		self.img_icon = PhotoImage(file='./Resources/icon.png')
		self.top.tk.call('wm', "iconphoto", self.top._w, self.img_icon)
		self.selectedOk = False
		self.hyperparameters = 999
		self.moduleList = []
		self.configuration = {}

		Label(top, text="Random Forest configuration", font=("", 15)).pack(pady=(0,10))

		
		self.fields = ["% Train", "# of Trainings", "Hyperparameter optimization", "N-estimators", "Max features", "Min samples leaf"]
		self.types = ["entry", "entry", "enable", "entry", "entry", "entry"]
		self.entries = {}
		for field, type_f in zip(self.fields, self.types):
			row = Frame(self.top)
			lab = Label(row, width=29, text=field+": ", anchor='w')
			if type_f == "enable":
				self.hyperparameters = IntVar()
				ent = Checkbutton(row, variable=self.hyperparameters, command=self.cb)
			else:
				ent = Entry(row)
				ent.insert(0,"0")
			row.pack(side = TOP, fill = X, padx = 5 , pady = 5)
			lab.pack(side = LEFT)
			ent.pack(side = RIGHT, expand = YES, fill = X)
			self.entries[field] = self.hyperparameters if type_f == "enable" else ent

		Label(self.top, anchor='w', text="Modules to use: ").pack(side = TOP, fill=X, padx = 5 , pady = 5)
		nextRow = True
		for x in range(nModules):
			if nextRow:
				row = Frame(self.top)
				nextRow = False

			var = IntVar(value=1)
			ent = Checkbutton(row, variable=var, text="Module "+str(x+1))
			self.moduleList.append(var)

			if x%2 == 1:
				nextRow = True
				ent.pack(side = RIGHT, expand = YES)
				row.pack(side = TOP, fill = X, padx = 5 , pady = 5)
			else:
				ent.pack(side = LEFT, expand = YES)

		if nextRow == False:
			color = top.cget('bg')
			entAux = Checkbutton(row, text="Module AAA", bg=color, fg=color, indicatoron = 0, borderwidth=0, activebackground=color, activeforeground=color, highlightcolor=color, selectcolor=color)
			entAux.pack(side = RIGHT, expand = YES)
			row.pack(side = TOP, fill = X, padx = 5 , pady = 5)



		b = Button(top, text="Start training", command=self.ok, width=15)
		b.pack(pady=15, side=BOTTOM)

		top.wait_visibility()
		top.withdraw()
		center(self.top, windowWidth=self.top.winfo_reqwidth(), windowHeight=self.top.winfo_reqheight())
		top.deiconify()
		top.grab_set()

	def ok(self):
		self.selectedOk = True

		for field, type_f in zip(self.fields, self.types):
			self.configuration[field] = self.entries[field].get() if type_f == "entry" else self.hyperparameters.get() == 1

		self.configuration["Active Module IDs"] = []
		for index, moduleVar in zip(range(len(self.moduleList)), self.moduleList):
			if moduleVar.get() == 1:
				self.configuration["Active Module IDs"].append(index+1)

		if self.hyperparameters.get() == 1:
			del self.configuration["N-estimators"]
			del self.configuration["Max features"]
			del self.configuration["Min samples leaf"]

		self.top.destroy()

	def cb(self):
		if self.hyperparameters.get() == 1:
			self.entries["N-estimators"].config(state=DISABLED)
			self.entries["Max features"].config(state=DISABLED)
			self.entries["Min samples leaf"].config(state=DISABLED)
		else:
			self.entries["N-estimators"].config(state=NORMAL)
			self.entries["Max features"].config(state=NORMAL)
			self.entries["Min samples leaf"].config(state=NORMAL)

	def getConfiguration(self):
		if self.selectedOk:
			return self.configuration
		else:
			return -1


