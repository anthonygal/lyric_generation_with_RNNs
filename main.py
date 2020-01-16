import numpy as np
import os

from lstm_model import CharRNN
from lstm_train import train
from lstm_predict import sample

with open('kanye_lyrics.txt') as f:
    text = f.read()
    f.close()

chars = tuple(set(text))
int2char = dict(enumerate(chars))
char2int = {ch: ii for ii, ch in int2char.items()}

# encode the text
encoded = np.array([char2int[ch] for ch in text])

# define and print the net
n_hidden=512
n_layers=4

net = CharRNN(chars, n_hidden, n_layers)
print(net)

batch_size = 64
seq_length = 160 #max length verses
n_epochs = 2 # start smaller if you are just testing initial behavior

# train the model
train(net, encoded, epochs=n_epochs, batch_size=batch_size, seq_length=seq_length, lr=0.001, print_every=10)

# Generate some lyrics
print(sample(net, 1000, prime='My ', top_k=5))
