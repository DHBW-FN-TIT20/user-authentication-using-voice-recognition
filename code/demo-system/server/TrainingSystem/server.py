from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
import numpy as np
import os
from DatasetHandler import DatasetHandler
from FeatureExtractor.FeatureExtractor import FeatureExtractor, Feature
from AudioPreprocessor import AudioPreprocessor
import librosa

def extract_features(file_path, speaker_id, feature_list, limit_frames=True, multiprocessing=False):
    audio_preprocessor = AudioPreprocessor()

    # load and preprocess file
    y, sr = librosa.load(file_path)
    y = audio_preprocessor.remove_silence(y)
    y = audio_preprocessor.remove_noise(y, sr)

    frames = audio_preprocessor.create_frames(y=y, frame_size=int(600), overlap=int(0.5 * int(600)))

    if limit_frames:
        if len(frames) < 15000:
            print(f"Warning: Not enough frames for speaker {speaker_id}.")
        else:
            frames = frames[0:15000]
    
    windowed_frames = audio_preprocessor.window_frames(frames=frames, window_function=np.hanning)

    # extract features
    extractor = FeatureExtractor(frames=windowed_frames, sr=sr)
    features = extractor.extract_features(feature_list=feature_list, multiprocessing=multiprocessing)

    # cluster 10 frames into 1
    clustered_features = []
    for i in range(int(len(features) / 10)):
        clustered_features.append(np.concatenate((features[i*10:(i+1)*10]), axis=0))

    return clustered_features

def generate_test_data(speaker_id: int, sample_id: int):

    ds_handler = DatasetHandler(os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "audio_dataset"))
    test_X = []
    test_y = []
    test_file_path = ds_handler.get_validation_file_path(speaker_id, sample_id)
    feature_list = [[Feature.MFCC, 20, [0,1]]]
    features = extract_features(
        file_path=test_file_path,
        speaker_id=speaker_id,
        feature_list=feature_list,
        limit_frames=False,
        multiprocessing=False
    )

    if features is not None:
        test_X.append(features)
        test_y.append(np.full(len(features), speaker_id))

    return test_X, test_y

neural_network: tf.keras.Model = tf.keras.models.load_model(os.path.join(os.path.dirname(__file__), "final-nn-serialized", "neural_network.h5"))  # type: ignore

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET", "POST"])
def hello():

    # get the url parameters
    args = request.args
    speaker_id = args["speaker_id"]
    sample_id = args["sample_id"]
    selected_speaker_id = args["selected_speaker_id"]

    # generate test data and predict the selected speaker
    test_data_x, test_data_y = generate_test_data(int(speaker_id), int(sample_id))
    prediction = neural_network.predict(np.asarray(test_data_x[0]))
    correspondence = {}
    for id in range(20):
        correspondence[f"{id}"] = np.count_nonzero(np.argmax(prediction, axis=1) == id) / len(prediction)
    absolute_accuracy_of_selected_speaker = correspondence[f"{selected_speaker_id}"]

    # return the result
    result = {
        "absolute_accuracy_of_selected_speaker": absolute_accuracy_of_selected_speaker,
        "is_authenticated": absolute_accuracy_of_selected_speaker > 0.7,
    }
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=False, host='localhost', port=5500)