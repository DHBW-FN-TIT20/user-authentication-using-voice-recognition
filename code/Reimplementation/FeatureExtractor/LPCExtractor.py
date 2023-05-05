from FeatureExtractor.ExtractorInterface import ExtractorInterface
from multiprocessing import Pool
import librosa

def calculate_lpc(frame, sr, order):
    return librosa.lpc(y=frame, order=order)[1:]

class LPCExtractor(ExtractorInterface):
    def calculate_features(self, frames, sr, order, multiprocessing=False):

        lpc_coefficients = []
        for frame in frames:
            lpc_coefficients.append(calculate_lpc(frame, sr, order))

        return lpc_coefficients