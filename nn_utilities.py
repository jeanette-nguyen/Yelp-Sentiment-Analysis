import torch
import torch.utils.data
from torch.autograd import Variable

from nltk.tokenize import word_tokenize
import random

def split_data(x,y):
    data = list(zip(x,y))
    random.shuffle(data)
    #zip(*data)
    data = data[:100000] #get only 100000 reviews
    total = len(data)
    train = data[:int(0.7*total)]
    valid = data[int(0.7*total): int(0.85*total)]
    test = data[int(0.85*total)]
    return train, valid, test

def word2int(review_text):
    assert isinstance(review_text, list)

    all_text = ' '.join(review_text)
    words = word_tokenize(all_text)
    word2int = dict((a, b) for b, a in enumerate(list(set(words))))
    return word2int

def text2numbers(text, word2int):
    assert isinstance(text,list)
    assert isinstance(word2int,dict)

    encoded_text = []
    for t in text: 
        words = word_tokenize(t)
        words_int = list(map(lambda x: word2int[x], words))
        encoded_text.append(words_int)
    return encoded_text

def load_dataset(data):
    assert isinstance(data, list)
    data = [list(a) for a in zip(*data)]
    inputs = torch.LongTensor(data[0])
    targets = torch.LongTensor(data[1])
    return torch.utils.data.TensorDataset(inputs, targets)

def load_model(model,optimizer,gpu,filename):
    assert isinstance(filename,str)
    assert isinstance(gpu,bool)

    if gpu:
        f = torch.load(filename)
    else:
        f = torch.load(filepath, map_location=lambda storage, loc:storage)

    epoch = f['epoch']
    losses = f['losses']
    model.load_state_dict(f['state_dict'])
    optimizer.load_state_dict(f['optimizer'])

    return model, optimizer, epoch, losses

def make_variable(data,gpu):
    assert isinstance(gpu,bool)
    X, y = data
    X, y = Variable(X), Variable(y) 
    if gpu:
        X = X.cuda()
        y = y.cuda()
    return X, y

def checkpoint(state, file_name):
    '''
    Save the PyTorch model

    :param state: Contains everything to be stored
    :type state: dict
    :param file_name: path where to save the file
    :type file_name: str
    '''

    assert isinstance(state, dict)
    assert isinstance(file_name, str)

    torch.save(state, file_name)

def early_stop(loss):
    assert isinstance(loss,list)
    return loss[-3] > loss[-4] and loss[-2] > loss[-3] and loss[-1] > loss[-4]