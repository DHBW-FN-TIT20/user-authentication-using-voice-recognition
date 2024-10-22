"""
 @file Evaluator.py
 @section authors
  - Lukas Braun
"""
from TestResult import TestResult

import numpy as np

class Evaluator:
    """
    @brief Evaluates a feature set using the neural network


    """
    def __init__(self, neural_network, neural_network_id, test_data_x, test_data_y):
        """
        @brief Initializes the object

        Parameters : 
            @param neural_network => nn for evaluating the features
            @param neural_network_id => id of the nn (easy access for users of the class)
            @param test_data_x => values to use for the prediction/evaluation/classification
            @param test_data_y => expected results (used for saving the result)

        """
        self.results = []
        self.neural_network = neural_network
        self.neural_network_id = neural_network_id
        self.test_data_x = test_data_x # [[[]]] for each file, for each frame, X input values
        self.test_data_y = test_data_y # [[]] for each file, for each Frame the same speaker_id

    def evaluate(self):
        """
        @brief Evaluates the given test data using the given neural network and saves the results to the self.results list

        """
        for i in range(len(self.test_data_x)): # for each file
            prediction = self.neural_network.predict(np.asarray(self.test_data_x[i]))  # generate prediction for the sample
            speaker_id = self.test_data_y[i][0] # get the speaker_id of the sample
            sample_id = i%5 # 0-4
            correspondence = {}
            for id in range(20): # for each speaker
                correspondence[f"{id}"] = np.count_nonzero(np.argmax(prediction, axis=1) == id) / len(prediction)
            result = TestResult(speaker_id = speaker_id, sample_id = sample_id, correspondence = correspondence)  # create a TestResult object
            self.results.append(result)              # save the TestResult object in the list
    
    def get_test_data(self):
        return self.test_data_x, self.test_data_y
    
    def get_results(self):
        return self.results

    def get_neural_network_id(self):
        return self.neural_network_id
    
    def get_neural_network(self):
        return self.neural_network
    