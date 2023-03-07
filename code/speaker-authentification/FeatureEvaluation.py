import numpy as np
import librosa
import os
import tensorflow as tf
from tensorflow import keras
from FeatureExtractor.FeatureExtractor import FeatureExtractor, Feature
from DatasetHandler import DatasetHandler
from AudioPreprocessor.AudioPreprocessor import AudioPreprocessor

class FeatureEvaluator:
    def __init__(self, dataset_basepath):
        self.n_features = 0
        self.dataset = DatasetHandler(dataset_basepath)
        self.nn_data = ([], [])
        self.total_input_chunks = 0
        self.n_speaker = None
        self.nn_data_is_created = False
        self.model_is_created = False
        self.start_at_speaker = 0
        self.frames_per_chunk = 0
        self.feature_list = []
        self.dense_layer_sizes = []
        self.epochs = 0

    def create_nn_data(self, total_input_chunks, frames_per_chunk, n_speaker, start_at_speaker = 0, start_at_file = 0, feature_list = [[Feature.MFCC, 13, [1, 2]], [Feature.LPC, 12, []]]):
        # [Feature.MFCC, 13, [1, 2]], # MFCC  -> order=13 -> delta 1 and 2
        # [Feature.LPC, 12, []]       # LPC   -> order=12 -> no deltas
        self.total_input_chunks = total_input_chunks
        self.n_speaker = n_speaker
        self.start_at_speaker = start_at_speaker
        nn_input_chunks_per_speaker = int(total_input_chunks/n_speaker)
        self.frames_per_chunk = frames_per_chunk
        frames_per_speaker = nn_input_chunks_per_speaker * self.frames_per_chunk
        self.feature_list = feature_list

        all_speakers = []
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

                extractor = FeatureExtractor(frames, sr)
                features = extractor.extract_features(feature_list)
                self.n_features = extractor.get_last_feature_count()

                all_speakers[speaker_index] = all_speakers[speaker_index] + features

                file_index += 1
            print()
        
        X = np.zeros((total_input_chunks, self.frames_per_chunk*self.n_features))
        y = np.zeros(total_input_chunks, dtype='uint8')

        for speaker_index in range(0, n_speaker):
            for chunk_index in range(0, nn_input_chunks_per_speaker):

                input_chunk_list = []
                for frame_index in range(0, self.frames_per_chunk):
                    input_chunk_list.append(
                        (all_speakers[speaker_index][chunk_index*self.frames_per_chunk+frame_index]))

                X[speaker_index * nn_input_chunks_per_speaker + chunk_index] = np.concatenate(input_chunk_list)
                y[speaker_index * nn_input_chunks_per_speaker + chunk_index] = speaker_index

        if (len(X) != 0 and len(y) != 0):
            self.nn_data_is_created = True

        self.nn_data = (X, y)

    def unison_shuffled_copies(self, a, b):
        assert len(a) == len(b)
        p = np.random.permutation(len(a))
        return a[p], b[p]

    def create_model(self, dense_layer_sizes:list=[], epochs:int=0, verbose:int=1):

        if (not self.nn_data_is_created):
            print("Error: First create nn data with create_nn_data()")
            return

        # process parameters
        if (len(dense_layer_sizes) == 0):
            dense_layer_sizes = [16, 16]
        self.dense_layer_sizes = dense_layer_sizes
        if (epochs == 0):
            epochs = 1000
        self.epochs = epochs

        test_accuracy_achieved = False
        while (not test_accuracy_achieved):

            tf.keras.backend.clear_session()

            dense_layers = []
            for dense_layer_size in dense_layer_sizes:
                dense_layers.append(tf.keras.layers.Dense(dense_layer_size, activation=tf.nn.relu))

            X, y = self.nn_data
            X, y = self.unison_shuffled_copies(X, y)
            self.nn_data = (X, y)

            model = tf.keras.Sequential([
                tf.keras.layers.Flatten(input_shape=[self.n_features*self.frames_per_chunk]),
                *dense_layers,
                tf.keras.layers.Dense(self.n_speaker, activation=tf.nn.softmax)
            ])

            model.compile(optimizer=tf.optimizers.Adam(), loss='sparse_categorical_crossentropy', metrics=['accuracy'])

            model.fit(X[int(5*self.total_input_chunks/6):], y[int(5 * self.total_input_chunks/6):], epochs=epochs, verbose=0) # type: ignore

            test_loss, test_acc = model.evaluate(X[-int(self.total_input_chunks/6):], y[-int(self.total_input_chunks/6):], verbose=verbose) # type: ignore
            
            if (test_acc > 0.9):
                test_accuracy_achieved = True
                self.model = model
                if verbose == 1: print(f"Model accuracy achieved: {test_acc}")
            else: 
                if verbose == 1: print("Model accuracy not achieved, retrying...")

        self.model_is_created = True

    def evaluate_model_with_example(self, speaker_index, file_index, verbose: int=1):

        X, y = self.nn_data

        if (not self.model_is_created or self.n_speaker == None or len(X) == 0 or len(y) == 0):
            
            if verbose == 1: print("Error: First create model with create_model()")
            return

        if verbose == 1:
            test_loss, test_acc = self.model.evaluate(X[-int(self.total_input_chunks/6):], y[-int(self.total_input_chunks/6):])

            print(f"Test accuracy: {test_acc}")
            print(f"Test loss: {test_loss}")

        y_, sr = librosa.load(self.dataset.filepath(speaker_index, file_index))

        y_ = AudioPreprocessor.remove_noise(y=y_, sr=sr)
        y_ = AudioPreprocessor.remove_silence(y=y_)
        frames = AudioPreprocessor.create_frames(y=y_, frame_size=500, overlap=100)
        frames = AudioPreprocessor.window_frames(frames=frames)

        extractor = FeatureExtractor(frames, sr)
        features = extractor.extract_features(self.feature_list)
        n_features = extractor.get_last_feature_count()

        X = np.zeros((int(len(features)/self.frames_per_chunk), n_features*self.frames_per_chunk))

        for chunk_index in range(0, int(len(features)/self.frames_per_chunk)):
            input_chunk_list = []
            for frame_index in range(0, self.frames_per_chunk):
                input_chunk_list.append((features[chunk_index*self.frames_per_chunk+frame_index]))
            X[chunk_index] = np.concatenate(input_chunk_list)

        pred = self.model.predict(X, verbose=verbose) # type: ignore
        result = []
        hits_correct = 0
        hits_incorrect = 0
        hits_on_closest_incorrect_speaker = 0

        for speaker_i in range(0, self.n_speaker):
            if verbose == 1: print(f"Speaker {speaker_i + self.start_at_speaker}: {np.count_nonzero(np.argmax(pred, axis=1) == speaker_i)}")
            hits_on_speaker_i = np.count_nonzero(np.argmax(pred, axis=1) == speaker_i)
            result.append({
                "speaker": speaker_i + self.start_at_speaker,
                "count": hits_on_speaker_i
            })
            if (speaker_i + self.start_at_speaker == speaker_index):
                hits_correct += hits_on_speaker_i
            else:
                hits_incorrect += hits_on_speaker_i
                if (hits_on_speaker_i > hits_on_closest_incorrect_speaker):
                    hits_on_closest_incorrect_speaker = hits_on_speaker_i

        # difference between the hits on the correct speaker and the hits on closest incorrect speaker
        # the bigger the difference, the more confident the model is in its prediction
        diff_correct_closest_incorrect = hits_correct - hits_on_closest_incorrect_speaker
        if verbose == 1:
            print(f"Correct: {hits_correct}, Incorrect: {hits_incorrect}")
            print(f"Diff correct - closest incorrect: {diff_correct_closest_incorrect}")

        return result, hits_correct, hits_incorrect, diff_correct_closest_incorrect


    def evaluate_extensively(self, speaker_indices: list, file_indices: list, rebuild_model_every_iteration=True, verbose:int=0):

        if (not self.model_is_created or self.n_speaker == None):
            print("Error: First create model with create_model()")
            return

        result = []
        hits_correct = 0
        hits_incorrect = 0
        diff_correct_closest_incorrect = 0

        for speaker_index in speaker_indices:
            for file_index in file_indices:
                print(f"Evaluating speaker {speaker_index} and file {file_index} (Correct: {hits_correct}, Incorrect: {hits_incorrect})", end="\r")
                
                # TODO: check if working correctly (maybe out of memory)
                if rebuild_model_every_iteration:
                    self.create_model(dense_layer_sizes=self.dense_layer_sizes, epochs=self.epochs, verbose=verbose)

                evaluation_result = self.evaluate_model_with_example(speaker_index, file_index, verbose=verbose)
                if (evaluation_result == None):
                    print(f"Error: Evaluation of speaker {speaker_index} and file {file_index} failed")
                    return
                r, c, i, d = evaluation_result
                result.append(r)
                hits_correct += c
                hits_incorrect += i
                diff_correct_closest_incorrect += d

        diff_correct_closest_incorrect /= len(speaker_indices) * len(file_indices)

        print(end="\x1b[2K") # clear line
        print("Evaluation finished")
        print(f"Correct: {hits_correct}, Incorrect: {hits_incorrect}")
        print(f"Average difference between correct and closest incorrect: {diff_correct_closest_incorrect}")

