import TestResult
class Evaluator:
    def __init__(self, neural_network, neural_network_id):
        self.results = None
        self.neural_network = neural_network
        self.neural_network_id = neural_network_id
        self.test_data = None

    """Evaluates the neural network with the test data and saves the results"""
    def evaluate(self):
        pass
    
    def set_test_data(self, X, y):
        # TODO: Überlegen wegen test-data array
        pass

    def set_neural_network(self, neural_network, neural_network_id):
        self.neural_network = neural_network
        self.neural_network_id = neural_network_id

    def get_test_data(self):
        return self.test_data
    
    def get_results(self):
        return self.results
