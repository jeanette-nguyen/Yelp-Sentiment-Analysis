import torch.nn as nn
from torch.autograd import Variable
import torch


class LSTM(nn.Module):

    def __init__(self, batch_size, num_embedding, embedding_dim=500,hidden_units=100, num_layers=1, num_outputs=6, dropout=0):

    #def __init__(self, batch_size, num_embedding, embs, embedding_dim=500,hidden_units=100, num_layers=1, num_outputs=5, dropout=0):
        '''
        :param batch_size: size of input expecting
        :param hidden_units: number of hidden units to use, default 100
        :param num_layers: number of layers, default 1
        :param num_outputs: star raing
        '''
        #print(type(num_embedding))
        #print(type(embedding_dim))

        super(LSTM, self).__init__()
        self.hidden_units = hidden_units
        self.num_layers = num_layers
        self.batch_size = batch_size
        self.num_embedding = num_embedding
        self.embedding_dim = embedding_dim

        # Create LSTM network

        self.emb = nn.Embedding(num_embedding, embedding_dim)
        #self.emb = nn.Embedding.from_pretrained(embs) # batchxSeq - > Batch x Seq x Emb Dim
        self.lstm = nn.LSTM(input_size=embedding_dim,
                            hidden_size=hidden_units,
                            num_layers=num_layers,
                            dropout=dropout)

        self.dense = nn.Linear(hidden_units, num_outputs)

        self.hidden = self.init_hidden()

    def init_hidden(self):
        if torch.cuda.is_available():
            return (nn.init.xavier_normal(Variable(torch.zeros(self.num_layers, self.batch_size, self.hidden_units),
                                                   requires_grad=True).cuda()),
                    nn.init.xavier_normal(Variable(torch.zeros(self.num_layers, self.batch_size, self.hidden_units),
                                                   requires_grad=True).cuda()))
        else:
            return (nn.init.xavier_normal(Variable(torch.zeros(self.num_layers, self.batch_size, self.hidden_units),
                                                   requires_grad=True)),
                    nn.init.xavier_normal(Variable(torch.zeros(self.num_layers, self.batch_size, self.hidden_units),
                                                   requires_grad=True)))

    def forward(self, x):
        '''
        :param x: input of size (batch, input_size)
        :param h: hidden state of previous cell or initial cell
        :param c: initial cell state for each layer in batch
        :return char_out: character outputs from network
        '''
        # Use 1's because we want character level
        # x = self.emb(x.view(1, -1)) # 1 x Batch Size

        x = self.emb(x) 
        x = x.view(-1,self.batch_size,self.embedding_dim)
        # x is now batch_size x input_size x embedding_dim

        #out, self.hidden = self.lstm(x.view(-1,self.batch_size,self.embedding_dim), self.hidden)
        out, hidden_out = self.lstm(x, self.hidden)
        out = out[-1, :, :]
        word_out = self.dense(out.view(self.batch_size,-1,self.hidden_units))
        self.hidden = hidden_out
        return word_out

