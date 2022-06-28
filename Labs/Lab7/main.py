import numpy as np
import torch

from createDB import TrainingDb
from myModel import Net
from trainModel import TrainModel

INPUT_TENSORS = [
    torch.tensor([0.0, 1.0]),
    torch.tensor([1.0, 0.0]),
    torch.tensor([-3.0, 3.0]),
    torch.tensor([1.0, 1.0]),
    torch.tensor([2.0, 2.0]),
    torch.tensor([np.pi, np.pi]),
    torch.tensor([np.pi, 0]),
    torch.tensor([0, np.pi]),
]


def run():
    # TrainingDb.saveToFile()
    x = TrainModel()
    x.train()
    x.saveToFile()

    neuralNetwork = Net(2, 10, 1)
    neuralNetwork.load_state_dict(torch.load('myNetwork.pt'))
    neuralNetwork.eval()

    for inputTensor in INPUT_TENSORS:
        print(neuralNetwork(inputTensor).item())


if __name__ == '__main__':
    run()
