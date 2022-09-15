import torch

from lstm.lstm_model import CharRNN
from lstm.lstm_predict import sample




def writeSomeBars(artist, first_bars):
    """Generates a sample of lyrics for a given artist from the first_bars"""
    model_path = './pytorch_models/model_' + artist + '_200_epoch.net'
    with open(model_path, 'rb') as f:
        checkpoint = torch.load(f)
    loaded = CharRNN(checkpoint['tokens'], 
                     n_hidden=checkpoint['n_hidden'], 
                     n_layers=checkpoint['n_layers'])
    loaded.load_state_dict(checkpoint['state_dict'])
    return sample(loaded, 2000, top_k=5, prime=first_bars)
