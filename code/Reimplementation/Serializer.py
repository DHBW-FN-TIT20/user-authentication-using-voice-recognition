from ModelTrainer import ModelTrainer
from Evaluator import Evaluator
import json
import os
import tensorflow as tf

class Serializer:
    def __init__(self, folder_path):
        self.folder_path = folder_path

    def serialize(self, model_trainer: ModelTrainer, evaluator: Evaluator):
        
        # create a folder for the neural_network_id
        os.mkdir(os.path.join(self.folder_path, model_trainer.neural_network_id))

        # store the neural network
        model_trainer.neural_network.save(os.path.join(self.folder_path, model_trainer.neural_network_id, "neural_network.h5"))

        # store the training data
        with open(os.path.join(self.folder_path, model_trainer.neural_network_id, "training_data.json"), "w") as f:
            json.dump(model_trainer.training_data, f)

        # store the evaluator
        with open(os.path.join(self.folder_path, model_trainer.neural_network_id, "evaluator.json"), "w") as f:
            json.dump(evaluator, f)

    def deserialize(self, nn_id) -> tuple[ModelTrainer, Evaluator]:
        
        # load the neural network
        neural_network = tf.keras.models.load_model(os.path.join(self.folder_path, nn_id, "neural_network.h5"))

        # load the training data
        with open(os.path.join(self.folder_path, nn_id, "training_data.json"), "r") as f:
            training_data = json.load(f)

        # load the evaluator
        with open(os.path.join(self.folder_path, nn_id, "evaluator.json"), "r") as f:
            evaluator = json.load(f)

        # create a model trainer
        model_trainer = ModelTrainer()
        model_trainer.set_neural_network(neural_network, nn_id)
        model_trainer.set_training_data(training_data["X"], training_data["y"])

        return model_trainer, evaluator