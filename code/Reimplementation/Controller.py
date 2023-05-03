from AudioPreprocessor import AudioPreprocessor
from DatasetHandler import DatasetHandler
from FeatureExtractor.FeatureExtractor import FeatureExtractor, Feature
from ModelTrainer import ModelTrainer
from Evaluator import Evaluator
from Serializer import Serializer

import numpy as np
import librosa

class Controller:
    def __init__(self, csv_path):
        self.config = None
        self.data_path = "/home/henry/Downloads/audio_dataset"
        self.serialize_base_path="/home/henry/Downloads/serialized"
        self.csv_path = csv_path

    def append_results_to_csv(self, test_results, neural_network_id):
        with open(self.csv_path, "a") as csv_file:
            for test_result in test_results:
                csv_string = f'{neural_network_id};{test_result.sample_id};{self.config["amount_of_frames"]};{self.config["size_of_frame"]};{self.config["lpc_weight"]};{self.config["lpc_order"]};{self.config["mfcc_weight"]};{self.config["mfcc_order"]};{self.config["lpcc_weight"]};{self.config["lpcc_order"]};{self.config["delta_mfcc_weight"]};{self.config["delta_mfcc_order"]};{test_result["speaker_id"]};'
                for speaker_id in range(20):
                    # TODO: Check with Lukas if this is correct
                    csv_string += test_result.correspondence[f"{speaker_id}"] or "0"
                    csv_string += ";"
                csv_file.write(csv_string + "\n")

    def set_config(self, config):
        self.config = config

    def extract_features(self, file_path, speaker_id, feature_list, limit_frames=True):
        audio_preprocessor = AudioPreprocessor()

        # load and preprocess file
        y, sr = librosa.load(file_path)
        y = audio_preprocessor.remove_silence(y)
        y = audio_preprocessor.remove_noise(y, sr)

        frames = audio_preprocessor.create_frames(y=y, frame_size=self.config["size_of_frame"], overlap=0.5)

        if limit_frames:
            if len(frames) < self.config["amount_of_frames"]:
                print(f"Warning: Not enough frames for speaker {speaker_id}.")
            else:
                frames = frames[0:self.config["amount_of_frames"]]

        windowed_frames = audio_preprocessor.window_frames(frames=frames, window_function=np.hanning)

        # extract features
        print("Extracting features ...")

        extractor = FeatureExtractor(frames=windowed_frames, sr=sr)

        return extractor.extract_features(feature_list=feature_list)

    def start(self):
        # INITIALIZATION
        print("Initialization started.")
        
        if self.config is None:
            print("No config set. Aborting.")
            return
        
        ds_handler = DatasetHandler(self.data_path)

        # convert config to feature_list
        feature_list = []
        for i in range(self.config["lpc_weight"]):
            feature_list.append([Feature.LPC, self.config["lpc_order"], [0]])
        for i in range(self.config["mfcc_weight"]):
            feature_list.append([Feature.MFCC, self.config["mfcc_order"], [0]])
        for i in range(self.config["lpcc_weight"]):
            feature_list.append([Feature.LPCC, self.config["lpcc_order"], [0]])
        for i in range(self.config["delta_mfcc_weight"]):
            feature_list.append([Feature.MFCC, self.config["delta_mfcc_order"], [1]])

        print("Initialization finished.")

        # COLLECTING TRAINING DATA
        print("Collecting training data for all 20 speakers.")

        training_X = np.array([])
        training_y = np.array([])

        for speaker_id in range(20):
            print(f"Collecting training data for speaker {speaker_id} ...")

            training_file_path = ds_handler.get_training_file_path(speaker_id)

            features = self.extract_features(training_file_path, speaker_id, feature_list, limit_frames=True)

            # append features to X and y
            training_X = np.append(training_X, features)
            training_y = np.append(training_y, np.full(len(features), speaker_id))

        print("Training data collected.")

        # COLLECTING TEST DATA
        print("Collecting test data for all 20 speakers. (5 files per speaker)")

        test_X = []
        test_y = []

        for speaker_id in range(20):
            print(f"Collecting test data for speaker {speaker_id} ...")

            for i in range(5):
                test_file_path = ds_handler.get_test_file_path(speaker_id, i)

                features = self.extract_features(test_file_path, speaker_id, feature_list, limit_frames=False)

                # add X and y to the lists
                test_X.append(features)
                test_y.append(np.full(len(features), speaker_id))

        print("Test data collected.")

        # TRAINING
        # execute training 3 times with different sorted training data

        for training_process in range(3):
            print(f"Start training process {training_process}.")

            # train model
            trainer = ModelTrainer()
            trainer.set_training_data(training_X, training_y)
            trainer.generate_neural_network()
            neural_network, neural_network_id = trainer.get_neural_network()

            print("Generated neural network.")

            print("Start evaluating network.")

            evaluator = Evaluator(neural_network, neural_network_id)
            evaluator.set_test_data(test_X, test_y)
            evaluator.evaluate()
            results = evaluator.get_results()

            print("Evaluation finished, saving data ...")
        
            serializer = Serializer(self.serialize_base_path)
            serializer.serialize(trainer, evaluator)

            self.append_results_to_csv(results, neural_network_id)

            print("Data saved.")
        
        print("Configuration completed.")
