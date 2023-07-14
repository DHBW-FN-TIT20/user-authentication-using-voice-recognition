"""
 @file TestResult.py
 @section authors
  - Lukas Braun
"""
class TestResult:
    """
    @brief Data class for storing test results


    """
    def __init__(self, speaker_id: int, sample_id: int, correspondence):
        """
        @brief Initializes the object with the given values

        Parameters : 
            @param speaker_id : int => id of the speaker from the sample
            @param sample_id : int => id of the sample
            @param correspondence : dict[int,float] => calculated correspondence of the neural network

        """
        self.speaker_id: int = speaker_id #expected speaker
        self.sample_id: int = sample_id
        self.correspondence = correspondence