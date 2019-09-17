import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image
import pandas as pd

class MainGUI:

	def __init__(self):

		self.root = tk.Tk()
		self.root.title("Machine Learning - Model Training")
		self.root.geometry("330x360")
		self.center(self.root, windowWidth=330, windowHeight=360)
		self.df = None
		self.root.filename = ""
		self.dataFrames = []
		self.dataProcessing = -1

		Label(self.root, text = "File:").place(x = 10,y = 100)
		self.filename_Entry = tk.Entry(self.root, width=24)
		self.filename_Entry.bindtags((str(self.filename_Entry), str(self.root), "all"))
		self.filename_Entry.place(x = 60,y = 100)
		self.imgSeach = ImageTk.PhotoImage(Image.open("./Data/search.png").resize((20, 20), Image.BICUBIC))
		Button(self.root, command = self.openFileChooser, image = self.imgSeach).place(x = 290, y = 102)

		self.imgLogo = ImageTk.PhotoImage(Image.open("./Data/logo.jpg").resize((209, 50), Image.BICUBIC))
		self.logo = Label(self.root, image = self.imgLogo).place(x=60,y=10)

		self.console = tk.Text(self.root, height=9, width=43, font=("Monaco", 11), background='black', foreground='white', wrap='none', highlightthickness=0)
		self.console.insert(END, "Welcome to ML - Model Training")
		self.console.bind("<Key>", self.disableWriting)
		self.console.pack(side=BOTTOM, padx=10, pady=10)

		Button(self.root, command=self.processData, text = "Process data from file", width=20).place(x = 70, y = 150)

		self.root.resizable(False, False)
		self.root.mainloop()

	def openFileChooser(self):
		self.root.filename = filedialog.askopenfilename(initialdir = ".",title = "Select file",filetypes = (("CSV files","*.csv"),("Excel files","*.xls *.xlsx")))
		if self.root.filename:
			self.logConsole("Selected file: "+self.root.filename.split("/")[-1])
			self.filename_Entry.delete(0, tk.END)
			self.filename_Entry.insert(0, self.root.filename.split("/")[-2]+"/"+self.root.filename.split("/")[-1])

	def processData(self):
		if self.root.filename.endswith("csv"):
			self.logConsole("Processing "+self.root.filename.split("/")[-1])
			self.df = pd.read_csv(self.root.filename, header=None)
		elif self.root.filename.endswith("xls") or self.root.filename.endswith("xlsx"):
			self.logConsole("Processing "+self.root.filename.split("/")[-1])
			self.df = pd.read_excel(self.root.filename, header=None)
		else:
			self.logConsole("Wrong file format")
			return
		try:
			self.logConsole("Counting and sorting module data")

			if self.df.shape[1]%10 != 0:
				raise Exception("Error de formato")

			self.dataFrames = []
			for module in range(int(self.df.shape[1]/10)):
				actualDF = self.df[[(x+10*module) for x in range(10)]]
				actualDF.columns = ['date','module','packet', 'x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'action']
				self.dataFrames.append(actualDF)

			self.logConsole("Dropping empty rows")
			for x in range(len(self.dataFrames)):
				self.dataFrames[x] = self.dataFrames[x].dropna(axis=0, how='all')
				self.dataFrames[x] = self.dataFrames[x].reset_index(drop=True)
			
			self.logConsole("Modules detected: "+str(len(self.dataFrames)))
			for x in range(len(self.dataFrames)):
				self.logConsole("Rows in module "+str(x+1)+" : "+str(self.dataFrames[x].shape[0]))
			

			d = MyDialog(self.root, self)
			self.root.wait_window(d.top)
			print(self.dataProcessing)


		except Exception as e:
			self.logConsole("Critical ERROR in file structure")
			raise e

	def askMLConfig(self, msg):
		popup = tk.Tk()
		popup.wm_title("!")
		label = tk.Label(popup, text=msg)
		label.pack(side="top", fill="x", pady=10)
		B1 = tk.Button(popup, text="Okay", command = popup.destroy)
		B1.pack()
		popup.mainloop()

	def logConsole(self, text):
		self.console.insert(END, "\n"+text)
		self.console.see(END)

	def disableWriting(self, event):
		return "break"

	def center(self, win, windowWidth, windowHeight):
		positionRight = int(win.winfo_screenwidth()/2 - windowWidth/2)
		positionDown = int(win.winfo_screenheight()/2 - windowHeight/2)
		win.geometry("+{}+{}".format(positionRight, positionDown))

class MyDialog:

	def __init__(self, parent, parentOb):

		top = self.top = Toplevel(parent)
		self.parent = parentOb

		Label(top, text="What kind of data processing should I use?").pack(pady=15)


		self.v = tk.IntVar()
		self.v.set(0)
		options = ["Use all data available", "Use 1 data/sec", "Use a dynamic window of data"]
		for val, option in enumerate(options):
			tk.Radiobutton(top, text=option, indicatoron = 0, width = 20, padx = 20, variable=self.v, value=val, selectcolor='gray25').pack()




		b = Button(top, text="Continue", command=self.ok, width=10)
		b.pack(pady=15, side=BOTTOM)
		top.grab_set_global()

		self.top.geometry("310x195")
		self.center(self.top, windowWidth=310, windowHeight=195)

	def ok(self):

		self.parent.dataProcessing = self.v.get()
		self.top.destroy()

	def center(self, win, windowWidth, windowHeight):
		positionRight = int(win.winfo_screenwidth()/2 - windowWidth/2)
		positionDown = int(win.winfo_screenheight()/2 - windowHeight/2)
		win.geometry("+{}+{}".format(positionRight, positionDown))
		
mainGUI = MainGUI()