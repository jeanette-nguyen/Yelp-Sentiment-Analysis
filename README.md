# Yelp-Sentiment-Analysis

### Project Overview
Sentiment Analysis has become an important field in Machine Learning. Sentiment analysis pertains to the feelings(attitudes, emotions, opinions, etc.) towards certain products or ideas. Through sentiment analysis, companies can gain an insight of the wider public opinion on certain topics and act accordingly.

### Dataset
In this project, we explore the [Yelp Dataset](https://www.yelp.com/dataset/challenge), provided by Yelp.  Yelp provides the data in `.json` files. In this project, we will be utilizing:
- review.json
- business.json

### Dependencies
This project requires **Python 3.6** and the following library installations:
- [PyTorch](http://pytorch.org/)
- [Natural Language Toolkit](https://www.nltk.org/)
- [ArgParse](https://pypi.python.org/pypi/argparse)
- If you would like to run and execute the project through a notebook: [Jupyter Notebook](http://jupyter.org/) 

### Preprocessing the Data
#### Code
Code is provided in the `preprocessing` folder in the following files:
- preprocess_data.py
- pp_utilities.py
- pp_logger.py
- contractions_dict.py

#### How to Run
##### Parameters
Parameters are given in the `pp_args.txt` file in the `preprocessing` folder. These parameters are:
- business_data: path of `business.json` file containing business data (attributes, categories, etc.)
- review_data: path of `review.json` file containing review data (review text, user who wrote the review, business which the review pertains to, etc.)
- num_reviews: number of reviews to process
- processed_review_text: path to save processed review text
- processed_review_star: path to save star ratings
- min_freq: minimum frequency for a word to appear throughout the entirety of the taken data, else the word is removed from the review text

### Predicting Rating
#### Code
Code is provided in the main folder in the following files:
- predict_rating.py
- nn_utilities.py
- nn_logger.py

#### How to Run
##### Parameters
- Parameters are given in the `nn_args.txt` file. These parameters are:
- *num_outputs:* number of outputs for the model (since labels are 1-5, there are "6" outputs for the "0" class
- *num_review:* how many reviews to use of the dataset
- *split_pct:* percentage of the reviews to be used for training and validation
- *check_loss:* number of epochs before checking the validation loss 
- *batch_size:* number of training examples per forward/backward pass
- *embedding_dim:* embedding dimension
- *num_layers:* number of layers for the LSTM network
- *num_units:* number of units per layer
- *drop_out:* percentage of units used to incorporate [dropout](https://en.wikipedia.org/wiki/Dropout_(neural_networks))
- *max_epochs:* maximum number of epochs for the model to train
- *learning_rate:* learning rate for the model
- *data_text_file:* ./preprocessing/processed_data/first100000_std_text.p
- *data_star_file:* ./preprocessing/processed_data/first100000_std_star.p
- *optim:* specify which optimization technique to use (only the [Adam optimizer](https://machinelearningmastery.com/adam-optimization-algorithm-for-deep-learning/) was implemented
- **_training:_** indicate whether the model needs to be trained
- **save_model_file:** path where to save the model
- **losses_file:** path where to save the losses

