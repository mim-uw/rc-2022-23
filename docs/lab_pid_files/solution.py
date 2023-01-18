import csv
import numpy as np


class Lowpass:
    def __init__(self, filtering=0.8, init_val=0):
        self.filtering = filtering
        self.filtered = init_val

    def update(self, value):
        self.filtered = self.filtering * self.filtered + (1 - self.filtering) * value
        return self.filtered


class PID:
    def __init__(
        self, name, kp, ki, kd, limits, iterm_limits=None, setpoint=0, d_lowpass=0.1
    ):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.limits = limits
        self.iterm_limits = limits if iterm_limits is None else iterm_limits
        self.setpoint = setpoint

        self.iterm = 0
        self.derivative_filter = Lowpass(d_lowpass)
        self.previous_value = None
        self.output = None

        self.iteration = 0
        self.csvfile = open(name + ".csv", "w", newline="")
        self.csvwriter = csv.writer(
            self.csvfile, delimiter=",", quotechar="|", quoting=csv.QUOTE_MINIMAL
        )
        self.csvwriter.writerow(["iter", "p", "i", "d", "out", "input", "setpoint"])

    def update(self, input):
        error = input - self.setpoint

        self.iterm += self.ki * -error
        if self.iterm > self.iterm_limits[1]:
            self.iterm = self.iterm_limits[1]
        elif self.iterm < self.iterm_limits[0]:
            self.iterm = self.iterm_limits[0]

        derivative = input - self.previous_value if self.previous_value else 0
        self.previous_value = input
        self.derivative_filter.update(derivative)

        pterm = self.kp * -error
        dterm = self.kd * -self.derivative_filter.filtered
        self.output = pterm + self.iterm + dterm

        if self.output > self.limits[1]:
            self.output = self.limits[1]
        elif self.output < self.limits[0]:
            self.output = self.limits[0]

        self.csvwriter.writerow(
            [
                self.iteration,
                pterm,
                self.iterm,
                dterm,
                self.output,
                input,
                self.setpoint,
            ]
        )

        self.iteration += 1
        return self.output


MAX_FORCE = 2
MAX_FORCE_ITERM = 1


class SolutionAngle:
    def __init__(self, target):
        self.angle_pid = PID(
            "angle", 1.5, 0.005, 100, (0, MAX_FORCE), (0, MAX_FORCE_ITERM), target
        )

    def change_target(self, target):
        self.angle_pid.setpoint = target

    def update(self, state):
        return self.angle_pid.update(state[2])


MAX_ANGLE = 1


class SolutionPos:
    def __init__(self, target):
        self.angle_control = SolutionAngle(0)
        self.pos_pid = PID(
            "pos", 1.5, 0.0, 500, (-MAX_ANGLE, MAX_ANGLE), setpoint=target
        )

    def change_target(self, target):
        self.pos_pid.setpoint = target

    def update(self, state):
        self.angle_control.change_target(-self.pos_pid.update(state[0]))
        return self.angle_control.update(state)
