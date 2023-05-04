import TestResult
import numpy as np
class Evaluator:
    def __init__(self, neural_network, neural_network_id, test_data):
        self.results = None
        self.neural_network = neural_network
        self.neural_network_id = neural_network_id
        self.test_data = test_data

    """Evaluates the neural network with a prediction for test data and saves the results"""
    def evaluate(self):
        for sample in  self.test_data:
            prediction = self.neural_network.predict(sample)  # generate prediction for the sample
            speaker = np.argmax(prediction)     # select the output class with highest probability
            # TODO speaker_id, sample_id has to be extracted from test data --> How is Test data structured? maybe use a class or tuple for it.
            result = TestResult(speaker_id = None, sample_id = None, correspondence = None)  # create a TestResult object
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
    