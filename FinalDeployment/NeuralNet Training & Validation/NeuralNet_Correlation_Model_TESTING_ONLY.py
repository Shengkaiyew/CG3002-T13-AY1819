from ExtractFeaturesCorrelation import extractFeatures
import numpy as np

from sklearn.externals import joblib
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import MinMaxScaler

SAVED_MODEL_NAME = "NeuralNet_Correlation"
SAVED_SCALER_NAME = "NeuralNet_Correlation_Scaler"

MAX_PREDICTION_ATTEMPTS = 3
#Mininum confidence for the model to output a prediction. If this is not met, steps will be taken to make a good guess.
CONFIDENCE_THRESHOLD = 0.90

SAMPLING_RATE = 50 #Sampling frequency in Hz
WINDOW_DURATION = 2 #Duration of window in seconds
SAMPLES = SAMPLING_RATE * WINDOW_DURATION
FEATURES = 19
WINDOW_SIZE = SAMPLES * FEATURES

class DanceClassifierNN_TEST_MODE:
    def __init__(self):
        self.clf = joblib.load(SAVED_MODEL_NAME)
        self.scaler = joblib.load(SAVED_SCALER_NAME)

    #############################################################################################
    #THE FOLLOWING FUNCTIONS BELOW ARE ONLY TO BE USED FOR TESTING PURPOSES. NOT FOR DEPLOYMENT!#
    #############################################################################################
    def TEST_MODE_DETECT_MOVE(self, window):
        if (len(window) != WINDOW_SIZE):
            print("ERROR: Window size does not match!")
            print("Expected window size is " + str(WINDOW_SIZE) + ". Input size: " + str(len(window)))
            return None
        
        processedData = extractFeatures(window)
        
        scaledData = self.scaler.transform([processedData])

        currentPrediction = self.clf.predict(scaledData)
        
        confidence_array = self.clf.predict_proba(scaledData)
        currentConfidence = max(confidence_array[0])

        if (currentConfidence < CONFIDENCE_THRESHOLD):
            print(currentPrediction, currentConfidence)

        return currentPrediction

    #Helper function to get the current and next best confidence for the prediction
    def TEST_MODE_GET_CONFIDENCE(self, window):
        if (len(window) != WINDOW_SIZE):
            print("ERROR: Window size does not match!")
            print("Expected window size is " + str(WINDOW_SIZE) + ". Input size: " + str(len(window)))
            return None

        processedData = extractFeatures(window)
        
        scaledData = self.scaler.transform([processedData])
        
        confidence_array = self.clf.predict_proba(scaledData)
        currentConfidence = max(confidence_array[0])
        print("Current confidence is ", str(currentConfidence))

        confidence_array2 = list(confidence_array[0])
        confidence_array2.remove(currentConfidence)
        currentConfidence2 = max(confidence_array2)
        print("Next best confidence is ", str(currentConfidence2))
        print() #Print newline for readability

        
