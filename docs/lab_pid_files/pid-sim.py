#!/usr/bin/env python3

import math
import pybullet as p
import pybullet_data
import time

import solution

LINK_CART = 0
LINK_POLE = 1
LINK_PROP = 2
JOINT_CART = 0
JOINT_POLE = 1
JOINT_PROP = 2

POLE_LENGTH = 0.5
MAX_THRUST_N = 2

EPS = 1e-3
TEST_TIMEOUT_STEPS = 7500
TIME_STEP_S = 1 / 240

POLE_FRICTION_COEF = 0.01


class Simulation:
    def __init__(self):
        p.connect(
            p.GUI, options="--width=1920 --height=1080"
        )  # --mp4=scene0.mp4 --mp4fps=30")
        print(p.resetDebugVisualizerCamera(2.5, 90, -35, [0, 2.5, 0]))

        p.setGravity(0, 0, -9.8)

        self.cartpole = p.loadURDF("assets/table-pid.urdf")
        self.slider = p.addUserDebugParameter("  SETPOINT", 0, 1, 0)
        self.msg_id = None

        p.setJointMotorControl2(self.cartpole, JOINT_CART, p.POSITION_CONTROL, 2.5)

        p.setRealTimeSimulation(0)
        self.show_msg("INIT")
        for _ in range(100):
            self.step()

        self.show_msg("DELAY")
        time.sleep(1)
        self.show_msg("GO")

    def __del__(self):
        p.disconnect()

    def get_state(self):
        """Get cart and pole state"""
        pole_state = list(p.getJointState(self.cartpole, JOINT_POLE)[0:2])
        return list(p.getJointState(self.cartpole, JOINT_CART)[0:2]) + pole_state

    def stable_pos(self, desired):
        """Check if cart is at desired position and not moving"""
        pos, vel = self.get_state()[0:2]
        return abs(pos - desired) < EPS and abs(vel) < EPS

    def stable_angle(self, desired):
        """Check if pole is at desired angle and not moving"""
        angle, angular_vel = self.get_state()[2:4]
        return abs(angle - desired) < EPS and abs(angular_vel) < EPS

    def show_msg(self, text, rgb=[0, 0, 1]):
        """Show message in GUI
        
        Replace old msg if exists
        """
        MSG_POS = [0, 4, 0]
        if self.msg_id is not None:
            self.msg_id = p.addUserDebugText(
                text,
                MSG_POS,
                textColorRGB=rgb,
                textSize=2,
                replaceItemUniqueId=self.msg_id,
            )
        else:
            self.msg_id = p.addUserDebugText(
                text, MSG_POS, textColorRGB=rgb, textSize=2
            )

    def apply_friction(self):
        pole_friction = -POLE_FRICTION_COEF * self.get_state()[3]

        p.applyExternalTorque(
            self.cartpole,
            LINK_POLE,
            torqueObj=[-pole_friction, 0, 0],
            flags=p.WORLD_FRAME,
        )

    def free_joints(self, free_cart=False):
        # Disable joints position control
        if free_cart:
            p.setJointMotorControl2(
                self.cartpole, JOINT_CART, controlMode=p.VELOCITY_CONTROL, force=0
            )
        p.setJointMotorControl2(
            self.cartpole, JOINT_POLE, controlMode=p.VELOCITY_CONTROL, force=0
        )

    def set_prop_thrust(self, thrust_N):
        if thrust_N < 0 or thrust_N > MAX_THRUST_N:
            error_msg = f"Invalid thrust_N: {thrust_N}"
            print(error_msg)
            # raise ValueError(error_msg)
            return

        p.applyExternalForce(
            self.cartpole,
            LINK_POLE,
            forceObj=[0, 0, thrust_N],
            posObj=[0, POLE_LENGTH, 0],
            flags=p.LINK_FRAME,
        )

        # Visual
        p.setJointMotorControl2(
            self.cartpole,
            JOINT_PROP,
            p.VELOCITY_CONTROL,
            targetVelocity=thrust_N * 100,
            force=99,
        )

    def step(self):
        self.apply_friction()
        p.stepSimulation()
        time.sleep(TIME_STEP_S)

    def manual_control(self):
        # Control the cart with GUI slider
        self.show_msg("SLIDER CONTROL")
        pos_control = False  # Choose manual control behaviour

        self.free_joints()

        while True:
            if pos_control:
                p.setJointMotorControl2(
                    self.cartpole,
                    JOINT_POLE,
                    p.POSITION_CONTROL,
                    p.readUserDebugParameter(self.slider),
                )
            else:
                self.set_prop_thrust(p.readUserDebugParameter(self.slider))

            self.step()

    def test_solution(self, is_cart_moveable=False):
        # Create an instance of Solution

        target = p.readUserDebugParameter(self.slider)
        if is_cart_moveable:
            sol = solution.SolutionPos(target)
            setpoint_mult = 2 
        else:
            sol = solution.SolutionAngle(target)
            setpoint_mult = 1

        self.free_joints(is_cart_moveable)

        while True:
            self.show_msg(f"{self.get_state()[0 if is_cart_moveable else 2]:.3f}")

            # Call and apply the policy
            command = sol.update(self.get_state())
            self.set_prop_thrust(command)

            # Step pybullet
            self.step()

            # Update setpoint
            sol.change_target(setpoint_mult * p.readUserDebugParameter(self.slider))


def main():
    sim = Simulation()
    # You can test manual control by uncommenting here:
    # sim.manual_control()

    #sim.test_solution()
    sim.test_solution(True)


if __name__ == "__main__":
    main()
