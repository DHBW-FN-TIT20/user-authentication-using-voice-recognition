import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.subplots as sp
import numpy as np
import os
import json
import copy

def get_config_id_without_features():
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
        This function calculates the average accuracy of all three neural networks for each config.
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
    }

    # Read results.csv
    # with open(os.path.join(os.path.dirname(__file__), "results.csv"), "r") as csv_file:
    with open("/home/henry/Documents/Studium/Studienarbeit/Ergebnisse/without.csv", "r") as csv_file:
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
        for line in lines:
            arguments = line.split(";")
            if uuid == "":
                uuid = arguments[0]
                uuid_line = arguments
            if uuid != arguments[0]:
                # data collected -> process/save
                # evaluate config id from uuid
                config_id = get_config_id_from_features(uuid_line)
                if config_id == 388 or uuid == "0c83734d-aea0-4805-b282-790cc885d6ee":
                    print(388)
                print(value_count)

                if has_one_value:
                    print(f"Config {config_id} has 0.0 value")

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
                if uuid == "06409118-ae25-40f9-82b3-19683673f3ca":
                    print(23)
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

    # for config_id in get_config_id_without_features():
    #     for i in range(3):
    #         data_list['absolute_accuracy'][i]['x'].append(config_id)
    #         data_list['absolute_accuracy'][i]['y'].append(1.0)

    for speaker_id in range(20):
        data_list['min_relative_distance_speaker_id_amount'][0]['x'].append(speaker_id)
        data_list['min_relative_distance_speaker_id_amount'][0]['y'].append(sum(data_list['min_relative_distance_speaker_id'][i]['y'].count(speaker_id) for i in range(3)))



    layout = {
        'xaxis': {'title': 'configID'},
        'yaxis': {'title': 'Percentage'}
    }

    app = Dash(__name__)

    app.layout = html.Div([
        html.H4('Interactive plot with custom data source'),
        dcc.Graph(id="graph"),
        html.P("Type"),
        dcc.RadioItems(['absolute_accuracy', 'relative_accuracy', 'min_relative_distance', 'min_relative_distance_speaker_id', 'min_relative_distance_speaker_id_amount', 'correct_asserted_test_samples_per_nn', 'correct_asserted_absolute', 'false_asserted_absolute', 'not_asserted_absolute'], value='absolute_accuracy', id="type_value"),
    ])


    @app.callback(
        Output("graph", "figure"), 
        Input("type_value", "value"))
    def update_bar_chart(type_value):
        this_data = {'data': data_list[type_value], 'layout': layout}
        fig = go.Figure(
            data=this_data,
            layout_title_text="Not asserted test samples per nn (absolute 65%)"
        )
        return fig

    app.run_server(debug=True)
                

if __name__ == "__main__":
    compare_nn_accuracy_per_config()
    # print(get_config_id_without_features())

    # app = Dash(__name__)


    # app.layout = html.Div([
    #     html.H4('Interactive nn accuracy per config'),
    #     dcc.Graph(id="graph"),
    #     html.P("Config:"),
    #     dcc.Slider(id="config", min=0, max=510, value=0, 
    #             marks={0: '0', 510: '510'})
    # ])

    # @app.callback(
    #     Output("graph", "figure"), 
    #     Input("config", "value"))
     
    # def display_color(config):
    #     data = np.random.normal(mean, std, size=500) # replace with your own data source
    #     fig = px.histogram(data, range_x=[-10, 10])
    #     return fig

    # app.run_server(debug=True)



# data = [
#     {
#         'x': [], 
#         'y': [], 
#         'name': 'Bar 0',
#         'type': 'bar'
#     },
#     {
#         'x': [], 
#         'y': [], 
#         'name': 'Bar 1',
#         'type': 'bar'
#     },
#     {
#         'x': [], 
#         'y': [], 
#         'name': 'Bar 2',
#         'type': 'bar'
#     },
#     {
#         'x': [], 
#         'y': [], 
#         'name': 'Bar 3',
#         'type': 'bar'
#     },
#     {
#         'x': [], 
#         'y': [], 
#         'name': 'Bar 4',
#         'type': 'bar'
#     }
# ]

# # Read results.csv
# with open("/home/henry/Downloads/results.csv", "r") as csv_file:
#     # iterate through lines
#     # uuid = ""
#     # accuracy = 0
#     # value_count = 0
#     # for line in csv_file:
#     #     values = line.split(";")
#     #     if values[0] != uuid:
#     #         if uuid != "":
#     #             # save values
#     #             accuracy = accuracy / value_count
#     #             data[0]['x'].append(uuid)
#     #             data[0]['y'].append(accuracy)
#     #         uuid = values[0]
#     #         accuracy = 0
#     #         value_count = 0

#     #     if values[0] == uuid:
#     #         speaker_id = int(values[12])
#     #         speaker_percent = float(values[13 + speaker_id])
#     #         accuracy += speaker_percent
#     #         value_count += 1

#     # percentage of correct predictions for each speaker
#     uuid = "44e8a2bb-cf16-456d-ba41-3a8bd2e8a97f"
#     for line in csv_file:
#         values = line.split(";")
#         if uuid == "":
#             uuid = values[0]
#         if uuid == values[0]:
#             file_number = int(values[1])
#             speaker_id = int(values[12])
#             speaker_percent = float(values[13 + speaker_id])
#             data[file_number]['x'].append(speaker_id)
#             data[file_number]['y'].append(speaker_percent)
            



# layout = {
#     'xaxis': {'title': 'ID'},
#     'yaxis': {'title': 'Percentage'}
# }

# fig = {'data': data, 'layout': layout}

# plot = go.Figure(fig)
# plot.show()
