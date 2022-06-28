import numpy as np
import torch

"""
   We have to create a training database and save it into a file:
      1. Create a distribution of 1000 random points in the domain [-10, 10] x [-10, 10]
      2. Compute the value of the function f for each point
      3. Create pairs d^i = ((x1^i, x2^i), f(x1^i, x2^i)), i = 1,1000
    
"""


class TrainingDb:

    upperBound = 10
    lowerBound = -10
    functionParam = 2

    @staticmethod
    def createDistribution():
        """
        :return: a distribution of 1000 random points in [-10, 10] x [-10, 10]
        """
        return (TrainingDb.upperBound - TrainingDb.lowerBound) * torch.rand(
            1000, TrainingDb.functionParam) + TrainingDb.lowerBound

    @staticmethod
    def computeFValue(x1, x2):
        """
        :param x1: first val
        :param x2: second val
        :return: the value of function f for the two values: f(x1,x2)
        """
        return np.sin((x1, x2/np.pi))

    @staticmethod
    def computeFValueAllPoints(points):
        """
        :param points: points
        :return: The value of function f for each point
        """
        return torch.tensor([TrainingDb.computeFValue(x[0], x[1]) for x in points.numpy()])

    @staticmethod
    def createPairs():
        """
        :return: pairs in the format: d^i = ((x1^i, x2^i), f(x1^i, x2^i))
        """
        distribution = TrainingDb.createDistribution()

        return torch.column_stack((distribution, TrainingDb.computeFValueAllPoints(distribution)))

    @staticmethod
    def saveToFile():
        """
        Saves the db to file "dataSet.dat"
        :return: -
        """
        torch.save(TrainingDb.createPairs(), 'dataSet.dat')
