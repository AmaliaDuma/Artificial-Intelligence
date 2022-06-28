import matplotlib.pyplot as plt
import torch

import myModel


class TrainModel:
    def __init__(self):
        # Set up the lossFunction as the mean square error
        self.lossFunction = torch.nn.MSELoss()

        # Create the ANN
        self.neuralNetwork = myModel.Net(2, 10, 1).double()

        # Set up an optimizer that implements stochastic gradient descent
        self.optimizerBatch = torch.optim.SGD(self.neuralNetwork.parameters(), lr=0.01)

        # Load the training data
        pairedTensor = torch.load('dataSet.dat')
        self.inputTensor = pairedTensor.narrow(1, 0, 2)  # just the first 2 columns
        self.outputTensor = pairedTensor.narrow(1, 2, 1)  # just the last column

    def train(self):
        # Memorize the losses for some graphics
        lossList = []
        avgLossList = []

        # Set up the environment for training in batches
        batchCount = int(1000 / 20)
        splitInputData = torch.split(self.inputTensor, 20)
        splitOutputData = torch.split(self.outputTensor, 20)

        for epoch in range(2000):
            lossSum = 0
            for batchIndex in range(batchCount):
                # Compute the output of the current batch
                predictedOutput = self.neuralNetwork(splitInputData[batchIndex].double())

                # Compute the loss for the current batch
                loss = self.lossFunction(predictedOutput, splitOutputData[batchIndex])

                # Save to plot
                lossList.append(loss)

                # Add it to the sum for average list
                lossSum += loss.item()

                # Set up the gradients for the weights to zero
                self.optimizerBatch.zero_grad()

                # Compute automatically the variation for each weight and bias of the network
                loss.backward()

                # Compute the new values for the weights
                self.optimizerBatch.step()

            avgLossList.append(lossSum / batchCount)

            # Print the loss for all the dataset for each 10th epoch
            if epoch % 100 == 99:
                y_pred = self.neuralNetwork(self.inputTensor.double())
                loss = self.lossFunction(y_pred, self.outputTensor)
                print('\repoch: {}\tLoss =  {:.5f}'.format(epoch, loss))

        plt.plot(avgLossList)
        plt.show()


    def saveToFile(self):
        """
        Saves the trained network to file "myNetwork.pt"
        :return: -
        """
        torch.save(self.neuralNetwork.state_dict(), 'myNetwork.pt')
