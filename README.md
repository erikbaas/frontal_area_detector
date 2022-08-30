# Frontal Area Detection by Reference Object 

This code is meant as support tool for the Aerospace Engineering MSc thesis. 

## Installation & Getting Started

### Directory Management

It is very important that you keep the same hierarchy of folders as suggested in this project! That means **for the algorithm to work, you must**:

- Put the images inside data/photos folder

You should create the folder yourself if it's not there yet (or change the paths accordingly). 

### 0. How to make the pictures

The photos you take require the following:

- Place a football or other spherical object directly next to the drone. Calculate the theoretical frontal area of the spherical object (pi * r^2) and 
assign its value to A_ref in the code.
- Make photos at a sufficient distance to mimick the "free flow" frontal area and avoid fish eye effects
- Take a series of photos at slight variations of yaw angle, such that you can take the average later.

![metsis_area_example](https://user-images.githubusercontent.com/47579794/187547062-54f0378d-ba6f-40ec-a9c7-40d9a1b6831a.jpg)

An example photo is shown above, for 0 degrees yaw and 15 degrees pitch

### 1. Download Packages 

It is advised to set up a seperate Anaconda virtual environment. The following imports are used and are thus required.

Use the package manager [pip](https://pip.pypa.io/en/stable/) (or conda) to install the following imports.

```bash
import numpy
import cv2
import numpy as np
import os
Import time
from PIL import Image
```

### 2. Run the main file and main algorithm

The core of this repository consists of the following three files. 

**Main.py** should be run first (!). It calls the utility script which crops and then converts images to numpy arrays. When prompted, please press enter to then run the color detection algorithm. 

**Utility.py** can remain untouched by the user. Utility functions contains functions that are called from other scripts. Contains the following definitions: ```def stackImages()``` to display the images together without matplotlib and ```def convertJpgToNpy()``` to convert images to numpy arrays as preprocessing. 

**areaDetection.py** is the final script. It is called from the main automatically. Note that the program takes about 10 seconds to start up! The code shows you several thresholds you can work with; the recommended settings are set as initial guesses.

Important note: **Press enter to skip to the next image** after each other!


### 4. Choose optimal settings during runtime

Assuming you are running the winning areaDetection.py, you will be presented (alongside the visual stacked images), a slider menu. Here, the following can be adjusted.

First, the color_parameters tell you the range (0-255) in which the color masking works. Please set a lower and upper bound for Blue, Green and Red, respectively.

Second, the noise_parameter bar lets you select the minimum (and maximum) area for a contour to be considered a unity. This way you can filter out noise of objects which are too small.

[![Settings-And-Parameters.jpg](https://i.postimg.cc/fTGWfVvQ/Settings-And-Parameters.jpg)](https://postimg.cc/jLhrsd9M)

## Results & Visuals

The following results can be obtained. We see size screens:

1. Original image
2. Blurred image
3. Colour masked image
4. Colour masked image
5. Image after 1 iteration of dilation
6. Detected contours, written over the original image

For the Black/White counting method we get 0.06582 m^2
For the Area method we get 0.06041076 m^2

## Support

If stuck, or if any questions arise, feel free to send an email to e.b.vanbaasbank@student.tudelft.nl

## License
[MIT](https://choosealicense.com/licenses/mit/)

## University
[![rsz-tudelft-klein.png](https://i.postimg.cc/dQGW41rc/rsz-tudelft-klein.png)](https://postimg.cc/F1sgKhTT) 








