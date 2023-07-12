"""!
 @file ExtractorInterface.py
 @section authors
  - 
"""
class ExtractorInterface:
    """!
    @brief An interface for the feature extraction

    """
    def calculate_features(self, frames, sr, order, multiprocessing=False):
        """!
        @brief A function implementing a feature calculation algorithm

        Parameters : 
            @param frames => frames to perform calculation on
            @param sr => sampling rate
            @param order => number of coefficients
            @param multiprocessing = False => Use multiprocessing

        """
        pass