from FeatureExtractor.ExtractorInterface import ExtractorInterface
import numpy as np

import librosa

class MFCCExtractor(ExtractorInterface):
    def calculate_features(self, frames, sr, order):
        mfccs = []

        for frame in frames:
            mfcc = librosa.feature.mfcc(y=frame, sr=sr, n_mfcc=order)
            mfcc_of_frame = np.mean(mfcc.T, axis=0)
            mfccs.append(mfcc_of_frame)

        return mfccs