from network import lstm
import nn_logger as logger
import nn_utilities as utils

import torch
import torch.optim as optim
from torch.autograd import Variable

import numpy as numpy
import datetime
import random
import string

# Read in arguments from text file
args = logger.read_args('nn_args.txt')

# Check if running on GPU
gpu = torch.cuda.is_available()
if gpu:
    print("\nRunning on GPU\n")


def train(model, train_data, valid_data, criterion, optimizer, word2int):
    global temp_x
    global temp_y
    dataset_train = utils.load_dataset(train_data)
    dataset_valid = utils.load_dataset(valid_data)

    loader_train = torch.utils.data.DataLoader(dataset_train, batch_size=args.batch_size, shuffle=True)
    loader_valid = torch.utils.data.DataLoader(dataset_train, batch_size=args.batch_size, shuffle=False)

    losses = {'train': [], 'valid': []}
    for epoch in range(args.max_epochs):
        curr_train_loss = 0
        for batch,data in enumerate(loader_train):
            print(batch)
            X, y = utils.make_variable(data,gpu)
            temp_x = X
            temp_y = y
            model.zero_grad()
            output = model(X)
            loss = criterion(torch.squeeze(output, dim=1), y)
            curr_train_loss += loss.data[0]
            loss.backward(retain_graph=True)
            #loss.backward()
            optimizer.step()
        losses['train'].append(curr_train_loss)

        # Check validation loss after specified number of epochs
        if epoch%args.check_loss == 0:
            curr_valid_loss = 0
            for batch,data in enumerate(loader_train):
                X, y = utils.make_variable(data,gpu)
                model.zero_grad()
                #output = model(X.detach())
                output = model(X)
                loss = criterion(torch.squeeze(output, dim=1), y)
                curr_train_loss += loss
                loss.backward()
                optimizer.step()
            losses['valid'].append(curr_valid_loss)

            utils.pickle_files(args.losses_file,losses)
            if curr_valid_loss < min(losses['valid']):
                print("Saving Model")
                utils.checkpoint({'state_dict': model.state_dict(),
                                  'optimizer': optimizer.state_dict()},
                                  args.save_model_file)
            #pif args.early_stop.lower() == 'true':
            if len(losses['valid'])>10 and utils.early_stop(losses['valid']):
                break

        print('Epoch: {}\tCurrent Train Loss: {}\tValidation Loss: {} \r'.format(
            epoch, curr_train_loss, curr_val_loss, ),end='')

    return model, losses

def main():

    review_text = logger.load_files(args.data_text_file)
    word2int = utils.word2int(review_text)
    data_x = utils.text2numbers(review_text,word2int)
    data_y = logger.load_files(args.data_star_file)
    train_data,valid_data,test_data = utils.split_data(data_x,data_y)

    #Model
    model = lstm.LSTM(args.batch_size, len(word2int), embedding_dim=args.embedding_dim, 
                      hidden_units=args.num_units, num_layers=args.num_layers, 
                      num_outputs=args.num_outputs, dropout=args.drop_out)

    # Loss function
    criterion = torch.nn.CrossEntropyLoss()

    # Optimizer function
    optimizer = optim.Adam(model.parameters(), lr=args.learning_rate)

    if args.training.lower()=='true': 
        train(model, train_data, valid_data, criterion, optimizer, word2int)
    else:
        model, optimizer, epoch, losses = utils.load_model(model,optimizer,gpu,args.save_model_file)

if __name__=="__main__":
    main()