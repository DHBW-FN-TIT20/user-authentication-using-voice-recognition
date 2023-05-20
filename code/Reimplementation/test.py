import os
import json

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
        
uuids = []
writable_lines = []
with open("/home/henry/Documents/Studium/Studienarbeit/Ergebnisse/combined.csv", "r") as csv_file:
    lines = csv_file.readlines()

    with open("/home/henry/Documents/Studium/Studienarbeit/Ergebnisse/without.csv", "w") as write_file:
        for line in lines:
            arguments = line.split(";")
            config_id = get_config_id_from_features(arguments)
            uuid_lines = []
            # if config_id >= 471 and config_id <= 478:
            if arguments.count("1.0") == 1 and arguments.count("0.0") == 19:
                uuids.append(arguments[0])
            else:
                writable_lines.append(line)
        for wline in writable_lines:
            if wline.split(";")[0] not in uuids:
                write_file.write(wline)
                print("line")

