import cv2
from torch import det
from detect import detections

# get detections from detect.py and use them to decide what action to take
# if detect "can", want to open all 5 fingers, then close them when closer to can 

finger_positions = { # 
    "open": [0, 0, 0, 0, 0],
    "close": [1, 1, 1, 1, 1]
}

def open_hand():
    global finger_positions
    finger_positions = [0, 0, 0, 0, 0]

def close_hand():
    global finger_positions
    finger_positions = [1, 1, 1, 1, 1]

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

def decide_action(detections, im_shape):
    obj = select_primary(detections)

    if obj is None:
        return None

    label = obj["label"]

    if label == "bottle":
        return "grasp_can"
    elif label == "pencil":
        return "pinch"
    else:
        return None
    
# motions 

# grasp 
def grasp_can():
    # open fingers
    open_hand()
    # wait for can to be close enough (area threshold)
    while True:
        detections = get_detections()  # function to get current detections
        obj = select_primary(detections)
        if obj and obj["label"] == "bottle" and obj["area"] > 10000:  # example threshold
            break
    # close fingers
    close_hand()