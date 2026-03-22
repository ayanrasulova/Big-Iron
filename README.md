# Welcome to Big Iron!
The Quickest prosthetic in the Wild West! Official "HooHacks 2026" Submission for: Ayan Rasulova (GitHub: ayanrasulova), Emilie Deadman (GitHub: echiino), Amelia Chen, Jack Ellis (GitHub: jackawackadoo)

## Our Inspiration:

A lot of our previous projects have involved tools for accessiblity. We noticed that a lot of modern prosthetic limbs typically average in the ~thousands, depending on complexity. We wanted to see if, with a very low budget, we would be able to create a much cheaper alternative (<$40) using computer vision. 

## Features:

Big Iron utilizes YOLOv5, fine tuning our image classification model with real-world data. The user wears the webcam, which detects objects within a certain distance. The computer vision application composes and transmits a package to an Arduino Nano, which drives the prosthetic arm using a hardware API we developed. 

## Run Instructions
**You must be using Python 3.11 for the necessary libraries to work** 

First, you must install all the correct dependencies in a virtual environment using our install script: 

```
# create venv (if mac do python3)
python -m venv yolov5-env

# activate (on mac do source yolov5-env/bin/activate)
yolov5-env\Scripts\activate

# install requirements
python install.sh
```

Then, cd to the yolov5 directory, and run the following command to start the webcam:
```
python detect.py --weights yolov5x.pt --source 0
# if the webcam is not opening up, change it to --source 1 (or whatever the source of the webcam you are using is)
```
