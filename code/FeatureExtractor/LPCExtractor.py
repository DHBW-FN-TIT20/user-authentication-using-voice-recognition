from FeatureExtractor.ExtractorInterface import ExtractorInterface

import librosa

class LPCExtractor(ExtractorInterface):
    def calculate_features(self, frames, sr, order):
        lpc_coefficients = []
        
        for frame in frames:
            lpc_coefficients.append(librosa.lpc(y=frame, order=order)[1:]) #(*@\label{line:removeLPC0}@*)
            
        return lpc_coefficients