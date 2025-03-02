"""
 @file ConfigGeneration.py
 @section authors
  - Johannes Brandenburger
"""
import json
import os

configs_structured = {
    "amount_of_frames": [10000, 15000],
    "size_of_frame": [400, 600],
    "LPC": {
        "order": [13, 20],
        "weight": [0, 1]
    },
    "MFCC": {
        "order": [13, 20],
        "weight": [0, 1]
    },
    "LPCC": {
        "order": [13, 20],
        "weight": [0, 1]
    },
    "delta_MFCC": {
        "order": [13],
        "weight": [0, 1]
    }
}

configs_flat = []
config_id = -1
for amount_of_frames in configs_structured["amount_of_frames"]:
    for size_of_frame in configs_structured["size_of_frame"]:
        for LPC_order in configs_structured["LPC"]["order"]:
            for LPC_weight in configs_structured["LPC"]["weight"]:
                for MFCC_order in configs_structured["MFCC"]["order"]:
                    for MFCC_weight in configs_structured["MFCC"]["weight"]:
                        for LPCC_order in configs_structured["LPCC"]["order"]:
                            for LPCC_weight in configs_structured["LPCC"]["weight"]:
                                for delta_MFCC_order in configs_structured["delta_MFCC"]["order"]:
                                    for delta_MFCC_weight in configs_structured["delta_MFCC"]["weight"]:
                                        configs_flat.append({
                                            "id": config_id,
                                            "amount_of_frames": amount_of_frames,
                                            "size_of_frame": size_of_frame,
                                            "lpc_order": LPC_order,
                                            "lpc_weight": LPC_weight,
                                            "mfcc_order": MFCC_order,
                                            "mfcc_weight": MFCC_weight,
                                            "lpcc_order": LPCC_order,
                                            "lpcc_weight": LPCC_weight,
                                            "delta_mfcc_order": delta_MFCC_order,
                                            "delta_mfcc_weight": delta_MFCC_weight
                                        })
                                        config_id += 1

# drop first config (all zeros)
configs_flat = configs_flat[1:]

# store it in the same directory as this file
with open(os.path.join(os.path.dirname(__file__), "configs.json"), "w") as f:
    json.dump(configs_flat, f, indent=4)