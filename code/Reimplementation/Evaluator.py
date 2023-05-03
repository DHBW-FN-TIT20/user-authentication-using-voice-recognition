class Evaluator:
    def __init__(self, neural_network, neural_network_id):
        results = None
        neural_network = neural_network
        neural_network_id = neural_network_id
        test_data = None

    def evaluate(self):
        pass
    
    def get_test_data(self):
        pass

    def set_test_data(self, X, y):
        # TODO: Überlegen wegen test-data array
        pass

    def get_test_result(self):
        pass

    def set_neural_network(self, neural_network, neural_network_id):
        self.neural_network = neural_network
        self.neural_network_id = neural_network_id

    def get_results(self):
        return self.results

