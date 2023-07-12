"""
 @file ResultEvaluation.py
 @section authors
  - Henry Schuler
"""
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
import numpy as np
import os
import json
import copy

def get_config_id_without_features():
    """
    @brief Searches for all configs with no parameters and returns their ids in order to be removed.


    """
    configs = []
    with open(os.path.join(os.path.dirname(__file__), "Configs", "config.json"), "r") as json_file:
        configs = json.load(json_file)

    id_list = []

    for config in configs:
        if (config["lpc_weight"] == 0 and
            config["mfcc_weight"] == 0 and
            config["lpcc_weight"] == 0 and
            config["delta_mfcc_weight"] == 0):
            id_list.append(config["id"])

    return id_list


def get_config_id_from_features(arguments):
    """
    @brief Helper function to determine the config id from a given set of arguments (CSV)

    Parameters : 
        @param arguments => arguments in order of the csv results file

    """
    # load configs
    configs = []
    with open(os.path.join(os.path.dirname(__file__), "Configs", "configs.json"), "r") as json_file:
        configs = json.load(json_file)

    for config in configs:
        if (int(arguments[2]) == config["amount_of_frames"] and
            int(arguments[3]) == config["size_of_frame"] and 
            int(arguments[4]) == config["lpc_weight"] and
            int(arguments[5]) == config["lpc_order"] and
            int(arguments[6]) == config["mfcc_weight"] and
            int(arguments[7]) == config["mfcc_order"] and
            int(arguments[8]) == config["lpcc_weight"] and
            int(arguments[9]) == config["lpcc_order"] and
            int(arguments[10]) == config["delta_mfcc_weight"] and
            int(arguments[11]) == config["delta_mfcc_order"]):
            return config["id"]
    
def write_data(data_list, config_id, abs_accuracy, rel_accuracy, min_rel_distance, min_rel_distance_speaker_id, correct_asserted_test_samples, correct_asserted_absolute, false_asserted_absolute, not_asserted_absolute, value_count):
    """
    @brief Saves the given values to the data_list for displaying as a graph

    Parameters : 
        @param data_list => array containing the chart data
        @param config_id => config id for the given data
        @param abs_accuracy => calculated absolute accuracy
        @param rel_accuracy => calculated relative accuracy
        @param min_rel_distance => minimal distance to the second place
        @param min_rel_distance_speaker_id => speaker id of the second place
        @param correct_asserted_test_samples => amount of correct asserted samples (relative, closed set)
        @param correct_asserted_absolute => amount of correct asserted samples (absolute, open set, threshold)
        @param false_asserted_absolute => amount of false asserted samples (absolute, open set, threshold)
        @param not_asserted_absolute => amount of not asserted samples (absolute, open set, threshold)
        @param value_count => amount of asserted samples

    """
    ### absolute accuracy

    for i in range(3):
        if config_id not in data_list['absolute_accuracy'][i]['x']:
            data_list['absolute_accuracy'][i]['x'].append(config_id)
            data_list['absolute_accuracy'][i]['y'].append(abs_accuracy / value_count)
            break

    ### relative accuracy

    for i in range(3):
        if config_id not in data_list['relative_accuracy'][i]['x']:
            data_list['relative_accuracy'][i]['x'].append(config_id)
            data_list['relative_accuracy'][i]['y'].append(rel_accuracy / value_count)
            break

    ### min relative distance
    
    for i in range(3):
        if config_id not in data_list['min_relative_distance'][i]['x']:
            data_list['min_relative_distance'][i]['x'].append(config_id)
            data_list['min_relative_distance'][i]['y'].append(min_rel_distance)
            data_list['min_relative_distance_speaker_id'][i]['x'].append(config_id)
            data_list['min_relative_distance_speaker_id'][i]['y'].append(min_rel_distance_speaker_id)
            break

    ### correct asserted test samples
    for i in range(3):
        if config_id not in data_list['correct_asserted_test_samples_per_nn'][i]['x']:
            data_list['correct_asserted_test_samples_per_nn'][i]['x'].append(config_id)
            data_list['correct_asserted_test_samples_per_nn'][i]['y'].append(correct_asserted_test_samples / value_count)
            break

    for i in range(3):
        if config_id not in data_list['correct_asserted_absolute'][i]['x']:
            data_list['correct_asserted_absolute'][i]['x'].append(config_id)
            data_list['correct_asserted_absolute'][i]['y'].append(correct_asserted_absolute / value_count)
            break

    for i in range(3):
        if config_id not in data_list['false_asserted_absolute'][i]['x']:
            data_list['false_asserted_absolute'][i]['x'].append(config_id)
            data_list['false_asserted_absolute'][i]['y'].append(false_asserted_absolute / value_count)
            break

    for i in range(3):
        if config_id not in data_list['not_asserted_absolute'][i]['x']:
            data_list['not_asserted_absolute'][i]['x'].append(config_id)
            data_list['not_asserted_absolute'][i]['y'].append(not_asserted_absolute / value_count)
            break
    
def compare_nn_accuracy_per_config():
    """
    @brief Calculates different metrics and displays them as a graph


    """
    """
    The data value is a template for displaying bar data for three nn per config
    """
    data = [
        {
            'x': [],
            'y': [],
            'name': 'NN 0',
            'type': 'bar'
        },
        {
            'x': [],
            'y': [],
            'name': 'NN 1',
            'type': 'bar'
        },
        {
            'x': [],
            'y': [],
            'name': 'NN 2',
            'type': 'bar'
        }
    ]

    data_list = {
        'absolute_accuracy': copy.deepcopy(data),
        'relative_accuracy': copy.deepcopy(data),
        'min_relative_distance': copy.deepcopy(data),
        'min_relative_distance_speaker_id': copy.deepcopy(data),
        'min_relative_distance_speaker_id_amount': copy.deepcopy(data),
        'correct_asserted_test_samples_per_nn': copy.deepcopy(data),
        'correct_asserted_absolute': copy.deepcopy(data),
        'false_asserted_absolute': copy.deepcopy(data),
        'not_asserted_absolute': copy.deepcopy(data),
        'absolute_accuracy_per_config': [{'x': [], 'y': [], 'name': 'absolute_accuracy', 'type': 'bar'}],
        'correct_asserted_per_config': [{'x': [], 'y': [], 'name': 'correct_asserted', 'type': 'bar'}],
        'false_asserted_per_config': [{'x': [], 'y': [], 'name': 'false_asserted', 'type': 'bar'}],
        'not_asserted_per_config': [{'x': [], 'y': [], 'name': 'not_asserted', 'type': 'bar'}],
    }

    # Read results.csv
    # with open(os.path.join(os.path.dirname(__file__), "results.csv"), "r") as csv_file:
    with open("/home/scu8bh/Documents/code/sa-hs-lb-jb/code/demo-system/server/TrainingSystem/results_combined.csv", "r") as csv_file:
        lines = csv_file.readlines()
        uuid = ""
        uuid_line = []
        abs_accuracy = 0
        rel_accuracy = 0
        min_rel_distance = 10000
        min_rel_distance_speaker_id = -1
        correct_asserted_test_samples = 0
        correct_asserted_absolute = 0
        false_asserted_absolute = 0
        not_asserted_absolute = 0
        absolute_percent = 0.65
        value_count = 0
        has_one_value = False
        max_config_id=517
        for line in lines:
            arguments = line.split(";")
            if uuid == "":
                uuid = arguments[0]
                uuid_line = arguments
            if uuid != arguments[0]:
                # data collected -> process/save
                # evaluate config id from uuid
                config_id = get_config_id_from_features(uuid_line)

                if has_one_value:
                    print(f"Config {config_id} has 0.0 value")

                if not has_one_value and (config_id == 472 or config_id > 510):
                    write_data(data_list, config_id, abs_accuracy, rel_accuracy, min_rel_distance, min_rel_distance_speaker_id, correct_asserted_test_samples, correct_asserted_absolute, false_asserted_absolute, not_asserted_absolute, value_count)

                # reset values
                uuid = arguments[0]
                uuid_line = arguments
                has_one_value = False
                value_count = 0
                rel_accuracy = 0
                abs_accuracy = 0
                min_rel_distance = 10000
                min_rel_distance_speaker_id = -1
                correct_asserted_test_samples = 0
                correct_asserted_absolute = 0
                false_asserted_absolute = 0
                not_asserted_absolute = 0
            if uuid == arguments[0]:
                speaker_id = int(arguments[12])

                speaker_percent = float(arguments[13 + speaker_id])
                # absolute percentage
                abs_accuracy += speaker_percent

                # relative percentage
                sorted_array = np.sort(np.array(arguments[13:33]))
                rel_distance = 0
                if speaker_percent == float(sorted_array[-1]):
                    rel_distance = speaker_percent - float(sorted_array[-2])
                else:
                    rel_distance = speaker_percent - float(sorted_array[-1])
                rel_accuracy += rel_distance
                
                # min relative distance
                if rel_distance < min_rel_distance:
                    min_rel_distance = rel_distance
                    min_rel_distance_speaker_id = speaker_id

                # correct asserted test samples
                if rel_distance > 0:
                    correct_asserted_test_samples += 1

                if speaker_percent >= absolute_percent:
                    correct_asserted_absolute += 1
                elif speaker_percent < absolute_percent:
                    if float(sorted_array[-1]) >= absolute_percent:
                        false_asserted_absolute += 1
                    else:
                        not_asserted_absolute += 1

                if speaker_percent == 0.0:
                    has_one_value = True
                value_count += 1

            if line == lines[-1]:
                # last evaluation
                config_id = get_config_id_from_features(uuid_line)

                if has_one_value:
                    print(f"Config {config_id} has 0.0 value")

                write_data(data_list, config_id, abs_accuracy, rel_accuracy, min_rel_distance, min_rel_distance_speaker_id, correct_asserted_test_samples, correct_asserted_absolute, false_asserted_absolute, not_asserted_absolute, value_count)

    for speaker_id in range(20):
        data_list['min_relative_distance_speaker_id_amount'][0]['x'].append(speaker_id)
        data_list['min_relative_distance_speaker_id_amount'][0]['y'].append(sum(data_list['min_relative_distance_speaker_id'][i]['y'].count(speaker_id) for i in range(3)))

    # Create datasets that combine the data of all 3 NN per config

    for config_id in range(max_config_id):
        found_items = 0
        acc = 0
        for i in range(3):
            if config_id in data_list['absolute_accuracy'][i]['x']:
                found_items += 1
                acc += data_list['absolute_accuracy'][i]['y'][data_list['absolute_accuracy'][i]['x'].index(config_id)]
        if found_items > 0:
            acc = acc / found_items
            data_list['absolute_accuracy_per_config'][0]['x'].append(config_id)
            data_list['absolute_accuracy_per_config'][0]['y'].append(acc)

    for config_id in range(max_config_id):
        found_items = 0
        acc = 0
        for i in range(3):
            if config_id in data_list['correct_asserted_absolute'][i]['x']:
                found_items += 1
                acc += data_list['correct_asserted_absolute'][i]['y'][data_list['correct_asserted_absolute'][i]['x'].index(config_id)]
        if found_items > 0:
            acc = acc / found_items
            data_list['correct_asserted_per_config'][0]['x'].append(config_id)
            data_list['correct_asserted_per_config'][0]['y'].append(acc)

    for config_id in range(max_config_id):
        found_items = 0
        acc = 0
        for i in range(3):
            if config_id in data_list['false_asserted_absolute'][i]['x']:
                found_items += 1
                acc += data_list['false_asserted_absolute'][i]['y'][data_list['false_asserted_absolute'][i]['x'].index(config_id)]
        if found_items > 0:
            acc = acc / found_items
            data_list['false_asserted_per_config'][0]['x'].append(config_id)
            data_list['false_asserted_per_config'][0]['y'].append(acc)

    for config_id in range(max_config_id):
        found_items = 0
        acc = 0
        for i in range(3):
            if config_id in data_list['not_asserted_absolute'][i]['x']:
                found_items += 1
                acc += data_list['not_asserted_absolute'][i]['y'][data_list['not_asserted_absolute'][i]['x'].index(config_id)]
        if found_items > 0:
            acc = acc / found_items
            data_list['not_asserted_per_config'][0]['x'].append(config_id)
            data_list['not_asserted_per_config'][0]['y'].append(acc)


    layout = {
        'xaxis': {'title': 'configID'},
        'yaxis': {'title': 'Percentage'}
    }

    app = Dash(__name__)

    app.layout = html.Div([
        html.H4('Interactive plot with custom data source'),
        dcc.Graph(id="graph"),
        html.P("Type"),
        dcc.RadioItems(['absolute_accuracy', 'relative_accuracy', 'min_relative_distance', 'min_relative_distance_speaker_id', 'min_relative_distance_speaker_id_amount', 'correct_asserted_test_samples_per_nn', 'correct_asserted_absolute', 'false_asserted_absolute', 'not_asserted_absolute', 'absolute_accuracy_per_config', 'correct_asserted_per_config', 'false_asserted_per_config', 'not_asserted_per_config'], value='absolute_accuracy', id="type_value"),
    ])


    @app.callback(
        Output("graph", "figure"), 
        Input("type_value", "value"))
    def update_bar_chart(type_value):
        """
        @brief Refresh function for changing the selected metric in the web graph view.

        Parameters : 
            @param type_value => selected graph index

        """
        this_data = {'data': data_list[type_value], 'layout': layout}
        fig = go.Figure(
            data=this_data,
            # layout_title_text="Average absolute accuracy"
            # layout_title_text="Correct asserted test samples (absolute 65%)"
            # layout_title_text="False asserted test samples (absolute 65%)"
            layout_title_text="Not asserted test samples (absolute 65%)"
        )
        return fig

    app.run_server(debug=True)
                
if __name__ == "__main__":
    compare_nn_accuracy_per_config()
