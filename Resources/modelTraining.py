import time
import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt
#import seaborn as sns

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.utils import shuffle
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2

import math

### 
COLUMNA_FECHA = 0
COLUMNA_X1 = 3
COLUMNA_X2 = 4
COLUMNA_X3 = 5
COLUMNA_X4 = 6
COLUMNA_X5 = 7
COLUMNA_X6 = 8
COLUMNA_LABEL = 9
feat_labels = [ "X1" , "X2", "X3" , "X4", "X5", "X6"]


#optionsDataProcessing = ["Use all data available", "Use 1 data/sec", "Use a dynamic window of data"] #0,1,2
#optionsAlgorithm = ["Random Forest", "Neural Network", "Convolutional Neural Network"] #0,1,2

# Random Forest:
#configuration {'% Train': '70', '# of Trainings': '3', 'Hyperparameter optimization': True, 'Active Module IDs': [1, 2]}
# neural network
# configuration {'% Train': '0', 'Total layers': 1, 'Layers': {'Layer 1': ['0', 'Sigmoidal']}, 'Active Module IDs': [1, 2]}
def trainModel(pDataFrames, pDataProcessing, pAlgorithm, configuration):
	time.sleep(2)
	print("--------------------------------------------------------")
	print("Start: Training Model")
	print("--------------------------------------------------------")
	#print("pDataFrames",pDataFrames)

	activeModules = configuration['Active Module IDs']
	#print("activeModules",activeModules)

	X = []
	Y = []
	##########################################
	### functions  optionsDataProcessing
	##########################################
	if pDataProcessing == 0:
		#### "Use all data available"
		X, Y = useAllDataAvailable(pDataFrames, activeModules)
	elif pDataProcessing ==1:
		#### "Use 1 data/sec"
		X, Y = averagePerSecond(pDataFrames, activeModules)
	elif pDataProcessing ==2:
		#### "Use a dynamic window of data"
		X, Y = dynamicWindow(pDataFrames, activeModules)
		
	#print("X", "Y", X, Y)

	### it is mandatory convert the labels to numbers.
	Y = convertLabelsToNumbers(Y)
	print("Data is ready")
	print("--------------------------------------------------------")
###
###
###
### to do:
###aqui ya se puede hacer la gráfica de feauture vs feature
###
###
###

	##########################################
	### functions pAlgorithm
	##########################################
	model = ""
	if pAlgorithm == 0:
		#### Random Forest"
		model = algorithmRandomForest(configuration, X, Y)
	elif pAlgorithm ==1:
		#### "Neural Network"
		model = algorithNeuralNetwork(configuration, X, Y)
		
	elif pAlgorithm ==2:
		#### "Convolutional Neural Network"
		model = algorithConvolutionNeuralNetwork(configuration, X, Y)
		

	
	print("--------------------------------------------------------")
	print("Model Training finished successful ")
	print("--------------------------------------------------------")
	print("model", model)

	return []

####################################################################################
### label string to number
####################################################################################
# 0 = Nada
# 1 = Caminando  
# 2 = Rumiando(Trotadora)
# 3 = Comiendo(Elíptica)
# 4 = Agua(Escaladora)
def convertLabelsToNumbers(arrayLabelsString):
	arrayLabelsInt = []

	for dato in arrayLabelsString:
		if (dato == "Nada"):
			arrayLabelsInt.append(0)
		elif (dato == "Caminando" ):
			arrayLabelsInt.append(1)
		elif (dato == "Rumiando(Trotadora)" ):
			arrayLabelsInt.append(2)
		elif (dato == "Comiendo(Elíptica)" ):
			arrayLabelsInt.append(3)
		elif (dato == "Tomando Agua(Escaladora)" ):
			arrayLabelsInt.append(4)

	arrayLabelsInt = np.array(arrayLabelsInt)
	return arrayLabelsInt


####################################################################################
### functions  optionsDataProcessing
####################################################################################
def useAllDataAvailable(pDataFrames, activeModules):
	print("pDataProcessing  0 : Use all data available")
	nModule = len(pDataFrames)
	nActivateModules = len(activeModules)

	#dataToUse = ['x1','x2','x3','x4','x5','x6'] don't care modules
	dataToUse = np.array([[0, 0, 0 , 0 , 0 , 0 ]])
	labelToUse = [""]
	
	for i in range(0,nActivateModules):
		### id-1, list in python begin in 0
		idModulei = activeModules[i]-1
		datosActiveModulei = np.array(pDataFrames[idModulei])
		### add data for activateModule i 
		dataToUse = np.concatenate ( (dataToUse,   datosActiveModulei[ : , COLUMNA_X1:COLUMNA_LABEL ] ) )
		labelToUse =  np.concatenate(  ( labelToUse,  datosActiveModulei[ : , COLUMNA_LABEL ] ) )

	## delete the first row of zeros
	dataToUse = dataToUse[1:dataToUse.shape[0], :]
	labelToUse =  labelToUse[1:labelToUse.shape[0]]
	print("--------------------------------------------------------")
	print("Done: --> Used all data available of active modules")
	print("--------------------------------------------------------")
	return(dataToUse,labelToUse)

def averagePerSecond(pDataFrames, activeModules):
	print("pDataProcessing 1: Use 1 data/sec")
	nModule = len(pDataFrames)
	nActivateModules = len(activeModules)

	#dataToUse = ['x1','x2','x3','x4','x5','x6'] don't care modules
	dataToUse = np.array([[0, 0, 0 , 0 , 0 , 0 ]])
	labelToUse = [""]
	
	for i in range(0,nActivateModules):
		### id-1, list in python begin in 0
		idModulei = activeModules[i]-1
		datosActiveModulei = np.array(pDataFrames[idModulei])
		
		### one by one second have a average... 
		segundoAnterior = ""
		promedio = datosActiveModulei[ 0 , COLUMNA_X1:COLUMNA_LABEL ]
		data_Modulei_Average = []
		label_Modulei_STRING = []
		for informacion in datosActiveModulei :
			segundoActual = informacion[ COLUMNA_FECHA ]

			if segundoActual == segundoAnterior:
				promedio = np.average( [informacion[  COLUMNA_X1:COLUMNA_LABEL ], promedio]   , axis=0) 
			else:
				data_Modulei_Average.append(  np.around ( promedio.tolist(), decimals = 3  ).tolist()   )
				label_Modulei_STRING.append(informacion[COLUMNA_LABEL] )
				segundoAnterior = segundoActual
				promedio = informacion[ COLUMNA_X1:COLUMNA_LABEL ]

		print("Active module number ",i," had a record for " , len(label_Modulei_STRING), "seconds.")

		### add data for activateModule i
		dataToUse = np.concatenate ( (dataToUse,  data_Modulei_Average  ) )
		labelToUse =  np.concatenate(  ( labelToUse, label_Modulei_STRING ) )


	## delete the first row of zeros
	dataToUse = dataToUse[1:dataToUse.shape[0], :]
	labelToUse =  labelToUse[1:labelToUse.shape[0]]

	# print("dataToUse", dataToUse)
	# print("dataToUse shape", dataToUse.shape)
	# print("labelToUse", labelToUse)
	# print("labelToUse shape", labelToUse.shape)
	print("--------------------------------------------------------")
	print("Done: --> Used 1 data/sec")
	print("--------------------------------------------------------")
	return(dataToUse,labelToUse)

def dynamicWindow(pDataFrames, activeModules):
	print("pDataProcessing 2: Use a dynamic window of data ")
	X = [3]
	Y = [3]
	nModule = len(pDataFrames)
	return(X,Y)

####################################################################################
### functions pAlgorithm
####################################################################################
def algorithmRandomForest(configuration, X, Y):
	# Random Forest:
	#configuration {'% Train': '70', '# of Trainings': '3', 'Hyperparameter optimization': True}
	#'Hyperparameter optimization': False, 'N-estimators': '0', 'Max features': '0', 'Min samples leaf': '0'}
	print("Start: Random Forest")
	percentageTrain = configuration['% Train']
	percentageTest = np.around(1-(int(percentageTrain)/100), decimals = 3)
	nTrainings = int(configuration['# of Trainings'])
	print("percentageTrain", percentageTrain, "  nTrainings", nTrainings, "percentageTest", percentageTest)
	optimization=configuration['Hyperparameter optimization']

	if optimization == True:
		## optimization search the best hiperparameter for the data.
		print("looking for parameters . . .")
			### repeat all, for each training
		for trainingN in range(1,nTrainings+1):
			print("--------------------------------------------------------")
			print("Trainning number ", trainingN)
			X, Y = shuffle(X,Y)
			X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=percentageTest, random_state=0)
			print('There are', X_train.shape[0], 'training data and',  X_test.shape[0], 'testing data.')
			print(np.vstack((np.unique(Y_train), np.bincount(Y_train))).T)

			### primero optimzar n_Estimators que debe ser un entero entre 0 y 160
			modelMaximum = ""
			resultados =[["nArboles", "n_max_features", "n_min_samples_leaf", "precision"]]
			maximunAccuarance = 0
			x_n_Estimators = range(1,140,5)
			for nArboles in x_n_Estimators:
				for n_max_features in range(1,6):
					for n_min_samples_leaf in range(1,10):
						### training random forest . . . with the input parameters
						model_rf = RandomForestClassifier(n_estimators=nArboles, max_features=n_max_features, min_samples_leaf=n_min_samples_leaf,random_state=0, n_jobs=2)
						model_rf.fit(X_train, Y_train.ravel())
						y_pred = model_rf.predict(X_test)
						precision=accuracy_score(Y_test, y_pred)
						resultados = resultados + [nArboles,n_max_features,n_min_samples_leaf,"%.4f" %precision]
						print(nArboles,n_max_features,n_min_samples_leaf,"%.4f" %precision)

			print("resultados ")
			print(resultados )



	else:
			### repeat all, for each training
		for trainingN in range(1,nTrainings+1):
			print("--------------------------------------------------------")
			print("Trainning number ", trainingN)
	
			X, Y = shuffle(X,Y)
			X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=percentageTest, random_state=0)
			print('There are', X_train.shape[0], 'training data and',  X_test.shape[0], 'testing data.')
			print(np.vstack((np.unique(Y_train), np.bincount(Y_train))).T)
#####
##### to do:
#####primera grafica a guardar		
		#sns.countplot(Y_train)
		#plt.show()
#####
#####

			### training random forest . . . with the input parameters
			print("training random forest . . .")
			nEstimators = int(configuration['N-estimators'])
			nMaxFeatures = int(configuration['Max features'])
			nMinSamplesLeaf = int(configuration['Min samples leaf'])
			print("nEstimators","nMaxFeatures","nMinSamplesLeaf",nEstimators,nMaxFeatures,nMinSamplesLeaf)
			
			model_rf = RandomForestClassifier(n_estimators=nEstimators, max_features=nMaxFeatures, min_samples_leaf=nMinSamplesLeaf,random_state=0, n_jobs=2)
			model_rf.fit(X_train, Y_train.ravel())
			#####################################################
			# Encontrar importancia de cada variable, y graficar
			print('Calculating importance of variables for prediction ...')
			importanciaVars=model_rf.feature_importances_
			print(np.around(importanciaVars, decimals=3))

#####
##### to do:
			# # Graficar con barras la importancia de cada variable
			# pos=[1, 2, 3, 4, 5, 6]
			# plt.rcdefaults()
			# fig, ax = plt.subplots()
			# ax.barh(pos, importanciaVars, align='center',color='blue')
			# ax.set_yticks(pos)
			# ax.set_yticklabels(feat_labels)
			# ax.invert_yaxis()  # labels read top-to-bottom
			# ax.set_xlabel('Importancia Variables')
			# #plt.show()
#####
#####

			# Validation data prediction
			print("""
				Validation data prediction...""")
			y_pred = model_rf.predict(X_test)
			precision=accuracy_score(Y_test, y_pred)
			print("%.4f" %precision)

			# Matriz de confusion
			print("""
				Graph confusion matrix...
				""")
			tabla=pd.crosstab(Y_test.ravel(), y_pred, rownames=['Actual LOS'], colnames=['Predicted LOS'])
			print(tabla*100/len(y_pred))

	model = "aun no"
	return model

def algorithNeuralNetwork(configuration, dataX, dataY):
	# neural network
	# configuration {'% Train': '0', 'Total layers': 1, 'Layers': {'Layer 1': ['0', 'Sigmoidal']}}
	print("pAlgorithm 1: Neural Network")
	percentageTrain = configuration['% Train']
	totalLayers = configuration['Total layers']
	infoLayers = configuration['Layers']
	for i in range(1,totalLayers+1):
		print("layer ", i)
		nNeuronsi = infoLayers[ str('Layer ' + str(i) ) ][0]
		print("neuronas", nNeuronsi )
		functionActivationi = infoLayers[ str('Layer ' + str(i) ) ][1]
		print("function", functionActivationi )

	model = "aun no"
	return model

def algorithConvolutionNeuralNetwork(configuration, dataX, dataY):
	print("pAlgorithm 2: Convolutional Neural Network ")
	print("configuration", configuration)
	model = "aun no"
	return model

