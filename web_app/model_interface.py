from lstm.lstm_model import *
from lstm.lstm_predict import *

def writeSomeBars(first_bars):
    with open('./pytorch_models/model_booba_200_epoch.net', 'rb') as f:
        checkpoint = torch.load(f)

    loaded = CharRNN(checkpoint['tokens'], n_hidden=checkpoint['n_hidden'], n_layers=checkpoint['n_layers'])
    loaded.load_state_dict(checkpoint['state_dict'])

    # Sample using a loaded model
    return sample(loaded, 2000, top_k=5, prime=first_bars)
