"""
 @file FeatureExtractor.py
 @section authors
  - 
"""
from FeatureExtractor.LPCExtractor import LPCExtractor
from FeatureExtractor.LPCCExtractor import LPCCExtractor
from FeatureExtractor.MFCCExtractor import MFCCExtractor

import librosa
import numpy as np
from enum import Enum

class Feature(Enum):
    """
    @brief Enum for accessing the available feature types
    """
    LPC = 0
    LPCC = 1
    MFCC = 2

class FeatureExtractor:
    """
    @brief Class implementing methods for extracting features


    """
    def __init__(self, frames, sr):
        """
        @brief Initializes the class with standard values

        Parameters : 
            @param frames => frames to work with
            @param sr => sampling rate

        """
        self.frames = frames
        self.sr = sr
        self.extractors = [
            LPCExtractor(),
            LPCCExtractor(),
            MFCCExtractor()
        ]
        self.last_feature_count = 0

    def extract_features(self, feature_list, multiprocessing=False): #(*@\label{line:extract_features}@*)
        """
        @brief Function to extract a set of features

        Parameters :
            @param feature_list => List of all features to extract. Format: ((Feature, int, int[])[]): 2D List of Features (enum) + order (int) + deltas (int[]) lists to extract #(*@\label{line:feature_list_info}@*)
            @param multiprocessing = False => enables multiprocessing for supported features

        """
        feature_set = None
        
        if len(feature_list) > 0:
            for feature_info in feature_list:
                features = self.extractors[feature_info[0].value].calculate_features(self.frames, self.sr, feature_info[1], multiprocessing=multiprocessing)
                
                for delta in feature_info[2]:
                    if delta == 0:
                        delta_features = features
                    else:
                        delta_features = librosa.feature.delta(np.array(features), order=delta, mode='nearest')
                        
                    if feature_set is None:
                        feature_set = np.array(delta_features)
                    else:
                        np.concatenate((feature_set, delta_features), axis=1)
            
            feature_set = feature_set.tolist()
            self.last_feature_count = len(feature_set[0])
        
        return feature_set
    
    def get_last_feature_count(self):
        """
        @brief Getter for the last_feature_count variable
        
        """
        return self.last_feature_count