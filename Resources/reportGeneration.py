import numpy as np
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
		self.dataResults = None

	def export(self, directory, file):

		self.f = open(directory+"/"+file,"w+")
		self.writeLine("//////////////////////////////////////////////////////////////////////////////////////////")
		self.writeLine("//////////////////////////////////////////////////////////////////////////////////////////")
		self.writeLine("///////////// Machine Learning - Model Training - Report /////////////////////////////////")
		self.writeLine("//////////////////////////////////////////////////////////////////////////////////////////")
		self.writeLine("File original directory: "+directory+"/"+file)
		self.writeLine("Datetime of generation: "+self.datetime)
		self.writeLine("OS of generation: "+self.platform)
		self.writeLine("File processed: "+self.filename)
		self.writeLine("Modules detected in file: "+str(self.modulesDetected))
		for index, row in zip(range(len(self.rowsDetected)), self.rowsDetected):
			self.writeLine("Rows detected in module "+str(index+1)+": "+str(row))
		self.writeLine("//////////////////////////////////////////////////////////////////////////////////////////")
		self.writeLine("//////////////////////// DATA ENTERED BY USER ////////////////////////////////////////////")
		self.writeLine("//////////////////////////////////////////////////////////////////////////////////////////")
		self.writeLine("Data processing requested was "+self.dataProcessing)
		self.writeLine("Algorithm requested was "+self.algorithm)

		self.writeLine("CONFIGURATION:")
		for key, value in self.configuration.items():
				if key == "Layers":
					for keyL, valueL in value.items():
						self.writeLine( keyL+" -> Neurons: "+str(valueL[0]+"  Activation Function: "+valueL[1]))
				else:
					self.writeLine( key+": "+str(value).strip("[").strip("]") )

		self.writeLine("//////////////////////////////////////////////////////////////////////////////////////////")
		self.writeLine("////////////////////// Features of Input Data ////////////////////////////////////////////")
		self.writeLine("//////////////////////////////////////////////////////////////////////////////////////////")

		self.writeLine("DATA READY: ")
		self.writeLine("All info of activates modules read, labels was converted to numbers...")
		self.writeLine(" CLASS = ACTION ")
		self.writeLine("   0   = Nada ")
		self.writeLine("   1   = Caminando " )
		self.writeLine("   2   = Rumiando(Trotadora)")
		self.writeLine("   3   = Comiendo(Elíptica)")
		self.writeLine("   4   = Agua(Escaladora))")
		self.writeLine(" ")
		self.writeLine(" X Shape: " + str(self.dataResults['X'].shape))
		self.writeLine(" Y Shape: " + str(self.dataResults['Y'].shape))
		self.writeLine("  ")
		
		self.writeLine("//////////////////////////////////////////////////////////////////////////////////////////")
		self.writeLine("////////////////////// Results ML Model //////////////////////////////////////////////////")
		self.writeLine("//////////////////////////////////////////////////////////////////////////////////////////")


		if self.algorithm == "Random Forest":
			self.writeLine("Random Forest:")
			if self.configuration['Hyperparameter optimization']==True:
				for trainingN in range(1,int(self.configuration['# of Trainings'])+1):
					self.writeLine("------------------------------------------------------------------------------------------")
					self.writeLine("Trainning number "+ str( trainingN))
					self.writeLine('There are ' + str(self.dataResults['X_train_'+str(trainingN)].shape[0]) + ' training data and ' + str(self.dataResults['X_test_'+str(trainingN)].shape[0])+ ' testing data. ')
					self.writeLine(np.array2string(np.vstack((np.unique(self.dataResults['Y_train_'+str(trainingN)]), np.bincount(self.dataResults['Y_train_'+str(trainingN)]))).T ))
					self.writeLine(" ")
					self.writeLine("After looking for parameters . . . ")
					self.writeLine("The best parameters found by the optimization method was:")
					self.writeLine("   n_estimators       =   "+str(self.dataResults["Opti_nEstimators_"+str(trainingN)]))
					self.writeLine("   max_features       =   "+str(self.dataResults["Opti_max_feature_"+str(trainingN)]))					
					self.writeLine("   n_samples_leaf     =   "+str(self.dataResults["Opti_samples_leaf_"+str(trainingN)]))
					self.writeLine("And the accuaracy precission with this parameters was:")					
					self.writeLine("   Accuaracy precission Percentage    =   "+str(int((self.dataResults['OptimaxPrecision_'+str(trainingN)])*100)))

			else:
				for trainingN in range(1,int(self.configuration['# of Trainings'])+1):
					self.writeLine("------------------------------------------------------------------------------------------")
					self.writeLine("Trainning number "+ str( trainingN))
					self.writeLine('There are ' + str(self.dataResults['X_train_'+str(trainingN)].shape[0]) + ' training data and ' + str(self.dataResults['X_test_'+str(trainingN)].shape[0])+ ' testing data. ')
					self.writeLine(np.array2string(np.vstack((np.unique(self.dataResults['Y_train_'+str(trainingN)]), np.bincount(self.dataResults['Y_train_'+str(trainingN)]))).T ))
					self.writeLine(" ")
					self.writeLine("After training random forest . . .")
					self.writeLine('The Calculated importance of variables for prediction was:')
					self.writeLine("   "+ str(np.around(self.dataResults['importanciaVars_'+str(trainingN)], decimals = 3)))
					self.writeLine(" ")
					self.writeLine("""Validation data prediction was: """ + str("%.4f" % self.dataResults['precision_'+str(trainingN)]))
					self.writeLine(" ")
					self.writeLine(""" Graph confusion matrix... """)
					self.writeLine(np.array2string(np.array(self.dataResults['Condusionmatrix_'+str(trainingN)] ) ))
		elif self.algorithm == "Neural Network":
			self.writeLine("Neural Network")
			self.writeLine("------------------------------------------------------------------------------------------")
					
		elif self.algorithm == "Convolutional Neural Network":
			self.writeLine("Convolutional Neural Network")
			self.writeLine("------------------------------------------------------------------------------------------")
					
		self.writeLine("//////////////////////////////////////////////////////////////////////////////////////////")
		self.writeLine("/////////////////////////// END OF REPORT ////////////////////////////////////////////////")
		self.writeLine("//////////////////////////////////////////////////////////////////////////////////////////")
		self.f.close()

	def writeLine(self, text):
		self.f.write(text+"\n")