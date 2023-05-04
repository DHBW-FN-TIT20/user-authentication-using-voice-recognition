import TestResult
import numpy as np
class Evaluator:
    def __init__(self, neural_network, neural_network_id, test_dataX, test_dataY):
        self.results = None
        self.neural_network = neural_network
        self.neural_network_id = neural_network_id
        self.test_data_X:list[list[int]] = test_dataX # [[[]]] for each file, for each frame, X input values
        self.test_data_Y:list[int] = test_dataY # [[]] for each file, for each Frame the same speaker_id

    """Evaluates the neural network with a prediction for test data and saves the results"""
    def evaluate(self):
        for i in range(len(self.test_data_X)): # for each file
            prediction = self.neural_network.predict(self.test_data_X[i])  # generate prediction for the sample
            speaker_id = self.test_data_Y[i][0] # get the speaker_id of the sample
            sample_id = i%5 # 0-4
            # TODO Calculate Correspondence in % and add it to the results
            result = TestResult(speaker_id = speaker_id, sample_id = sample_id, correspondence = None)  # create a TestResult object
            self.results.append(result)              # save the TestResult object in the list
        pass

    def get_test_data(self):
        return self.test_data
    
    def get_results(self):
        return self.results

    def get_neural_network_id(self):
        return self.neural_network_id
    
    def get_neural_network(self):
        return self.neural_network
    