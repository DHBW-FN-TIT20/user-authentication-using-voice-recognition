from FeatureExtractor.LPCExtractor import LPCExtractor
from FeatureExtractor.MFCCExtractor import MFCCExtractor

import librosa
import numpy as np
from enum import Enum

class Feature(Enum):
    MFCC = 0
    LPC = 1

class FeatureExtractor:
    def __init__(self, frames, sr):
        self.frames = frames
        self.sr = sr
        self.extractors = [
            MFCCExtractor(),
            LPCExtractor()
        ]
        self.last_feature_count = 0

    def extract_features(self, feature_list):
        """_summary_

        Args:
            feature_list ((Feature, int, int[])[]): 2D List of Features (enum) + order (int) + deltas (int[]) lists to extract

        Returns:
            NDArray[]: Array of requested features for each frame
        """
        feature_set = None
        
        for feature_info in feature_list:
            features = self.extractors[feature_info[0].value].calculateFeatures(self.frames, self.sr, feature_info[1])
            if feature_set is None:
                feature_set = np.array(features)
            else:
                np.concatenate((feature_set, np.array(features)), axis=1)
            
            for delta in feature_info[2]:
                delta_features = librosa.feature.delta(np.array(features), order=delta, mode='nearest')
                np.concatenate((feature_set, delta_features), axis=1)
        
        feature_set = feature_set.tolist()
        self.last_feature_count = len(feature_set[0])
        
        return feature_set
    
    def get_last_feature_count(self):
        return self.last_feature_count