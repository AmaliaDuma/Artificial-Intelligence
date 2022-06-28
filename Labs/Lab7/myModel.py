import torch.nn
import torch.nn.functional as F


class Net(torch.nn.Module):

    def __init__(self, initialLayerSize, hiddenLayerSize, outputLayerSize):
        super(Net, self).__init__()
        self.hidden = torch.nn.Linear(initialLayerSize, hiddenLayerSize)
        self.output = torch.nn.Linear(hiddenLayerSize, outputLayerSize)

    def forward(self, x):
        x = F.relu(self.hidden(x))
        x = self.output(x)
        return x
