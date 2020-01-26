from lstm.lstm_model import *
from lstm.lstm_predict import *

def writeSomeBars(artist, first_bars):
    model_path = './pytorch_models/model_' + artist + '_200_epoch.net'
    with open(model_path, 'rb') as f:
        checkpoint = torch.load(f)

    loaded = CharRNN(checkpoint['tokens'], n_hidden=checkpoint['n_hidden'], n_layers=checkpoint['n_layers'])
    loaded.load_state_dict(checkpoint['state_dict'])

    # Sample using a loaded model
    return sample(loaded, 2000, top_k=5, prime=first_bars)
