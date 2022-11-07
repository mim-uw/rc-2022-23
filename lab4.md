---
title: Lab 4
---

# Goals

The main goals of this lab:

- learn a bit about pybullet
- understand The Unified Robotic Description Format (URDF)
- setup simulation environment 
- control robot from python


# Steps

1. Install pybullet
2. Run sample simulation
3. Edit URDF file
4. Write a simple game

## Step 1

[Pybullet](https://pybullet.org/) is a Real-Time Physics Simulation engine written in C++ and Python. You can install it with `pip`. To do so in a virtual environment use following commads:

```bash
python3 -m venv pybullet_venv
. pybullet_venv/bin/activate # Use this line every time you open a new terminal session
pip install numpy pybullet
python -c 'import pybullet'
```

Last line of output should say something like `pybullet build time: Oct 11 2021 21:00:24`.

To check if everything works you can download hello_pybullet program:

```bash
wget 'https://mimuw.edu.pl/~pieniacy/robot-control/pybullet/hello_pybullet.py'
chmod +x hello_pybullet.py
./hello_pybullet.py
```

Try to grab R2D2 with your mouse and move it around. If this works, then you installed pybullet successfully.

Btw. `Ctrl + LMB` rotates the camera, `Ctrl + MMB` translates it and `Ctrl + RMB` (also scroll wheel) zooms in or out.


## Step 2

### Robot definition

Please note: Here we are using a different robot than during the last lab.

We have the following robot description in [URDF format](http://wiki.ros.org/urdf/XML/model). Save it into a `robot.urdf` file.

```xml
<?xml version="1.0" ?>
<robot name="robot">
    <link name="base_link">
        <inertial>
            <mass value="0" />
            <inertia ixx = "0" ixy = "0" ixz = "0"
                iyx = "0" iyy = "0" iyz = "0"
                izx = "0" izy = "0" izz = "0" />
        </inertial>
    </link>
    <joint name="center_z" type="prismatic">
        <parent link="base_link"/>
        <child link="y_control"/>
        <axis xyz="0 0 1"/>
        <limit effort="1000.0" lower="-0.1" upper="1.1" velocity="0.2"/>
    </joint>
    <link name="y_control">
        <inertial>
            <mass value="0.1" />
            <inertia ixx = "0" ixy = "0" ixz = "0"
                iyx = "0" iyy = "0" iyz = "0"
                izx = "0" izy = "0" izz = "0" />
        </inertial>
    </link>
    <joint name="center_y" type="prismatic">
        <parent link="y_control"/>
        <child link="x_control"/>
        <axis xyz="0 -1 0"/>
        <limit effort="1000.0" lower="-0.1" upper="1.1" velocity="0.2"/>
    </joint>
    <link name="x_control">
        <inertial>
            <mass value="0.1" />
            <inertia ixx = "0" ixy = "0" ixz = "0"
                iyx = "0" iyy = "0" iyz = "0"
                izx = "0" izy = "0" izz = "0" />
        </inertial>
    </link>
    <joint name="center_x" type="prismatic">
        <parent link="x_control"/>
        <child link="roll_control"/>
        <axis xyz="-1 0 0"/>
        <limit effort="1000.0" lower="-1.1" upper="1" velocity="0.2"/>
    </joint>
    <link name="roll_control">
        <inertial>
            <mass value="0.1" />
            <inertia ixx = "0" ixy = "0" ixz = "0"
                iyx = "0" iyy = "0" iyz = "0"
                izx = "0" izy = "0" izz = "0" />
        </inertial>
    </link>
    <joint name="gripper_roll" type="revolute">
        <parent link="roll_control"/>
        <child link="gripper_link"/>
        <axis xyz="0 0 1"/>
        <limit lower="-31.4" upper="31.4" velocity="3.14" effort="10000"/>
    </joint>
    <link name="gripper_link">
        <inertial>
            <origin rpy="0 0 0" xyz="0 0 0" />
            <mass value="1" />
            <inertia ixx="0" ixy="0" ixz="0" iyy="0" iyz="0" izz="0" />
        </inertial>
        <visual>
            <origin rpy="0 0 0" xyz="0 0 0" />
            <geometry>
                <box size="0.01 0.01 0.01"/>  
            </geometry>
            <material name="a">
                <color rgba="0.356 0.361 0.376 1" />
            </material>
        </visual>
        <collision>
            <origin rpy="0 0 0" xyz="0 0 0" />
            <geometry>
                <box size="0.01 0.01 0.01"/>
            </geometry>
        </collision>
    </link>
</robot>
```

As you can see, there is a series of joints with links between them. At the end we have `gripper_link`
which is the only visible element with shape, collision box and color. 

There are three prismatic joints (z, y, x) and then one revolute joint.
Since all prismatic joints are invisible here is a handy animation that should help you visualize a prismatic joint:

![Prismatic joint](https://user-images.githubusercontent.com/7950377/138752570-3c0aa0e1-b7c8-4bcd-919d-935f1a9ad12f.gif)

Image source: https://minecraft.fandom.com/wiki/Piston

Now imagine 3 of them chained together, perpendicular to each other such that they control z, y and x.
Fortunately, in contrast to the UR5 from the last lab, this robot has independent control over the translation axes.
We can independently work with joints to set specific coordinate values and moving one joint does not affect the others.

## Simulation

Let's load a simulation:

```python
#!/usr/bin/env python3

import pybullet as p
import pybullet_data
import time

# start the simulation with a GUI (p.DIRECT is without GUI)
p.connect(p.GUI)

# we can load plane and cube from pybullet_data
p.setAdditionalSearchPath(pybullet_data.getDataPath())

# load a plane
p.loadURDF("plane.urdf", [0, 0, -0.1], useFixedBase=True)

#setup gravity (without it there is no gravity at all)
p.setGravity(0,0,-10)

# load our robot definition
robot = p.loadURDF("robot.urdf")

# load a cube
cube_1 = p.loadURDF("cube.urdf", [0.3, 0.3, 0.1], globalScaling = 0.05)
p.changeVisualShape(cube_1, -1, rgbaColor=[1,0.5,0.7,1])

# display info about robot joints
numJoints = p.getNumJoints(robot)
for joint in range(numJoints):
  print(p.getJointInfo(robot, joint))

# add four sliders to GUI
p0_id = p.addUserDebugParameter("z", -0.1, 0, 0)
p1_id = p.addUserDebugParameter("y", -1, 1, 0)
p2_id = p.addUserDebugParameter("x", -1, 1, 0)
p3_id = p.addUserDebugParameter("pos", 0.0, 6.28, 0)

p.stepSimulation()

while True:
  # set joint parameters (we can control position, velocity, acceleration, force, and other)
  p.setJointMotorControl2(robot, 0, p.POSITION_CONTROL, p.readUserDebugParameter(p0_id))
  p.setJointMotorControl2(robot, 1, p.POSITION_CONTROL, p.readUserDebugParameter(p1_id))
  p.setJointMotorControl2(robot, 2, p.POSITION_CONTROL, p.readUserDebugParameter(p2_id))
  p.setJointMotorControl2(robot, 3, p.POSITION_CONTROL, p.readUserDebugParameter(p3_id))

  # step Simulation
  p.stepSimulation()
  time.sleep(0.01) # sometimes pybullet crashes, this line helps a lot
```

First, explore what this robot can do. Try to correlate any behaviour you observe with our URDF file. Can our robot reach the cube as of now?
Change the cube initial position in the python code such that it is reachable.
Then try to move the cube around using the visible (and collidable) link of the robot.
As you could notice the robot behaviour does not correctly reflect what we are setting with the sliders. There are some bugs in our URDF, we will fix it in the next step.


# Step 3

Get familiar with our URDF file:
 - The `gripper_link` link is really small. Make it 6cm * 4cm * 1cm.
 - Fix X and Y sliders so that the robot responds correctly.


# Step 4

Add four cubes in random places within the reach of the robot. Write a game with the goal of getting all the cubes close to the (x=0, y=0, z=-0.1) point. 
Pybullet function `getBasePositionAndOrientation` can be used to get current position of cubes. Refer back to the [hello_pybullet](https://mimuw.edu.pl/~pieniacy/robot-control/pybullet/hello_pybullet.py) code as an example of getting position of an object.

![pybullet_game](https://user-images.githubusercontent.com/7950377/138727688-9c800b10-bf2e-4d81-8805-edaf3cfae202.png)

# Step 5

Write a program that can win your game.

Functions that will be useful:
 - `getBasePositionAndOrientation` as in the previous task
 - `stepSimulation` should be used for simulation step (so don't delete it and remember to call it in a loop)
 - `setJointMotorControl2` can be used to control the robot, this function was used to apply sliders position to the robot
 - add `maxVelocity` parameter to `setJointMotorControl2` and observe the results for different values

Here is a demo of how could it look like, but remember that you can choose to implement some things differently!
You can also spot quite a few imperfections in the solution below and try to address them in your program.

![Possible solution](https://user-images.githubusercontent.com/7950377/138752169-6bd41b39-2615-4fe5-81d0-f717930c7ff4.gif)
