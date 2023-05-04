from Controller import Controller

import json
import os

def main():
    with open(os.path.join(os.path.dirname(__file__), "Configs", "configs.json"), "r") as json_file:
        data = json.load(json_file)

        print(data[0])

        controller = Controller(os.path.join(os.path.dirname(__file__), "results.csv"))
        controller.set_config(data[1])
        controller.start()

if __name__ == "__main__":
    main()