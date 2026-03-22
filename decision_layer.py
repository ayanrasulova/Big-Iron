import cv2

import sys
sys.path.append("..")  # or full path

from voice_control import voice_loop, latest_command

# get detections from detect.py and use them to decide what action to take
# if detect "can", want to open all 5 fingers, then close them when closer to can 

# start byte, wrist, thumb, pointer, mid, ring, pinky, checksum

#defaults
data_bytes = [1, 1, 180, 1, 1, 1]

def build_output(wrist, thumb, pointer, mid, ring, pinky):
    data_bytes = [wrist, thumb, pointer, mid, ring, pinky]

    check = 0
    for b in data_bytes:
        check ^= b

    return [190] + data_bytes + [check]

# select largest object
def select_primary(detections, min_area=5000):
    if not detections:
        return None

    # filter small objects
    detections = [d for d in detections if d["area"] > min_area]

    if not detections:
        return None

    # pick largest (closest)
    return max(detections, key=lambda d: d["area"])

def reset_hand():
    print("VOICE: resetting hand")

    reset = build_output( # all should be 1 except wrist and pointer (which are reversed)
        wrist=180,
        thumb=1,
        pointer=180,
        mid=1,
        ring=1,
        pinky=1
    )
    arduino_input = bytes(reset)
    return arduino_input

def decide_action(detections, im_shape, voice_command=None):

    if voice_command: # resets the hand position
        if "reset" in voice_command or "open" in voice_command or "reject" in voice_command:
            reset_hand()
        
    obj = select_primary(detections)

    if obj is None:
        return None

    label = obj["label"]

    if label == "cup" or label == "bottle":
        print("detected cup, opening hand")
        # if detected, wrist = 1, thumb = 180, pointer = 1, mid = 180, ring = 180, pinky = 180
        finger_output = build_output(1, 180, 1, 180, 180, 180)
        arduino_input = bytes(finger_output)
        print(finger_output)
        return(arduino_input)


        # ignore this for now 
        # if obj["area"] < 10000:
        #      return "approach"
        # else:
        #      return "grasp_can"

    elif label == "toothbrush": # change to pen/pencil later
            print("detected pencil, opening hand")
            # if detected, wrist = 1, thumb = 180, pointer = 1, mid = 180, ring = 180, pinky = 180
            finger_output = build_output(1, 180, 1, 180, 180, 180)
            arduino_input = bytes(finger_output)
            print(finger_output)
            return(arduino_input)
    return None
    
# motions 

# grasp 
# def grasp_can():
#     # open fingers
#     open_hand()
#     # wait for can to be close enough (area threshold)
#     while True:
#         detections = get_detections()  # function to get current detections
#         obj = select_primary(detections)
#         if obj and (obj["label"] == "bottle" or obj["label"] == "cup") and obj["area"] > 10000:  # example threshold
#             break
#     # close fingers
#     close_hand()