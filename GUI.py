import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image
import pandas as pd
import time
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from Resources.modelTraining import trainModel
from Resources.reportGeneration import report
from Resources.Dialogs import *
import platform
import logging
logging.basicConfig(filename='log.log', format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)
logging.info("Machine Learning - Model Training started")

class MainGUI:

	def __init__(self):

		self.root = tk.Tk()
		self.root.configure(background='white')
		self.root.title("Machine Learning - Model Training")
		self.img_icon = PhotoImage(file='./Resources/icon.png')
		self.root.tk.call('wm', "iconphoto", self.root._w, self.img_icon)
		self.df = None
		self.root.filename = ""
		self.dataFrames = []
		self.dataProcessing = 999
		self.algorithm = 999
		self.configuration = {}
		self.model = None
		self.folder = None
		self.optionsDataProcessing = ["Use all data available", "Use 1 data/sec", "Use a dynamic window of data"]
		self.optionsAlgorithm = ["Random Forest", "Neural Network", "Convolutional Neural Network"]

		self.imgLogo = ImageTk.PhotoImage(Image.open("./Resources/logo.jpg").resize((209, 50), Image.BICUBIC))
		self.logo = Label(self.root, image = self.imgLogo, borderwidth=0).pack(side=TOP, padx=10, pady=(25,10), expand=YES)



		self.frame = Frame(self.root, background='white')
		Label(self.frame, text = "File:  ", background='white', borderwidth=0).pack(side=LEFT)
		self.filename_Entry = tk.Entry(self.frame)
		self.filename_Entry.bindtags((str(self.filename_Entry), str(self.frame), "all"))
		self.filename_Entry.pack(side=LEFT, fill=BOTH, expand=YES)
		self.imgSeach = ImageTk.PhotoImage(Image.open("./Resources/search.png").resize((20, 20), Image.BICUBIC))
		self.imgSearchButton = Button(self.frame, command = self.openFileChooser, image = self.imgSeach)
		self.imgSearchButton.pack(side=LEFT)
		self.frame.pack(fill=BOTH, expand=True, pady=(30,0),padx=(18,25))

		

		self.processButton = Button(self.root, command=self.processData, text = "Process data from file", width=24)
		self.processButton.pack(pady=30, expand=YES)


		self.terminalFont = "Monaco" if platform.system() == "Darwin" else "Monospace"
		self.terminalSize = 11 if platform.system() == "Darwin" else 9
		self.console = tk.Text(self.root, height=9, width=48, font=(self.terminalFont, self.terminalSize), background='black', foreground='white', highlightthickness=0)
		self.console.insert(END, "Welcome to ML - Model Training")
		self.console.bind("<Key>", self.disableWriting)
		self.console.pack(padx=10, pady=10, expand=YES)

		self.root.resizable(False, False)
		self.root.wait_visibility()
		self.root.withdraw()
		center(self.root, windowWidth=self.root.winfo_reqwidth(), windowHeight=self.root.winfo_reqheight())
		self.root.deiconify()
		self.root.mainloop()

	def openFileChooser(self):
		self.root.filename = filedialog.askopenfilename(initialdir = ".",title = "Select file",filetypes = (("CSV files","*.csv"),("Excel files","*.xls *.xlsx")))
		if self.root.filename:
			self.logConsole("Selected file: "+self.root.filename.split("/")[-1])
			self.filename_Entry.delete(0, tk.END)
			self.filename_Entry.insert(0, self.root.filename.split("/")[-2]+"/"+self.root.filename.split("/")[-1])

	def processData(self):
		self.processButton.config(state=DISABLED)
		self.imgSearchButton.config(state=DISABLED)
		self.logConsole("---------------------------")
		if self.root.filename.endswith("csv"):
			self.logConsole("Processing "+self.root.filename.split("/")[-1])
			self.root.update()
			self.df = pd.read_csv(self.root.filename, header=None)
		elif self.root.filename.endswith("xls") or self.root.filename.endswith("xlsx"):
			self.logConsole("Processing "+self.root.filename.split("/")[-1])
			self.root.update()
			self.df = pd.read_excel(self.root.filename, header=None)
		else:
			self.logConsole("Wrong file format", error=True)
			self.processButton.config(state=NORMAL)
			self.imgSearchButton.config(state=NORMAL)
			return
		try:
			self.logConsole("Counting and sorting module data")
			self.root.update()
			if self.df.shape[1]%10 != 0:
				raise Exception("Data format error")

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
				self.logConsole("Rows in module "+str(x+1)+": "+str(self.dataFrames[x].shape[0]))
			

			d_DP = optionDialog(self.root, "What kind of data processing should I use?", self.optionsDataProcessing)
			self.root.wait_window(d_DP.top)
			self.dataProcessing = d_DP.getValue()

			if self.dataProcessing == -1:
				self.logConsole("Processing cancelled")
				self.processButton.config(state=NORMAL)
				self.imgSearchButton.config(state=NORMAL)
				return

			d_ML = optionDialog(self.root, "Select a Machine Learning algorithm", self.optionsAlgorithm)
			self.root.wait_window(d_ML.top)
			self.algorithm = d_ML.getValue()

			if self.algorithm == -1:
				self.logConsole("Processing cancelled")
				self.processButton.config(state=NORMAL)
				self.imgSearchButton.config(state=NORMAL)
				return

			#Configuration windows
			if self.algorithm == 0:
				RF_config = randomForestConfigDialog(self.root, len(self.dataFrames))
				self.root.wait_window(RF_config.top)
				self.configuration = RF_config.getConfiguration()
			elif self.algorithm == 1:
				pass#Neural Network config
				self.configuration = {}
			elif self.algorithm == 2:
				self.logConsole(self.optionsAlgorithm[self.algorithm]+" not implemented", error = True) #Convolutional Neural Network config
				self.configuration = {}
				self.processButton.config(state=NORMAL)
				self.imgSearchButton.config(state=NORMAL)
				return
			else:
				self.configuration = {}
				raise Exception("Internal Error")

			if self.configuration == -1:
				self.logConsole("Processing cancelled")
				self.processButton.config(state=NORMAL)
				self.imgSearchButton.config(state=NORMAL)
				return

			self.logConsole("Data processing: " + self.optionsDataProcessing[self.dataProcessing])
			self.logConsole("Algorithm: " + self.optionsAlgorithm[self.algorithm])

			for key, value in self.configuration.items():
				self.logConsole( key+": "+str(value).strip("[").strip("]") )

			self.logConsole("TRAINING...")
			self.root.update()
			
			self.model = trainModel(self.dataFrames, self.dataProcessing, self.algorithm, self.configuration)
			self.logConsole("Training completed successfully!")

			self.logConsole("Generating plots and model analysis")
			self.root.update()

			self.folder = plotAndAnalysis(self)
			self.logConsole("Plots and analysis generated")
			self.logConsole("Folder: "+self.folder)

			self.processButton.config(state=NORMAL)
			self.imgSearchButton.config(state=NORMAL)


		except Exception as e:
			self.logConsole("Critical ERROR in data", error = True)
			self.processButton.config(state=NORMAL)
			self.imgSearchButton.config(state=NORMAL)
			print("ERROR: ",str(e))

	def logConsole(self, text, error = False):
		self.console.insert(END, "\n"+text)
		self.console.see(END)
		if not error:
			logging.info(text)
		else:
			logging.error(text)

	def disableWriting(self, event):
		return "break"


def plotAndAnalysis(GUI):
	time.sleep(2)
	reportObj = report()
	return "/model"
		
mainGUI = MainGUI()