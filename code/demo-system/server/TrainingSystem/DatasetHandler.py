"""
 @file DatasetHandler.py
 @section authors
  - Johannes Brandenburger
"""
import os

class DatasetHandler:
    """
    @brief A helper for accessing the file system (audio files)

    """
    def __init__(self, base_path) -> None:
        """
        @brief Initializes the Object

        Parameters : 
            @param base_path => base path to the speaker audio files

        """
        self.base_path = base_path

    def get_training_file_path(self, speaker_index, file_index) -> str:
        """
        @brief Returns the path to a training file for the given parameter values

        Parameters : 
            @param speaker_index => id of the speaker
            @param file_index => index of the file to access

        """
        return os.path.join(self.base_path, f"Speaker{speaker_index:04}", f"Training_Speaker{speaker_index:02}_{file_index:02}.wav")

    def get_validation_file_path(self, speaker_index, file_index) -> str:
        """
        @brief Returns the path to a validation (test) file for the given parameter values

        Parameters : 
            @param speaker_index => id of the speaker
            @param file_index => index of the file to access

        """
        return os.path.join(self.base_path, f"Speaker{speaker_index:04}", f"Validation_Speaker{speaker_index:02}_{file_index:04}.wav")