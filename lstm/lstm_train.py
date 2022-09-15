from lstm_model import *
import numpy as np
import torch
from torch import nn




def train(net, data, epochs=10, batch_size=10, seq_length=50, lr=0.001, clip=5, 
          val_frac=0.1, print_every=10):
    """Trains a lyric generatori CharRNN model

    Args:
        net (nn.module): CharRNN network
        data (list): text data to train the network
        epochs (int, optional): Number of epochs for train. Defaults to 10.
        batch_size (int, optional): Number of mini-sequences per mini-batch, aka 
                                    batch size. Defaults to 10.
        seq_length (int, optional): Number of character steps per mini-batch. 
                                    Defaults to 50.
        lr (float, optional): learning rate. Defaults to 0.001.
        clip (int, optional): gradient clipping. Defaults to 5.
        val_frac (float, optional): Fraction of data to hold out for validation. 
                                    Defaults to 0.1.
        print_every (int, optional): Number of steps for printing training and 
                                    validation loss. Defaults to 10.
    """
    net.train()
    opt = torch.optim.Adam(net.parameters(), lr=lr)
    criterion = nn.CrossEntropyLoss()
    # create training and validation data
    val_idx = int(len(data)*(1-val_frac))
    data, val_data = data[:val_idx], data[val_idx:]
    counter = 0
    n_chars = len(net.chars)
    for e in range(epochs):
        # initialize hidden state
        h = net.init_hidden(batch_size)
        for x, y in get_batches(data, batch_size, seq_length):
            counter += 1
            # One-hot encode our data and make them Torch tensors
            x = one_hot_encode(x, n_chars)
            inputs, targets = torch.from_numpy(x), torch.from_numpy(y)
            # Creating new variables for the hidden state, otherwise
            # we'd backprop through the entire training history
            h = tuple([each.data for each in h])
            # zero accumulated gradients
            net.zero_grad()
            # get the output from the model
            output, h = net(inputs, h)
            # calculate the loss and perform backprop
            loss = criterion(output, targets.view(batch_size*seq_length))
            loss.backward()
            # `clip_grad_norm` helps prevent the exploding gradient problem in 
            # RNNs / LSTMs.
            nn.utils.clip_grad_norm_(net.parameters(), clip)
            opt.step()
            # loss stats
            if counter % print_every == 0:
                # Get validation loss
                val_h = net.init_hidden(batch_size)
                val_losses = []
                net.eval()
                for x, y in get_batches(val_data, batch_size, seq_length):
                    # One-hot encode our data and make them Torch tensors
                    x = one_hot_encode(x, n_chars)
                    x, y = torch.from_numpy(x), torch.from_numpy(y)
                    # Creating new variables for the hidden state, otherwise
                    # we'd backprop through the entire training history
                    val_h = tuple([each.data for each in val_h])
                    inputs, targets = x, y
                    output, val_h = net(inputs, val_h)
                    val_loss = criterion(output, 
                                         targets.view(batch_size*seq_length))
                    val_losses.append(val_loss.item())
                net.train() # reset to train mode after iterationg through 
                            # validation data
                print("Epoch: {}/{}...".format(e+1, epochs),
                      "Step: {}...".format(counter),
                      "Loss: {:.4f}...".format(loss.item()),
                      "Val Loss: {:.4f}".format(np.mean(val_losses)))