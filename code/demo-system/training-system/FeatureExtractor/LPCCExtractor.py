from FeatureExtractor.ExtractorInterface import ExtractorInterface
from FeatureExtractor.LPCExtractor import LPCExtractor
from scipy.signal import lfilter
import numpy as np

class LPCCExtractor(ExtractorInterface):
    # source: http://www.practicalcryptography.com/miscellaneous/machine-learning/tutorial-cepstrum-and-lpccs/
    def calculate_features(self, frames, sr, order, multiprocessing=False):

        for frame in frames:
            frame = frame / np.max(np.abs(frame))

        lpc_extractor = LPCExtractor()
        lpc_coefficients = lpc_extractor.calculate_features(frames, sr, order)
        lpcc_coefficients = []
        

        for i in range(len(lpc_coefficients)):
            e, _ = lfilter(np.append(0, -1*lpc_coefficients[i]), [1], frames[i], zi=np.zeros(order))
            gain = np.sqrt(np.mean(e**2))

            lpc_vector = np.append(1, lpc_coefficients[i] / np.max(np.abs(lpc_coefficients[i])))
            lpcc_vector = np.zeros(order)
            # Calculate the cepstral coefficients
            # n = 0 -> ln(gain)
            lpcc_vector[0] = np.log(gain)

            # 0 < n <= order -> sum from k=1 to k=n-1 of (k/n * c(k) * a(n-k)) + a(n)
            for n in range(1, order):
                lpcc_vector[n] = lpc_vector[n] + sum((k/n) * lpcc_vector[k] * lpc_vector[n-k] for k in range(1, n-1))

            lpcc_coefficients.append(lpcc_vector)
            
        return lpcc_coefficients