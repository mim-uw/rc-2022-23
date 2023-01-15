#!/usr/bin/env python3

import math
import pybullet as p
import pybullet_data
import time

import solution

LINK_CART = 0
LINK_POLE = 1
JOINT_CART = 0
JOINT_POLE = 1

EPS = 1e-3
TEST_TIMEOUT_STEPS = 7500
TIME_STEP_S = 1 / 240

POLE_FRICTION_COEF = 0.001


class Simulation:
    def __init__(self):
        p.connect(p.GUI, options="--width=1920 --height=1080")
        print(p.resetDebugVisualizerCamera(3.5, 90, -25, [0, 0, 0]))

        p.setGravity(0, 0, -9.8)

        self.cartpole = p.loadURDF("assets/table-cartpole.urdf")
        self.slider = p.addUserDebugParameter("y", -1, 1, 0)
        self.msg_id = None

        p.setRealTimeSimulation(0)
        time.sleep(1)

    def __del__(self):
        p.disconnect()

    def get_state(self):
        pole_state = list(p.getJointState(self.cartpole, JOINT_POLE)[0:2])
        pole_state[0] = (-pole_state[0] + (math.pi / 2)) % (2 * math.pi)
        if pole_state[0] > math.pi:
            pole_state[0] -= 2 * math.pi
        pole_state[1] = -pole_state[1]
        return list(p.getJointState(self.cartpole, JOINT_CART)[0:2]) + pole_state

    def stable_pos(self, desired):
        pos, vel = self.get_state()[0:2]
        return abs(pos - desired) < EPS and abs(vel) < EPS

    def stable_angle(self, desired):
        angle, angular_vel = self.get_state()[2:4]
        return abs(angle - desired) < EPS and abs(angular_vel) < EPS

    def msg(self, text, rgb=[0, 0, 1]):
        # Replace old msg if exists
        if self.msg_id is not None:
            self.msg_id = p.addUserDebugText(
                text,
                [2, 0, 0],
                textColorRGB=rgb,
                textSize=2,
                replaceItemUniqueId=self.msg_id,
            )
        else:
            self.msg_id = p.addUserDebugText(
                text, [2, 0, 0], textColorRGB=rgb, textSize=2
            )

    def apply_friction(self):
        pole_friction = -POLE_FRICTION_COEF * self.get_state()[3]

        p.applyExternalTorque(
            self.cartpole,
            LINK_POLE,
            torqueObj=[-pole_friction, 0, 0],
            flags=p.WORLD_FRAME,
        )

    def setup_state(self, desired_pos, desired_angle):
        # Engage joints position control
        p.setJointMotorControl2(
            self.cartpole, JOINT_CART, p.POSITION_CONTROL, desired_pos
        )
        p.setJointMotorControl2(
            self.cartpole,
            JOINT_POLE,
            p.POSITION_CONTROL,
            -desired_angle + (math.pi / 2),
        )

        # Run simulation until state achieved
        while True:
            p.stepSimulation()
            time.sleep(TIME_STEP_S)
            if self.stable_pos(desired_pos) and self.stable_angle(desired_angle):
                break

        # Disable joints position control
        p.setJointMotorControl2(
            self.cartpole, JOINT_CART, controlMode=p.VELOCITY_CONTROL, force=0
        )
        p.setJointMotorControl2(
            self.cartpole, JOINT_POLE, controlMode=p.VELOCITY_CONTROL, force=0
        )

    def manual_control(self):
        # Almost perfect setup
        self.msg("PERFECT SETUP")
        self.setup_state(0, 0)

        # Control the cart with GUI slider
        self.msg("SLIDER CONTROL")
        pos_control = False  # Choose manual control behaviour

        while True:
            if pos_control:
                p.setJointMotorControl2(
                    self.cartpole,
                    JOINT_CART,
                    p.POSITION_CONTROL,
                    p.readUserDebugParameter(self.slider),
                )
            else:
                p.applyExternalForce(
                    self.cartpole,
                    LINK_CART,
                    forceObj=[0, 10 * p.readUserDebugParameter(self.slider), 0],
                    posObj=[0, 0, 0],
                    flags=p.WORLD_FRAME,
                )

            self.apply_friction()
            p.stepSimulation()
            time.sleep(TIME_STEP_S)

    def test_solution(self, target=0):
        # Create an instance of Solution
        sol = solution.Solution1(self.get_state(), target)

        steps = 0
        total_effort = 0
        total_effort_sqr = 0
        while steps < TEST_TIMEOUT_STEPS:
            # Call and apply the policy
            command = sol.update(self.get_state())
            p.applyExternalForce(
                self.cartpole,
                LINK_CART,
                forceObj=[0, command, 0],
                posObj=[0, 0, 0],
                flags=p.WORLD_FRAME,
            )

            # Step pybullet
            self.apply_friction()
            p.stepSimulation()
            time.sleep(TIME_STEP_S)

            # Benchmarking
            total_effort += abs(command)
            total_effort_sqr += command**2
            steps += 1

            # Check for acceptance
            if self.stable_pos(target) and self.stable_angle(target):
                print(f"Accepting {self.get_state()}")
                return True, steps, total_effort, total_effort_sqr

        # Timeout occured
        return False, None, None, None

    def test_case(self, start_pos, start_angle, target, silent=False):
        self.msg("SETUP")
        self.setup_state(start_pos, start_angle)

        self.msg("TESTING")
        ret = self.test_solution(target)

        if not silent:
            if ret[0]:
                print(f"\n--- Success! ---\nSteps: {ret[1]}\nEffort: {ret[2]:.2f}\n")
                self.msg("SUCCESS", [0, 0.7, 0])
            else:
                print(f"\n--- Timeout! ---\n")
                self.msg("TIMEOUT", [0.7, 0, 0])
            time.sleep(0.5)

        return ret


def main():
    sim = Simulation()
    # You can test manual control by uncommenting here:
    # sim.manual_control()

    # NOTICE: These are only examples, grading cases may include more thorough testing.
    # NOTICE: It is not required to support targets other than (0,0,0,0)
    # ... but you are encouraged to implement arbitrary target position setting!
    sim.test_case(0.1, 0.03, 0)
    sim.test_case(1, 0, 0)
    sim.test_case(-1.5, -0.4, 0)
    sim.test_case(1.5, -1, 0)


if __name__ == "__main__":
    main()
