---
title: Working with cameras
---

# Goals

This should tell you how to work with ESP32 camera modules, which are distributed during Lab session 3 by your lab teacher.

<!---
# Physical connections
Watch this [video with instructions](https://drive.google.com/file/d/1lHgbmOissgU5pTqE78DFlTpSBdTsuWjS/view?usp=sharing).
To repeat the most important thing from the video: **be absolutely sure you connect red and black power cable the right way**.
-->

# Downloading "driver" code

Download [camera package](camera_package.tgz), it is useful to do this before disconnecting from the internet.
It is also worth setting up virtual environment to run the code, as it requires installing opencv and hence
requires internet access.

# Connecting to the board

The module should create a hotspot a few seconds after power-up, check for available networks,
you should see the `CAR-***` network where *** is the MAC address of your module. Connect with the network:

![connecting](imgs/cameras-wifi-1.png)

If you can, it is probably a good idea to simultaneously have ethernet cable with internet connection:

![two connections](imgs/cameras-wifi-1.png)

If you are unable to connect ethernet you will not be able to use internet and the camera at the same time.
You will need to switch wifi networks back and forth.

# Getting frames

Take `camera_package.tgz` that you downloaded before, extract files, run and inspect `camera_demo.py`.
You are not required to understand how frames are fetched from the camera.
Therefore, you can use this code as a blackbox and just use it to get frames, below is a brief API explanation:

```python
# Create camera object, you can optionally pass quality parameter, which will control resolution
cam = Camera()

while True:
    # Camera module will stop streaming if no keepalive is received for some time (to handle crashes etc.)
    cam.keep_stream_alive()
    # This is a blocking function and will return the most recent frame
    img = cam.get_frame()
    ...
```

Current implementation of the API is something like a public beta.
We are actively working on in to improve performance, robustness and get rid of crashes.
But it is perfectly usable and you should be albe to have some fun with the camera already.

# Image defects

Verify that image from the camera looks fine.
It should be quite smooth (>30 fps) on lower resolutions, on highest resolutions performance of ~5 fps is nominal.

Do not worry if you have a single dead pixel somewhere (one pixel that is constantly white, black, etc.).
You can try changing the resolution up or down, maybe that pixel will not be sampled anymore, but in general you can just ignore it.
If you want to perform a smart workaround you can try to localize your dead pixel and substitute this pixel's value for an average of its neighbours.

All cameras were checked and should work fine, but if you spot a bigger defect, like large part of the image looks wrong, or half of the view has wrong colours, let us know!

These cameras are not of the greatest quality, but at their price they are very cost effective. They include an ESP32 microcontroller with WiFi and camera, so we will use these boards to build a robot!
