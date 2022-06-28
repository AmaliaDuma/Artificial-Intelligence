"""
In this file your task is to write the solver function!

"""


class Region:
    def __init__(self, lowerLimit, middleLimit, upperLimit):
        self.lowerLimit = lowerLimit
        self.middleLimit = middleLimit
        self.upperLimit = upperLimit

    def compute_membership_degree(self, angle):
        return max(0,
                   min((angle - self.lowerLimit) / (self.middleLimit - self.lowerLimit),
                       1,
                       (self.upperLimit - angle) / (self.upperLimit - self.middleLimit)))


def solver(thetaAngle, wAngularSpeed):
    """
    Parameters
    ----------
    thetaAngle : TYPE: float
        DESCRIPTION: the angle theta
    wAngularSpeed : TYPE: float
        DESCRIPTION: the angular speed omega

    Returns
    -------
    F : TYPE: float
        DESCRIPTION: the force that must be applied to the cart
    or

    None :if we have a division by zero

    """

    # Membership functions for angle theta; Region(lowerLimit, middleLimit, upperLimit)
    theta = {"NVB": Region(-50, -40, -25),
             "NB": Region(-40, -25, -10),
             "N": Region(-20, -10, 0),
             "ZO": Region(-5, 0, 5),
             "P": Region(0, 10, 20),
             "PB": Region(10, 25, 40),
             "PVB": Region(25, 40, 50)}

    # Membership functions for angular speed omega
    omega = {"NB": Region(-10, -8, -3),
             "N": Region(-6, -3, 0),
             "ZO": Region(-1, 0, 1),
             "P": Region(0, 3, 6),
             "PB": Region(3, 8, 10)}

    # Table for the inverted pendulum fuzzy control system rule base
    force_table = {"PVB PB": "PVVB", "PVB P": "PVVB", "PVB ZO": "PVB", "PVB N": "PB", "PVB NB": "P",
                   "PB PB": "PVVB", "PB P": "PVB", "PB ZO": "PB", "PB N": "P", "PB NB": "Z",
                   "P PB": "PVB", "P P": "PB", "P ZO": "P", "P N": "Z", "P NB": "N",
                   "ZO PB": "PB", "ZO P": "P", "ZO ZO": "Z", "ZO N": "N", "ZO NB": "NB",
                   "N PB": "P", "N P": "Z", "N ZO": "N", "N N": "NB", "N NB": "NVB",
                   "NB PB": "Z", "NB P": "N", "NB ZO": "NB", "NB N": "NVB", "NB NB": "NVVB",
                   "NVB PB": "N", "NVB P": "NB", "NVB ZO": "NVB", "NVB N": "NVVB", "NVB NB": "NVVB"
                   }

    # We have an angle theta and omega and we look for force F
    # Steps:
    #    1. compute the membership degrees for theta and omega

    membershipDegrees_theta = compute_membership_degree(theta, thetaAngle)
    membershipDegrees_omega = compute_membership_degree(omega, wAngularSpeed)

    #    2. compute according to the last table  the membership degree of F to each set.

    forces = {}
    for thetaValue in theta:
        for omegaValue in omega:
            # take the minimum of the membership values of the index set
            forceValue = min(membershipDegrees_theta[thetaValue], membershipDegrees_omega[omegaValue])
            new_forceKey = thetaValue + " " + omegaValue
            # membership degree of F to each class -> maximum value for that class taken from the rules’ table
            if force_table[new_forceKey] not in forces:
                forces[force_table[new_forceKey]] = forceValue
            elif forces[force_table[new_forceKey]] < forceValue:
                forces[force_table[new_forceKey]] = forceValue

    # defuzzify the results for F using a weighted avg of the membership degrees and the b values of the sets
    products = {"NVVB": -32, "NVB": -24, "NB": -16, "N": -8, "Z": 0, "P": 8, "PB": 16, "PVB": 24, "PVVB": 32}

    sumOfForces = 0
    product = 0
    for force in forces:
        sumOfForces += forces[force]
        product += forces[force] * products[force]

    if sumOfForces != 0:
        finalForce = product / sumOfForces
    else:
        finalForce = 0

    return finalForce


def compute_membership_degree(values, x):
    membership_degrees = {}
    for element in values:
        membership_degrees[element] = 0
        if values[element].lowerLimit <= x <= values[element].upperLimit:
            membership_degrees[element] = values[element].compute_membership_degree(x)

    return membership_degrees
