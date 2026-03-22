import cv2
import sys
import serial

import time # to avoid overloading arduino
sys.path.append("..")  # or full path
from voice_control import voice_loop, get_latest_command

# get detections from detect.py and use them to decide what action to take
# if detect "can", want to open all 5 fingers, then close them when closer to can 
# start byte, wrist, thumb, pointer, mid, ring, pinky, checksum

# initialize serial port
ser = serial.Serial('COM5', 115200, timeout=1)

# give Arduino time to reset (VERY IMPORTANT)
time.sleep(2)

# send default/reset position immediately

def build_output(wrist, thumb, pointer, mid, ring, pinky):
    data_bytes = [wrist, thumb, pointer, mid, ring, pinky]

    check = 0
    for b in data_bytes:
        check ^= b

    return [190] + [0xEF] + data_bytes + [check]

ser.write(bytes(build_output(180, 1, 1, 1, 1, 1)))

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
        pointer=1,
        mid=1,
        ring=1,
        pinky=1
    )
    arduino_input = bytes(reset)
    return arduino_input

# detects based on labels, then prints output for arduino to open/close fingers accordingly
def decide_action(detections, im_shape, voice_command=None):
    if voice_command: # resets the hand position
        if "reset" in voice_command or "open" in voice_command or "reject" in voice_command:
            arduino_loop(reset_hand())
            return(arduino_input)
        
    obj = select_primary(detections)

    if obj is None:
        return None

    label = obj["label"]

    if label == "cup" or label == "bottle" or label == "can":
        print("detected can, opening hand")
        # if detected, wrist = 1, thumb = 180, pointer = 1, mid = 180, ring = 180, pinky = 180
        finger_output = build_output(1, 180, 180, 180, 180, 180)
        arduino_input = bytes(finger_output)
        arduino_loop(arduino_input)

        return(arduino_input)

    elif label == "toothbrush" or label == "pencil": # change to pen/pencil later
            print("detected pencil, opening hand")
            # if detected, wrist = 1, thumb = 180, pointer = 1, mid = 180, ring = 180, pinky = 180
            finger_output = build_output(1, 180, 180, 180, 180, 180)
            arduino_input = bytes(finger_output)
            arduino_loop(arduino_input)

            return(arduino_input)
    return None
    

last_send = 0
def arduino_loop(item):
    global last_send
    if time.time() - last_send > 0.1:  # 10 hz
        ser.write(item)
        last_send = time.time()