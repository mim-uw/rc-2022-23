#!/usr/bin/env python3
import copy
from interbotix_xs_modules.xs_robot.arm import InterbotixManipulatorXS
import numpy as np
import modern_robotics as mr


class Controller:
    def __init__(self):
        self.manipulator = InterbotixManipulatorXS(
            robot_model='vx300s',
            group_name='arm',
            gripper_name='gripper'
        )
        self.home_qs = self.get_qs()

    def forward_kinematics(self, qs: np.ndarray) -> np.ndarray:
        ee_pose = mr.FKinSpace(
            self.manipulator.arm.robot_des.M,
            self.manipulator.arm.robot_des.Slist,
            qs
        )

        return ee_pose

    def inverse_kinematics(self, x: np.ndarray, tolerance=0.03, learning_rate=0.01) -> np.ndarray:
        """ TODO: implement jacobian based method of solving inverse kinematics """

    def jacobian(self, qs: np.ndarray) -> np.ndarray:
        """ TODO: implement jacobian calculation based using finite differences """

    def get_qs(self) -> np.ndarray:
        """ Returns the current joint values """
        return np.array([
            self.manipulator.core.joint_states.position[self.manipulator.core.js_index_map[name]]
            for name in self.manipulator.arm.group_info.joint_names
        ])

    def movej(self, qs: np.ndarray, moving_time=1.):
        """ Moves to joint positions linear in joint space """
        self.manipulator.arm._publish_commands(qs, moving_time=moving_time)

    def get_ee_position(self):
        """ Return the 4x4 homogeneous matrix of a current end-effector pose """
        return self.forward_kinematics(self.get_qs())

    def movel(self, x: np.ndarray, velocity=.01, tolerance=0.03):
        """ TODO: implement robot movement linear in the cartesian end-effector space. """

    def open_gripper(self):
        self.manipulator.gripper.release()

    def close_gripper(self):
        self.manipulator.gripper.grasp()

    def move_home(self):
        self.manipulator.arm.go_to_home_pose()


def main():
    controller = Controller()
    controller.move_home()

    target = controller.get_ee_position()
    home = copy.deepcopy(target)

    target[2, 3] -= 0.1
    target[0, 3] = 0.15

    controller.movel(target)
    controller.movej(controller.inverse_kinematics(home))


if __name__ == '__main__':
    main()
