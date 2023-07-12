"""
 @file main.py
 @section authors
  - 
"""
from Controller import Controller

import json
import os

def main():
    """
    @brief Starting point of the Versuchssystem


    """

    # load configs from json file
    configs = []
    with open(os.path.join(os.path.dirname(__file__), "Configs", "configs.json"), "r") as json_file:
        configs = json.load(json_file)

    # for each config start the controller
    controller = Controller(os.path.join(os.path.dirname(__file__), "results.csv"))
    # start ID is inclusive, end ID is exclusive
    for i in range(0, 100):
        print(f"Starting config {i}")
        controller.set_config(configs[i])
        controller.start()
        print(f"Finished config {i}")

if __name__ == "__main__":
    main()