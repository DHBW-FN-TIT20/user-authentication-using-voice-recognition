import TestResult
class Evaluator:
    def __init__(self, neural_network, neural_network_id, test_data):
        self.results = None
        self.neural_network = neural_network
        self.neural_network_id = neural_network_id
        self.test_data = test_data

    """Evaluates the neural network with the test data and saves the results"""
    def evaluate(self):
        pass

    def get_test_data(self):
        return self.test_data
    
    def get_results(self):
        return self.results

    def get_neural_network_id(self):
        return self.neural_network_id
    
    def get_neural_network(self):
        return self.neural_network
    