"""
 @file Serializer.py
 @section authors
  - 
"""
from ModelTrainer import ModelTrainer
from Evaluator import Evaluator

import os
import tensorflow as tf
import numpy as np

class Serializer:
    """
    @brief Serialization functions for main components (nn and training data)


    """
    def __init__(self, folder_path):
        """
        @brief Initializes the object with default values

        Parameters : 
            @param folder_path => default path for saving/loading serialized objects

        """
        self.folder_path = folder_path

    def serialize(self, model_trainer: ModelTrainer, evaluator: Evaluator):
        """
        @brief Serializes a nn model trainer and evaluator

        Parameters : 
            @param model_trainer : ModelTrainer => object to serialize
            @param evaluator : Evaluator => object to serialize

        """
        # check if folder_path exists, otherwise create
        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path)

        # create a folder for the neural_network_id
        os.mkdir(os.path.join(self.folder_path, model_trainer.neural_network_id))

        # store the neural network
        model_trainer.neural_network.save(os.path.join(self.folder_path, model_trainer.neural_network_id, "neural_network.h5"))

        # store the training data
        dataset_path = os.path.join(self.folder_path, model_trainer.neural_network_id, "dataset")
        os.mkdir(dataset_path)
        training_X, training_y = model_trainer.get_training_data()
        with open (os.path.join(dataset_path, "training_X.npy"), "wb") as f:
            np.save(f, training_X)
        with open (os.path.join(dataset_path, "training_y.npy"), "wb") as f:
            np.save(f, training_y)

        # store the test data
        test_X, test_y = evaluator.get_test_data()
        with open (os.path.join(dataset_path, "test_X.npy"), "wb") as f:
            np.save(f, np.array(test_X, dtype=object))
        with open (os.path.join(dataset_path, "test_y.npy"), "wb") as f:
            np.save(f, np.array(test_y, dtype=object))

    def deserialize(self, nn_id) -> tuple[ModelTrainer, Evaluator]:
        """
        @brief deserializes a serialized tuple of ModelTrainer and Evaluator. Since the nn id is not serialized, it has to be provided

        Parameters : 
            @param nn_id => neural network id

        """
        
        # load the neural network
        neural_network = tf.keras.models.load_model(os.path.join(self.folder_path, nn_id, "neural_network.h5"))

        # load the training data
        dataset_path = os.path.join(self.folder_path, nn_id, "dataset")
        training_X, training_y = None, None
        with open(os.path.join(dataset_path, "training_X.npy"), "rb") as f:
            training_X = np.load(f)
        with open(os.path.join(dataset_path, "training_y.npy"), "rb") as f:
            training_y = np.load(f)

        model_trainer = ModelTrainer()
        model_trainer.set_neural_network(neural_network, nn_id)
        model_trainer.set_training_data(training_X, training_y)

        # load the evaluator
        test_X, test_y = None, None
        with open(os.path.join(dataset_path, "test_X.npy"), "rb") as f:
            test_X = np.load(f, allow_pickle=True)
        with open(os.path.join(dataset_path, "test_y.npy"), "rb") as f:
            test_y = np.load(f, allow_pickle=True)

        evaluator = Evaluator(neural_network, nn_id, test_X, test_y)

        return model_trainer, evaluator