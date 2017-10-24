# Zed Personal Assistant

Zed is a personal assistant that uses voice or text to open browsers, check the time, search Wikipedia, or calculate basic math problems.

Zed gets its voice from Amazons Polly API, wits from Wikipedia and WolframAlpha, and goodlooks from Skynet.

***Currently working to add a New York Times article generator.

## Getting Started

This program was built on Ubuntu 17.04

### Prerequisites

You will need the following:

```
sudo apt-get install wolfram-engine python-wxgtk2.8 python-pygame python-pywapi python-pyaudio python3-pyaudio chromium-browser

sudo pip install boto3 wikipedia
```

You will also need to obtain an API code from the following:

AWS Polly
WolframAlpha
***New York Times (WIP)

```
import wolframalpha
import wikipedia
import wx
from pygame import mixer
from subprocess import call
import time
import pywapi
import speech_recognition as sr
import boto3
import os
import sys
import random
import webbrowser
```

## Authors

* **Bryan Hardi**

## Acknowledgments

* Khanrad -- https://github.com/KhanradCoder/

I appreciate any advice or contributions. Thank you.

