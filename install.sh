#!/bin/bash

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Installing SpeechRecognition..."
pip install SpeechRecognition

# Detect OS
OS="$(uname)"

if [ "$OS" = "Darwin" ]; then
    echo "Detected macOS"

    echo "Installing PortAudio via Homebrew..."
    if ! command -v brew &> /dev/null
    then
        echo "Homebrew not found. Install it first: https://brew.sh/"
        exit 1
    fi

    brew install portaudio

    echo "Installing PyAudio..."
    pip install pyaudio

elif [ "$OS" = "Linux" ]; then
    echo "Detected Linux"

    sudo apt-get update
    sudo apt-get install -y portaudio19-dev python3-pyaudio

    pip install pyaudio
fi

echo "Done!"