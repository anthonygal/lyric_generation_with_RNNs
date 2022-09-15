import numpy as np
import torch
import torch.nn.functional as F

from lstm.lstm_utils import one_hot_encode



def predict(net, char, h=None, top_k=None):
        """Given a character, predict the next character and hidden state."""
        x = np.array([[net.char2int[char]]])
        x = one_hot_encode(x, len(net.chars))
        inputs = torch.from_numpy(x)
        h = tuple([each.data for each in h])
        out, h = net(inputs, h)
        p = F.softmax(out, dim=1).data
        if top_k is None:
            top_ch = np.arange(len(net.chars))
        else:
            p, top_ch = p.topk(top_k)
            top_ch = top_ch.numpy().squeeze()
        p = p.numpy().squeeze()
        char = np.random.choice(top_ch, p=p/p.sum())
        return net.int2char[char], h


def sample(net, size, prime='Il', top_k=None):
    net.cpu()
    net.eval()
    chars = [ch for ch in prime]
    h = net.init_hidden(1)
    for ch in prime:
        char, h = predict(net, ch, h, top_k=top_k)
    chars.append(char)
    for _ in range(size):
        char, h = predict(net, chars[-1], h, top_k=top_k)
        chars.append(char)
    return ''.join(chars)
