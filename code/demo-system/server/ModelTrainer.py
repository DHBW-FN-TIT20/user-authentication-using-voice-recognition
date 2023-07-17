"""
 @file ModelTrainer.py
 @section authors
  - Johannes Brandenburger
"""
import numpy as np
import tensorflow as tf
import uuid

class ModelTrainer:
    """
    @brief Class providing functionality for training a neural network


    """
    def __init__(self):
        """
        @brief Initializes the object and sets default values

        """
        self.training_data = { "X": None, "y": None}
        self.neural_network = None
        self.neural_network_id = None

    @staticmethod
    def unison_shuffled_copies(X, y):
        """
        @brief Shuffles two arrays in the same order

        Parameters : 
            @param X => array 1 to shuffle
            @param y => array 2 to shuffle

        """
        a = np.asarray(X)
        b = np.asarray(y)
        assert len(a) == len(b)
        p = np.random.permutation(len(a))
        return a[p], b[p]

    def generate_neural_network(self):
        """
        @brief trains a neural network with the provided training data

        """

        # guard
        if (self.training_data["X"] is None or self.training_data["y"] is None or len(self.training_data["X"]) != len(self.training_data["y"])):
            print("Model dataset is not set or not valid.")
            return
        
        # config
        epochs = 250
        hidden_layer_neurons = [128, 64, 32]

        # config based on the training data
        input_layer_neurons = self.training_data["X"][0].shape[0]
        output_layer_neurons = np.max(self.training_data["y"]) + 1

        # shuffle dataset
        X, y = self.unison_shuffled_copies(self.training_data["X"], self.training_data["y"])
        self.training_data["X"] = X
        self.training_data["y"] = y

        # create hidden/dense layers
        hidden_layer = []
        for i, neurons in enumerate(hidden_layer_neurons):
            hidden_layer.append(tf.keras.layers.Dense(neurons, activation=tf.nn.relu, name=f"hidden_layer_{i}"))
        
        # create model
        tf.keras.backend.clear_session()
        model = tf.keras.models.Sequential([
            tf.keras.layers.Flatten(input_shape=[input_layer_neurons]),
            *hidden_layer,
            tf.keras.layers.Dense(output_layer_neurons, activation=tf.nn.softmax),
        ])
        model.compile(optimizer=tf.optimizers.Adam(), loss='sparse_categorical_crossentropy', metrics=['accuracy'])

        # train model
        model.fit(X, y, epochs=epochs) # type: ignore

        # evaluate model (only if needed)
        # loss, accuracy = model.evaluate(X, y, verbose=0)
        # print(f"Model loss: {loss}")
        # print(f"Model accuracy: {accuracy}")

        self.neural_network = model

        # crate a uuid for the neural network
        self.neural_network_id = str(uuid.uuid4())

    def get_neural_network(self):
        """
        @brief returns the created neural network and its id

        """

        # guard
        assert self.neural_network is not None and self.neural_network_id is not None

        return self.neural_network, self.neural_network_id

    def set_neural_network(self, neural_network, neural_network_id):
        """
        @brief sets the nn and nn id value for serialization purpose

        Parameters : 
            @param neural_network => new nn value
            @param neural_network_id => new nn id

        """
        self.neural_network = neural_network
        self.neural_network_id = neural_network_id

    def get_training_data(self):
        """
        @brief Getter for the training data (X and y)

        """
        return (self.training_data["X"], self.training_data["y"])

    def set_training_data(self, X, y):
        """
        @brief Setter for the training data (X and y)

        Parameters : 
            @param X => new X value
            @param y => new y value

        """
        self.training_data = { "X": X, "y": y }