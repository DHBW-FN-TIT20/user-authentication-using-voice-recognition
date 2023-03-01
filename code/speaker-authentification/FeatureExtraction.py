import librosa
import numpy as np

class FeatureExtraction:

    @staticmethod
    def extract_features(frames, sr):
        mfcc, n_features_mfcc = FeatureExtraction.extract_mfcc(frames, sr)

        # concat here if there are more features

        return mfcc, n_features_mfcc


    @staticmethod
    def extract_mfcc(frames, sr):
        n_mfcc = 13

        if len(frames) == 0:
            return [], n_mfcc * 3

        mfccs = []
        for frame in frames:
            mfcc = librosa.feature.mfcc(y=frame, sr=sr, n_mfcc=n_mfcc)
            mfcc_of_frame = np.mean(mfcc.T, axis=0)
            mfccs.append(mfcc_of_frame)

        # calc delta and delta delta mfccs
        mfccs = np.array(mfccs)
        delta_mfccs = librosa.feature.delta(mfccs, order=1, mode='nearest')
        delta_delta_mfccs = librosa.feature.delta(mfccs, order=2, mode='nearest')
        features = np.concatenate((mfccs, delta_mfccs, delta_delta_mfccs), axis=1)
        features = features.tolist()

        return features, n_mfcc * 3

    @staticmethod
    def extract_lpc(frames, sr):
        pass