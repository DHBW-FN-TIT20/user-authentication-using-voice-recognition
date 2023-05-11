from Controller import Controller

import json
import os
import time
import sys

def main():

    # load configs from json file
    configs = []
    with open(os.path.join(os.path.dirname(__file__), "Configs", "configs.json"), "r") as json_file:
        configs = json.load(json_file)

    # use the cmd line parameter to set the config
    configId = []
    if len(sys.argv) > 1:
        try:
            configId.append(int(sys.argv[1]))
            configId.append(int(sys.argv[2]))
            configId.append(bool(sys.argv[3]))
            print(f"Using config {configId}")
        except:
            print("Invalid config ids provided.")
            sys.exit(1)
    else:
        print("No config ids provided.")
        return


    # for each config start the controller
    # add timestamp to results.csv foramt ist with Date and Time

    import datetime

    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    # timestamp = timestamp.replace(" ", "_")
    filename = f"results_{timestamp}.csv"
    print(f"Results will be saved in {filename}")
    controller = Controller(os.path.join(os.path.dirname(__file__), filename))
    # start ID is inclusive, end ID is exclusive
    for i in range(configId[0], configId[1]):
        print(f"Starting config {i}")
        controller.set_config(configs[i])
        controller.start(False)
        print(f"Finished config {i}")

if __name__ == "__main__":
    main()