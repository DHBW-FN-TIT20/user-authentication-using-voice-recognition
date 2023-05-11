from FeatureExtractor.LPCExtractor import LPCExtractor
from FeatureExtractor.LPCCExtractor import LPCCExtractor
from FeatureExtractor.MFCCExtractor import MFCCExtractor

import librosa
import os
import json
import pickle
import numpy as np
from enum import Enum

class Feature(Enum):
    LPC = 0
    LPCC = 1
    MFCC = 2

class FeatureExtractor:
    def __init__(self, frames, sr):
        self.frames = frames
        self.sr = sr
        self.extractors = [
            LPCExtractor(),
            LPCCExtractor(),
            MFCCExtractor()
        ]
        self.last_feature_count = 0

    def dump_features(self, config, feature_set, featureIndex, spaker_id, feature_order, testflag: bool, test_sample_id=-1):
        # create a new folder for the feature_set
        # Define the base directory for the folders
        base_dir = "C:/Code/sa-hs-lb-jb/code/Reimplementation/datadump/"

        # Find the next available folder ID by iterating over existing folders
        folder_id = 1
        while os.path.exists(os.path.join(base_dir + str(folder_id))):
            folder_id += 1

        # Create the new folder with the unique ID
        new_folder_path = base_dir + str(folder_id) + "/"
        os.makedirs(new_folder_path)

        filepath = new_folder_path + "feature_set.pickle"
        # save feature_set to a file
        with open(filepath, 'wb') as f:
            pickle.dump(feature_set, f)

        # save config in same folder as json
        # Create New Config
        # featureIndex --> 0 = LPC, 1 = LPCC, 2 = MFCC

        dump_config ={
            "speaker_id": spaker_id,
            "test_sample_id": test_sample_id,
            "testflag": testflag,
            "amount_of_frames": config["amount_of_frames"],
            "size_of_frame": config["size_of_frame"],
            "FeatureType": featureIndex,
            "FeatureOrder": feature_order,
        }
        with open(new_folder_path + "config.json", "w") as f:
            json.dump(dump_config, f, indent=4) 

    def load_features(self, config, featureIndex, speaker_id, feature_order, testflag: bool, test_sample_id=-1):
        # check if feature is calculated local
        # the datasets are stored in the datadump folder
        # foreach folder in dataset read the config
        # if the config is the same as the current config
        # load the feature_set from the folder

        base_dir = "C:\Code\sa-hs-lb-jb\code\Reimplementation\datadump"
        feature_set = None
        # Find the next available folder ID by iterating over existing folders
        for dir_name in os.listdir(base_dir):
            dir_path = os.path.join(base_dir, dir_name)
            # read config.json
            with open(dir_path + "/config.json", "r") as f:
                config_json = json.load(f)
                # check if config is useful
                # featureIndex --> 0 = LPC, 1 = LPCC, 2 = MFCC
                if (config_json["FeatureType"] == featureIndex and
                config_json["amount_of_frames"] == config["amount_of_frames"] and
                config_json["size_of_frame"] == config["size_of_frame"] and
                config_json["speaker_id"] == speaker_id and
                config_json["testflag"] == testflag and
                config_json["test_sample_id"] == test_sample_id and
                config_json["FeatureOrder"] == feature_order
                ):
                    # load feature_set from file
                    with open(dir_path+ "/feature_set.pickle", "rb") as f:
                        feature_set = pickle.load(f)
                        print(f"Loaded feature_set from datadump {dir_path} for featureIndex {featureIndex}")
                        return feature_set

    def extract_features(self,config, feature_list, speaker_id, test_sample_id, testflag = False, multiprocessing=False, dump_test_flag = False): #(*@\label{line:extract_features}@*)
        """_summary_

        Args:
            feature_list ((Feature, int, int[])[]): 2D List of Features (enum) + order (int) + deltas (int[]) lists to extract #(*@\label{line:feature_list_info}@*)

        Returns:
            NDArray[]: Array of requested features for each frame
        """
        feature_set = None
        
        if len(feature_list) > 0:
            for feature_info in feature_list:
                # Feature Dump Test
                if dump_test_flag == True:
                    # Calculate Features
                    print(f"DUMP TEST for feature {feature_info[0].value}, Speaker: {speaker_id}, TestSampleId: {test_sample_id}")
                    calculated_features = self.extractors[feature_info[0].value].calculate_features(self.frames, self.sr, feature_info[1], multiprocessing=multiprocessing)
                    # dump features
                    self.dump_features(config, calculated_features, feature_info[0].value, test_sample_id = test_sample_id, feature_order = feature_info[1], spaker_id = speaker_id, testflag = testflag)
                    # load features
                    dumped_features = self.load_features(config, feature_info[0].value, test_sample_id=test_sample_id, feature_order = feature_info[1], speaker_id = speaker_id, testflag = testflag)
                    # compare features
                    if np.array_equal(calculated_features, dumped_features):
                        print(f"Feature Dump Test (Speaker: {speaker_id}, TestSampleId: {test_sample_id}) for Feature {feature_info[0].value} was successful")
                    else:
                        print(f"Feature Dump Test (Speaker: {speaker_id}, TestSampleId: {test_sample_id}) for Feature {feature_info[0].value} was not successful")
                else:
                # check if feature is calculated local
                    features = None
                    features = self.load_features(config, feature_info[0].value, test_sample_id=test_sample_id, feature_order = feature_info[1], speaker_id = speaker_id, testflag = testflag)
                    if features is None:
                        features = self.extractors[feature_info[0].value].calculate_features(self.frames, self.sr, feature_info[1], multiprocessing=multiprocessing)
                        # feature_info[0].value --> 0 = LPC, 1 = LPCC, 2 = MFCC
                        # dump features
                        self.dump_features(config, features, feature_info[0].value, test_sample_id = test_sample_id, feature_order = feature_info[1], spaker_id = speaker_id, testflag = testflag)
                    for delta in feature_info[2]:
                        if delta == 0:
                            delta_features = features
                        else:
                            delta_features = librosa.feature.delta(np.array(features), order=delta, mode='nearest')
                            
                        if feature_set is None:
                            # First Feature --> Create Feature Set
                            feature_set = np.array(delta_features)
                        else:
                            # Append Feature to Feature Set
                            np.concatenate((feature_set, delta_features), axis=1)
            
            feature_set = feature_set.tolist()
            self.last_feature_count = len(feature_set[0])
        return feature_set
    
    def get_last_feature_count(self):
        return self.last_feature_count