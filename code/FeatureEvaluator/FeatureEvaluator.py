from DatasetHandler.DatasetHandler import DatasetHandler
from AudioPreprocessor.AudioPreprocessor import AudioPreprocessor
from FeatureExtractor.FeatureExtractor import FeatureExtractor

import numpy as np
import librosa
import tensorflow as tf

class FeatureEvaluator:
    def __init__(self, dataset_base_path) -> None:
        self.dataset = DatasetHandler(dataset_base_path)
        self.X = None
        self.y = None
        self.X_evaluation = None
        self.y_evaluation = None
        self.model = None

    def get_model_dataset(self):
        return self.X, self.y

    def set_model_dataset(self, X, y):
        self.X = np.asarray(X)
        self.y = np.asarray(y)

    def get_evaluation_dataset(self):
        return self.X_evaluation, self.y_evaluation

    def set_evaluation_dataset(self, X, y):
        self.X_evaluation = np.asarray(X)
        self.y_evaluation = np.asarray(y)

    def create_dataset(self, speaker_ids, extraction_pattern, frames_per_chunk, chunks_per_speaker, samples_per_frame, samples_overlap, window_function=np.hanning, start_at_file_index=0): #(*@\label{line:createDatasetStart}@*)
        frames_per_speaker = frames_per_chunk * chunks_per_speaker

        dataset = []
        dataset_speaker_ids = []

        print("Create dataset process started.")
        print(f"{samples_per_frame} samples per frame, {samples_overlap} samples overlap, {frames_per_speaker} frames per speaker.")
        print()

        for speaker_id in speaker_ids:
            print(f"Creating dataset for speaker {speaker_id:02}:")
            # get frames_per_speaker frames for speaker_id
            feature_list = []
            file_index = start_at_file_index
            while (len(feature_list) < frames_per_speaker):
                file_path = self.dataset.get_speaker_file_path(speaker_id, file_index)

                # Load audio file
                print(f"Loading dataset {file_index:04} ...", end="\r")
                y, sr = librosa.load(file_path)

                # Preprocess audio file
                y = AudioPreprocessor.remove_noise(y=y, sr=sr)
                y = AudioPreprocessor.remove_silence(y=y)
                # frame_size: frame_duration * sr, overlap: frame_size * overlap
                frames = AudioPreprocessor.create_frames(y=y, frame_size=samples_per_frame, overlap=samples_overlap)
                windowed_frames = AudioPreprocessor.window_frames(frames=frames, window_function=window_function)

                # Extract features
                feature_extractor = FeatureExtractor(windowed_frames, sr)
                features = feature_extractor.extract_features(extraction_pattern)

                feature_list.extend(features)
                file_index += 1

            print(f"Extracted features for {len(feature_list)} frames from {file_index - start_at_file_index} files.")
            print(f"Concatenating frames to chunks of {frames_per_chunk} frames ...")

            # concat features to chunks
            chunks = []
            for i in range(0, len(feature_list), frames_per_chunk):
                print(f"Chunk: {int(i/20):06}", end="\r")
                chunks.append(np.concatenate(feature_list[i:i+frames_per_chunk]))

            print(f"Created {len(chunks)} chunks, using first {chunks_per_speaker} chunks.")
            print()

            dataset.extend(chunks[:chunks_per_speaker])
            # create numpy array that has chunks_per_speaker times value speaker_id
            dataset_speaker_ids.extend(np.full((chunks_per_speaker), speaker_id))

        print("Dataset created.")
        return dataset, dataset_speaker_ids #(*@\label{line:createDatasetEnd}@*)
    
    def unison_shuffled_copies(self, X, y):
        a = np.asarray(X)
        b = np.asarray(y)
        assert len(a) == len(b)
        p = np.random.permutation(len(a))
        return a[p], b[p]
    
    def create_nn_model(self, epochs):
        if (self.X is None or self.y is None or len(self.X) != len(self.y)):
            print("Model dataset is not set or not valid.")
            return

        input_layer_neurons = self.X[0].shape[0]
        output_layer_neurons = np.max(self.y) + 1 #(*@\label{line:NNOutput}@*)

        # shuffle dataset
        X, y = self.unison_shuffled_copies(self.X, self.y) #(*@\label{line:shuffle}@*)

        # create model
        model = tf.keras.models.Sequential([ #(*@\label{line:NNStart}@*)
            tf.keras.layers.Flatten(input_shape=[input_layer_neurons]),
            tf.keras.layers.Dense(16, activation=tf.nn.relu),
            tf.keras.layers.Dense(16, activation=tf.nn.relu),
            tf.keras.layers.Dense(output_layer_neurons, activation=tf.nn.softmax),
        ]) #(*@\label{line:NNEnd}@*)

        model.compile(optimizer=tf.optimizers.Adam(), loss='sparse_categorical_crossentropy', metrics=['accuracy'])

        model.fit(X, y, epochs=epochs, verbose=0)

        self.model = model

    def evaluate_model(self): #(*@\label{line:evaluateModelStart}@*)
        if (self.model is None or self.X_evaluation is None or self.y_evaluation is None):
            print("Model or evaluation dataset is not set.")
            return
        
        loss, accuracy = self.model.evaluate(self.X_evaluation, self.y_evaluation, verbose=0)

        print(f"Model loss: {loss}")
        print(f"Model accuracy: {accuracy}") #(*@\label{line:evaluateModelEnd}@*)

    def predict(self, X): #(*@\label{line:predictStart}@*)
        if (self.model is None):
            print("Model is not set.")
            return
        
        prediction = self.model.predict(X)

        ids = np.unique(np.argmax(prediction, axis=1))

        for predicted_id in ids:
            print(f"ID {predicted_id}: {np.count_nonzero(np.argmax(prediction, axis=1) == predicted_id)}") #(*@\label{line:predictEnd}@*)