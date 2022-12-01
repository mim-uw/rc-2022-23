---
title: Lab 8
---

# General info

**This lab is a second graded homework.** Deadline is **21th December 08:00**. At the end of this scenario you will find more details and the exact grading scheme.

# Working with colors - this section is not graded

Let's find a red ball center in the following image (right click and `Save image as...`):

![Car view](/imgs/view.png)

```python
#!/usr/bin/env python3

import cv2
import numpy as np

image = cv2.imread('view.png')

# image crop
image = image[0:400, :, :]
cv2.imshow('a', image)
cv2.waitKey()

# conversion to HSV colorspace
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# positive red hue margin
lower1 = np.array([0, 100, 50])
upper1 = np.array([10, 255, 255])
mask1 = cv2.inRange(hsv_image, lower1, upper1)

# negative red hue margin
#lower2 = np.array([160,100,50])
#upper2 = np.array([189,255,255])
#mask2 = cv2.inRange(hsv_image, lower2, upper2)

mask = mask1
#mask = mask1 + mask2

cv2.imshow('a', mask)
cv2.waitKey()

# trick for finding two centers
print("center x", np.argmax(np.sum(mask, axis=0)))
print("center y", np.argmax(np.sum(mask, axis=1)))

cv2.destroyAllWindows()
```

Can you spot a cropping operation in the code above? Why is it needed?

Read about HSV Colorspace in [Wikipedia](https://en.wikipedia.org/wiki/HSL_and_HSV) and from [OpenCV perspective](https://docs.opencv.org/4.x/df/d9d/tutorial_py_colorspaces.html). You can also experiment with [color picker](https://www.google.com/search?q=colorpicker) (observe RGB and HSV values).

![Hue circle](https://www.newsshooter.com/wp-content/uploads/2018/07/Hue-color-wheel-by-degree.png)

[Image source](https://www.newsshooter.com/2018/07/30/fiilex-matrix-ii-rgbw-hands-review/hue-color-wheel-by-degree/)

As you can see, hue (the color) is represented as a cyclic 360&deg; range and OpenCV scales degrees value by half to fit in one byte.
Normally you would just take OpenCV `cv2.inRange()` function and filter for slighlty lower to slightly higher hue than wanted.
However, red hue is 0&deg; and hue scale is cyclic, so we need to do a positive margin, but also a negative margin, which wraps around to just below 360&deg;. That way we will get filtering for all colors that are slightly off perfect red. You can now fix (uncomment) the code to correctly include negative margin.

This example was quite simple. We can find width and height of the ball using the same mask. As an exercise try this mini-task (not graded, but will be useful):

Find positions of two blue bars on the same image we just used. You can easily find blue elements with only one call to `cv2.inRange()`. Check hue value for blue and remember to divide it by half, bacause that is how OpenCV stores the hue. Find a way to deal with two detected blobs on the mask (hint: vertical crop).

# Simulation

We are going to use already known racing car. Although it may seem counterintuitive, the red block is a bumper not a spoiler.

![Racecar](/imgs/racecar_gym.gif)

This time we are going to use a custom car (`my_racecar.urdf`) and we need additional
files for this model. Easiest way to download all required files is to clone the repository:

```bash
git clone https://github.com/mim-uw/rc-2022-23
```
All needed files are located in the `docs/lab8_files/` directory.

There are only two functions you should use directly, first takes a photo, and second moves the car. Functions are provided in the library
`docs/lab8_files/assignment_2_lib.py`

Code for reference follows


```python
import numpy as np
import pybullet as p
import pybullet_data

p.connect(p.DIRECT)
p.setAdditionalSearchPath(pybullet_data.getDataPath())


def build_world_with_car(pos=((0.0, 0.0, 0.0), (0.0, 0.0, 0.0, 1.0))):
    p.resetSimulation()
    p.setGravity(0, 0, -10)
    p.loadURDF("plane.urdf")
    car = p.loadURDF("my_racecar.urdf")
    p.resetBasePositionAndOrientation(car, pos[0], pos[1])
    return car


def simulate_car(car, steeringAngle=0.2, targetVelocity=-2, steps=5000):
    wheels = [2, 3, 5, 7]
    steering = [4, 6]
    maxForce = 10
    for wheel in wheels:
        p.setJointMotorControl2(
            car,
            wheel,
            p.VELOCITY_CONTROL,
            targetVelocity=targetVelocity,
            force=maxForce,
        )
    for steer in steering:
        p.setJointMotorControl2(
            car, steer, p.POSITION_CONTROL, targetPosition=steeringAngle
        )
    for i in range(steps):
        p.stepSimulation()
    return p.getBasePositionAndOrientation(car)


def drive(car, forward, direction):
    if forward:
        speed = 2
    else:
        speed = -2
    if direction < 0:
        steeringAngle = -0.45
    elif direction > 0:
        steeringAngle = 0.45
    else:
        steeringAngle = 0
    simulate_car(car, steeringAngle, speed, 250)


def take_a_photo(car, debug=False):
    pos = p.getBasePositionAndOrientation(car)
    orn = p.getQuaternionFromEuler([0, 0, 0])
    other_pos = [[20, 0, 0], orn]
    combined_pos = p.multiplyTransforms(pos[0], pos[1], other_pos[0], other_pos[1])
    pos = list(pos[0])
    pos[2] += 0.22
    _, _, rgb, _, _ = p.getCameraImage(
        640,
        640,
        viewMatrix=p.computeViewMatrix(pos, combined_pos[0], [0, 0, 1]),
        projectionMatrix=p.computeProjectionMatrixFOV(75, 1, 0.1, 10),
    )
    if p.isNumpyEnabled() == False:
        rgb = np.reshape(rgb, [640, 640, -1])
    return rgb
```

In order to get used to the environment let's try to experiment a little.

```python
>>> import pybullet as p
pybullet build time: Sep  8 2021 14:09:42
>>> p.connect(p.GUI)
>>> from assignment_2_lib import *
>>> car = build_world_with_car()
```


![Img1](/imgs/lab8_1.png)

You should be able to see a car in the world, now let's move

```python
>>> drive(car, True, 0) # forward
>>> drive(car, True, 1) # forward left
>>> drive(car, True, -1) # forward right
>>> drive(car, False, -1) # backward left
```

`drive` function takes three parameters:

- car
- forward (True if car should move forward of False if it should move backward)
- direction (negative number -> right, 0 -> straight, positive number -> left), although you can provide any number, wheel rotation angle will be always the same, so it's treated as if it was binary signal

`drive` function is blocking and moves the car a little (100 simulation steps) in the specified direction

![Img2](/imgs/lab8_2.png)


Let's load a ball. The ball does not bounce, so it will fall on the ground after some time (200 simulation steps).

```python
>>> p.loadURDF("sphere2red.urdf", [2, 0, 1], globalScaling = 0.4)
2
>>> for _ in range(200):
...    p.stepSimulation()
```

![Img3](/imgs/lab8_3.png)

And now, lets take a photo:

```python
>>> photo = take_a_photo(car)
>>> photo.shape
(640, 640, 4)
>>> from matplotlib import pyplot as plt
>>> plt.imshow(photo)
<matplotlib.image.AxesImage object at 0x1372d8670>
>>> plt.show()
```

![Img4](/imgs/lab8_4.png)

As we can see from the shape our photo has 4 channels, those are RGBA (reg, green, blue, alpha). Matplotlib's `pyplot` expects RGB order, and as you probably remember OpenCV expects BGR order. Use `cv2.cvtColor()` accordingly to account for that.

The camera is located 10 cm above at the rear end of the car and is pointing towards the front of the car. So we can see
not only the environnement but also the car itself.

**Tasks don't require any 3D camera transformations and can be solved using only pixel-level features of photos**, therefore it is not necessary to know the details of the camera.
However, pybullet's synthetic camera uses standard pinhole camera model described during the lectures and in this [refresher](http://ksimek.github.io/2013/08/13/intrinsic/).
Pybullet's functions `p.computeViewMatrix` and `p.computeProjectionMatrixFOV` are used to calculate intrinsic and extrinsic parameters of the camera.

# Tasks

Stubs for tasks are available in the `docs/lab8_files/assignment_2_solution.py`

Semi-automatic grading will be done using `docs/lab8_files/assignment_2_tests.py`

There are three tasks. Your submission should be only one file, a modified version of `assignment_2_solution.py`. You should not read any actual data from pybullet (i.e. do not read positions and orientations of objects), you should decide how to steer using only photos from the camera.

## Task 1

The first task is to estimate how long (number of simulation steps) the car should drive forward to be near the target. The target (red ball) should not move.

To be specific: at the end of the movement car should be less then 1 m from the center of the ball. Ball should not move more than 10 cm, as in the code below:

```python
car_ball = distance.euclidean(p.getBasePositionAndOrientation(car)[0],
          p.getBasePositionAndOrientation(ball)[0])
assert car_ball < 1, car_ball

ball_move = distance.euclidean(ball_start_pos, p.getBasePositionAndOrientation(ball)[0])
assert ball_move < 0.1, ball_move
```

You should write a function that takes an image as an input and returns number of simulation steps the car should drive forward in order to reach the ball.

```python
def forward_distance(photo):
  #TODO: magic
  return some_value
```

Example of successful estimation is shown in an animation below:

![Sol1](/imgs/l8_sol1.gif)

Rules:

- Do not read coordinates of objects from the simulator.
- The only function you should change is `forward_distance`.
- The red ball is placed randomly on the line segment from `[2, 0, 0]` to `[5, 0, 0]`.
- The ball should not move.
- Two asserts in `test_forward_distance` check if the requirements are fulfilled.

Hint: Experiment with different ideas of how to calculate forward_distance. See what works, tune the parameters.

## Task 2

During the second task the ball is placed randomly in `[-3, -3] x [3,3]` square, but not too close to `[0, 0, 0]` (more then 1 m away).

Your job is to find the ball and drive close to it without moving it.

You should write `find_a_ball` function that has a loop, in which it takes photos and moves the car accordingly.

Rules:

- Do not read coordinates of objects from the simulator.
- The ball should not move.
- Use `take_a_photo(car)` function for making photos.
- Use `drive(car, forward, direction)` function for driving (forward/backward, left/straight/right).

## Task 3

This time you have to move the ball through the gate. Ball is located randomly in
`[1, -1] x [2, 1]` rectangle. Car starts in a random position on the `[4, -1] x [4, 1]` line looking at the negative x direction, so ball and gate are visible from the camera. Gate consists of two large blue cylinders in `[-2, -1]`, and `[-2, 1]` points. There are two additional green cylinders in `[-4, -1]`, and `[-4, 1]` points.

The bumper is designed so that the ball does not come loose from it.

It's enough when at the end of `move_a_ball(pos)` the ball is located in `[-4, -1] x [-2, 1]` rectangle.

On an image below you can find the finish of successful move:

![Sol3](/imgs/l8_sol3.gif)

In the `move_a_ball` function you should (as in Task 2):

- not read coordinates of objects from simulator
- use `take_a_photo(car)` function for making photos
- use `drive(car, forward, direction)` function for driving (forward/backward, left/straight/right)

# Grading

There are 12 points in total:

- 2 points for passing first task's tests
- 3 points for passing second task's tests
- 4 points for passing third task's tests
- 3 points for an overall impression (selection of methods, solutions performance, source code quality, ...)

Your submission should be one file, a modified version of `assignment_2_solution.py`.

Deadline is **21th December 08:00**.

Solutions should be submitted through the moodle. Please use slack channel #rc-hw2 to ask questions.
