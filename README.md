# Yelp-Sentiment-Analysis
Team 9

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
```$ python3 preprocess_data.py```

##### Parameters
Parameters are given in the `pp_args.txt` file in the `preprocessing` folder. These parameters are:
- **_business_data:_** path of `business.json` file containing business data (attributes, categories, etc.)
- **_review_data:_** path of `review.json` file containing review data (review text, user who wrote the review, business which the review pertains to, etc.)
- **_num_reviews:_** number of reviews to process
- **_processed_review_text:_** path to save processed review text
- **_processed_review_star:_** path to save star ratings
- **_min_freq:_** minimum frequency for a word to appear throughout the entirety of the taken data, else the word is removed from the review text

### Predicting Rating
#### Code
Code is provided in the main folder in the following files:
- predict_rating.py
- nn_utilities.py
- nn_logger.py

#### How to Run
```
$ python3 predict_rating.py
```

##### Parameters
Parameters are given in the `nn_args.txt` file. These parameters are:
- **_num_outputs:_** number of outputs for the model (since labels are 1-5, there are "6" outputs for the "0" class
- **_num_review:_** how many reviews to use of the dataset
- **_split_pct:_** percentage of the reviews to be used for training and validation
- **_check_loss:_** number of epochs before checking the validation loss 
- **_batch_size:_** number of training examples per forward/backward pass
- **_embedding_dim:_** embedding dimension
- **_num_layers:_** number of layers for the LSTM network
- **_num_units:_** number of units per layer
- **_drop_out:_** percentage of units used to incorporate [dropout](https://en.wikipedia.org/wiki/Dropout_(neural_networks))
- **_max_epochs:* maximum number of epochs for the model to train
- **_learning_rate:_** learning rate for the model
- **_data_text_file:_** ./preprocessing/processed_data/first100000_std_text.p
- **_data_star_file:_** ./preprocessing/processed_data/first100000_std_star.p
- **_optim:_** specify which optimization technique to use (only the [Adam optimizer](https://machinelearningmastery.com/adam-optimization-algorithm-for-deep-learning/) was implemented
- **_training:_** indicate whether the model needs to be trained
- **_save_model_file:_** path where to save the model
- **_losses_file:_** path where to save the losses

