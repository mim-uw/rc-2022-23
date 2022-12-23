import control
import numpy as np


# This is a stub of your solution
# Add your code in any organized way, but please keep the following signatures unchanged
# Solution1 should optimize for speed, Solution2 for effort. Refer to the assignement specification.


# Keep this signature unchanged for automated testing!
# Returns 2 numpy arrays - matrices A and B
def linearize(
    gravity: float,
    mass_cart: float,
    mass_pole: float,
    length_pole: float,
    mu_pole: float,
):
    # A = np.array(...)
    # B = np.array(...)
    return A, B


class Solution1:
    # Keep this signature unchanged for automated testing!
    # Reminder: implementing arbitrary target_pos is not required, but please try!
    def __init__(self, init_state, target_pos):
        pass

    # Keep this signature unchanged for automated testing!
    # Returns one float - a desired force (u)
    def update(self, state):
        pass


class Solution2:
    # Keep this signature unchanged for automated testing!
    # Reminder: implementing arbitrary target_pos is not required, but please try!
    def __init__(self, init_state, target_pos):
        pass

    # Keep this signature unchanged for automated testing!
    # Returns one float - a desired force (u)
    def update(self, state):
        pass
