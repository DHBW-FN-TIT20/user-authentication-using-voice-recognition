import numpy as np
import librosa
import os
import tensorflow as tf
from tensorflow import keras
from FeatureExtraction import FeatureExtraction
from DatasetHandler import DatasetHandler
from AudioPreprocessor import AudioPreprocessor

class FeatureEvaluator:
    def __init__(self, dataset_basepath):
        _, self.n_features = FeatureExtraction.extract_features([], 0)
        self.dataset = DatasetHandler(dataset_basepath)
        self.nn_data = ([], [])
        self.total_input_chunks = 0
        self.n_speaker = None
        self.nn_data_is_created = False
        self.model_is_created = False
        self.start_at_speaker = 0

    def create_nn_data(self, total_input_chunks, n_speaker, start_at_speaker = 0, start_at_file = 0):
        self.total_input_chunks = total_input_chunks
        self.n_speaker = n_speaker
        self.start_at_speaker = start_at_speaker
        nn_input_chunks_per_speaker = int(total_input_chunks/n_speaker)
        frames_per_speaker = nn_input_chunks_per_speaker * 20

        all_speakers = []
        n_features = 0
        for speaker_index in range(0, n_speaker):
            all_speakers.append([])
            file_index = 0
            n_frames_of_current_speaker = 0
            while (n_frames_of_current_speaker < frames_per_speaker):
                print(file_index, end="\r")
                y_, sr = librosa.load(
                    self.dataset.filepath(speaker_index + start_at_speaker, file_index + start_at_file))

                y_ = AudioPreprocessor.remove_noise(y=y_, sr=sr)
                y_ = AudioPreprocessor.remove_silence(y=y_)
                frames = AudioPreprocessor.create_frames(y=y_, frame_size=500, overlap=100)
                frames = AudioPreprocessor.window_frames(frames=frames)
                n_frames_of_current_speaker += len(frames)

                features, n_features = FeatureExtraction.extract_features(frames, sr)

                all_speakers[speaker_index] = all_speakers[speaker_index] + features

                file_index += 1
            print()

        X = np.zeros((total_input_chunks, n_features*20))
        y = np.zeros(total_input_chunks, dtype='uint8')

        for speaker_index in range(0, n_speaker):
            for chunk_index in range(0, nn_input_chunks_per_speaker):

                input_chunk_list = []
                for frame_index in range(0, 20):
                    input_chunk_list.append(
                        (all_speakers[speaker_index][20*chunk_index+frame_index]))

                X[speaker_index * nn_input_chunks_per_speaker + chunk_index] = np.concatenate(input_chunk_list)
                y[speaker_index * nn_input_chunks_per_speaker + chunk_index] = speaker_index

        if (len(X) != 0 and len(y) != 0):
            self.nn_data_is_created = True

        self.nn_data = (X, y)

    def unison_shuffled_copies(self, a, b):
        assert len(a) == len(b)
        p = np.random.permutation(len(a))
        return a[p], b[p]

    def create_model(self):

        if (not self.nn_data_is_created):
            print("Error: First create nn data with create_nn_data()")
            return

        test_accuracy_achieved = False
        while (not test_accuracy_achieved):

            X, y = self.nn_data
            X, y = self.unison_shuffled_copies(X, y)
            self.nn_data = (X, y)

            # model takes 20 frames a n_features coefficients
            model = tf.keras.Sequential([
                tf.keras.layers.Flatten(input_shape=[self.n_features*20]),
                tf.keras.layers.Dense(16, activation=tf.nn.relu),
                tf.keras.layers.Dense(16, activation=tf.nn.relu),
                tf.keras.layers.Dense(self.n_speaker, activation=tf.nn.softmax)
            ])

            model.compile(optimizer=tf.optimizers.Adam(), loss='sparse_categorical_crossentropy', metrics=['accuracy'])

            model.fit(X[int(5*self.total_input_chunks/6):], y[int(5 * self.total_input_chunks/6):], epochs=1000, verbose=0)  # type: ignore

            test_loss, test_acc = model.evaluate(X[-int(self.total_input_chunks/6):], y[-int(self.total_input_chunks/6):])

            if (test_acc > 0.9):
                test_accuracy_achieved = True
                self.model = model
                print(f"Model accuracy achieved: {test_acc}")
            else: 
                print("Model accuracy not achieved, retrying...")

        self.model_is_created = True

    def evaluate_model_with_example(self, speaker_index, file_index):

        X, y = self.nn_data

        if (not self.model_is_created or self.n_speaker == None or len(X) == 0 or len(y) == 0):
            print("Error: First create model with create_model()")
            return

        test_loss, test_acc = self.model.evaluate(X[-int(self.total_input_chunks/6):], y[-int(self.total_input_chunks/6):])

        print(f"Test accuracy: {test_acc}")
        print(f"Test loss: {test_loss}")

        y_, sr = librosa.load(self.dataset.filepath(speaker_index, file_index))

        y_ = AudioPreprocessor.remove_noise(y=y_, sr=sr)
        y_ = AudioPreprocessor.remove_silence(y=y_)
        frames = AudioPreprocessor.create_frames(y=y_, frame_size=500, overlap=100)
        frames = AudioPreprocessor.window_frames(frames=frames)

        mfccs, n_features = FeatureExtraction.extract_features(frames, sr)

        X = np.zeros((int(len(mfccs)/20), n_features*20))

        for chunk_index in range(0, int(len(mfccs)/20)):
            input_chunk_list = []
            for frame_index in range(0, 20):
                input_chunk_list.append((mfccs[20*chunk_index+frame_index]))
            X[chunk_index] = np.concatenate(input_chunk_list)

        pred = self.model.predict(X)
        result = []

        for speaker_i in range(0, self.n_speaker):
            print(
                f"Speaker {speaker_i + self.start_at_speaker}: {np.count_nonzero(np.argmax(pred, axis=1) == speaker_i)}")
            result.append({
                "speaker": speaker_i + self.start_at_speaker,
                "count": np.count_nonzero(np.argmax(pred, axis=1) == speaker_i)
            })
