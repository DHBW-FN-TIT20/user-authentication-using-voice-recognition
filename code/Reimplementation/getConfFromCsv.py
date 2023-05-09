    # Python Script to compare the given csv file with the existing configuration and prints the used configuration Id from Configs/Configs.json

import json
import os
import sys

def main():
    # load configs from json file
	configs = []
	with open(os.path.join(os.path.dirname(__file__), "Configs", "configs.json"), "r") as json_file:
		configs = json.load(json_file)
	
	# get filename from cmd line parameter
	filename = "results.csv"
	if len(sys.argv) > 1:
		filename = str(sys.argv[1])
		print(f"Using file {filename}")
	else:
		print("No file provided, using results.csv")
	
	# get csv from file
	csv = []
	with open(os.path.join(os.path.dirname(__file__), filename), "r") as csv_file:
		csv = csv_file.readlines()
	
	# compare which parameters from config is used in csv
	# print the config id

	# id list with id and amount of occurences
	ids:list = {"key": "value"}
	for line in csv:
		line = line.split(";")
		for config in configs:
			if (int(line[2]) == config["amount_of_frames"] and
				int(line[3]) == config["size_of_frame"] and 
				int(line[4]) == config["lpc_weight"] and
				int(line[5]) == config["lpc_order"] and
				int(line[6]) == config["mfcc_weight"] and
				int(line[7]) == config["mfcc_order"] and
				int(line[8]) == config["lpcc_weight"] and
				int(line[9]) == config["lpcc_order"] and
				int(line[10]) == config["delta_mfcc_weight"] and
				int(line[11]) == config["delta_mfcc_order"]
				):
				# add id to list but check if it is already in the list
					if int(config["id"]) in ids:
						ids[int(config["id"])] += 1
					else:
						ids[int(config["id"])] = 1
	# remove key from list
	ids.pop("key")
	# print the list
	for id in ids:
		print(f"Config {id} used {ids[id]} times")

if __name__ == "__main__":
    main()