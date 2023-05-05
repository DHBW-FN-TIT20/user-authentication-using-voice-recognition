from FeatureExtractor.ExtractorInterface import ExtractorInterface
from multiprocessing import Pool
import numpy as np
import librosa

def calculate_mfcc(frame, sr, order):
    mfcc = librosa.feature.mfcc(y=frame, sr=sr, n_mfcc=order, n_fft=1024, hop_length=512)
    mfcc_of_frame = np.mean(mfcc.T, axis=0)
    return mfcc_of_frame

class MFCCExtractor(ExtractorInterface):
    def calculate_features(self, frames, sr, order, multiprocessing=False):

        if multiprocessing:

            with Pool(8) as p:
                mfccs = p.starmap(calculate_mfcc, [(frame, sr, order) for frame in frames])

            return mfccs

        else:

            mfccs = []
            for frame in frames:
                mfccs.append(calculate_mfcc(frame, sr, order))

            return mfccs