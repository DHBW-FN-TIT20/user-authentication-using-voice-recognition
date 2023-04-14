from FeatureExtractor.FeatureExtractor import Feature
from FeatureEvaluator.FeatureEvaluator import FeatureEvaluator

import numpy as np

def main():
    evaluator = FeatureEvaluator("/home/henry/Downloads/archive/50_speakers_audio_data")
    # evaluator = FeatureEvaluator("/Users/johannes/repos/t3000/code/data/50_speakers_audio_data")

    X, y = evaluator.create_dataset([0, 1, 2, 3, 4], [[Feature.LPC, 13, []]], 30, 1000, 500, 100, np.hanning, start_at_file_index=0)
    evaluator.set_model_dataset(X, y)

    X, y = evaluator.create_dataset([0, 1, 2, 3, 4], [[Feature.LPC, 13, []]], 30, 1000, 500, 100, np.hanning, start_at_file_index=15)
    evaluator.set_evaluation_dataset(X, y)

    evaluator.create_nn_model(epochs=1000)

    evaluator.evaluate_model()
    
if __name__ == "__main__":
    main()