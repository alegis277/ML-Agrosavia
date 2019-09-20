class report:
	def __init__(self):
		self.datetime = None
		self.platform = None
		self.filename = None
		self.modulesDetected = None
		self.rowsDetected = None
		self.dataProcessing = None
		self.algorithm = None
		self.configuration = None
		self.f = None

	def export(self, directory, file):

		self.f = open(directory+"/"+file,"w+")

		self.writeLine("//////////////////////////////////////////////////////////////////////")
		self.writeLine("///////////// Machine Learning - Model Training - Report /////////////")
		self.writeLine("//////////////////////////////////////////////////////////////////////")
		self.writeLine("File original directory: "+directory+"/"+file)
		self.writeLine("Datetime of generation: "+self.datetime)
		self.writeLine("OS of generation: "+self.platform)
		self.writeLine("File processed: "+self.filename)
		self.writeLine("Modules detected in file: "+str(self.modulesDetected))
		for index, row in zip(range(len(self.rowsDetected)), self.rowsDetected):
			self.writeLine("Rows detected in module "+str(index+1)+": "+str(row))
		self.writeLine("//////////////////////////////////////////////////////////////////////")
		self.writeLine("//////////////////////// DATA ENTERED BY USER ////////////////////////")
		self.writeLine("//////////////////////////////////////////////////////////////////////")
		self.writeLine("Data processing requested was "+self.dataProcessing)
		self.writeLine("Algorithm requested was "+self.algorithm)

		self.writeLine("CONFIGURATION:")
		for key, value in self.configuration.items():
				if key == "Layers":
					for keyL, valueL in value.items():
						self.writeLine( keyL+" -> Neurons: "+str(valueL[0]+"  Activation Function: "+valueL[1]))
				else:
					self.writeLine( key+": "+str(value).strip("[").strip("]") )

		self.writeLine("/////////////////////////// END OF REPORT ////////////////////////////")
		self.f.close()

	def writeLine(self, text):
		self.f.write(text+"\n")