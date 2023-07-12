"""
 @file LPCExtractor.py
 @section authors
  - Henry Schuler
"""
from FeatureExtractor.ExtractorInterface import ExtractorInterface
from multiprocessing import Pool
import librosa

class LPCExtractor(ExtractorInterface):
    """
    @brief Extractor for LPC features

    """
    def calculate_features(self, frames, sr, order, multiprocessing=False):
        """
        @brief Implements LPC algorithm using librosa function

        """
        lpc_coefficients = []
        for frame in frames:
            lpc_coefficients.append(librosa.lpc(y=frame, order=order)[1:])

        return lpc_coefficients