from Controller import Controller

import json
import os

def main():

    # load configs from json file
    configs = []
    with open(os.path.join(os.path.dirname(__file__), "Configs", "configs.json"), "r") as json_file:
        configs = json.load(json_file)

    # for each config start the controller
    controller = Controller(os.path.join(os.path.dirname(__file__), "results.csv"))
    # for config in configs:
    #     controller.set_config(config)
    #     controller.start()

    controller.set_config(configs[42])
    controller.start()

if __name__ == "__main__":
    main()