from FeatureExtractor.ExtractorInterface import ExtractorInterface

import librosa

class LPCExtractor(ExtractorInterface):
    def calculateFeatures(self, frames, sr, order):
        lpc_coefficients = []
        
        for frame in frames:
            lpc_coefficients.append(librosa.lpc(y=frame, order=order)[1:])
            
        return lpc_coefficients