# Sentiment-Analysis

Implemented text analysis using analytical and machine learning models to classify sentiment of the input sentence as positive or negative. Built using Python 2.7

* For all the methods below, training dataset comprises of 80% of total dataset and testing dataset is the remaining 20%

## Analytical Method of Sentence Scoring

### Training Phase:

For all the unique words in the training, unique words are identified and their positive and negative score is computed. Positive Score of a word is incremented if it is present in a sentence with positive sentiment, and similarly negative score is incremented if it is present in a sentence with negative sentiment.

For example:

| Word | Positive Score | Negative Score 
| --- | ---| --- |
| Awesome | 387 | 1 |
| Hate | 5 | 451 |
| Harry | 874 | 810 |
| Vinci | 800 | 792 |

**Inference:** From the example, it can be observed that words which depict the underlying opinion (adjectives) have a huge difference in positive and negative score, wheras wordds like Harry, Vinci (Nouns) have similar positive and negative count depending upon the sampling.

### Testing Phase:
For all the input sentences in the testing dataset, sentence score is calculated by adding the positive score of the words and subtracting the negative score, provided that the word is present in the collection of Unique Words.A threshold for sentence score is to be choosen for classifiying sentences as positive orr negative.

Plotting the accuracy, precision and recall for various thresholds:
![alt text](https://github.com/shubhi-sareen/Sentiment-Analysis/blob/master/plot_for_accuracy.png "Plot against various thresholds") 

From the plot, it can be observed that for threshold = 0, maximum accuracy of **~89%**, along with a reaonable precision of **~94%** and recall of **~88%** is achieved.

Choosing the threshold of 0, the distribution of the testing dataset across this threshold is as follows:

![alt text](https://github.com/shubhi-sareen/Sentiment-Analysis/blob/master/ss_projection.png "Plot of testing dataset across the threshold") 


## Logistic Regression

The Hypothesis function used in Logistic Regression is Sigmoid Function. It can be represented as follows:

![alt text](https://github.com/shubhi-sareen/Sentiment-Analysis/blob/master/sigmoid.png "Sigmoid") 

The classification of the hypothesis is considered 1 if sigmoid(x)>=0.5 and 0 if it is <0.5

The cost for such classification (without regularization) is:

![alt text](https://github.com/shubhi-sareen/Sentiment-Analysis/blob/master/cost.png "cost") 

where

![alt text](https://github.com/shubhi-sareen/Sentiment-Analysis/blob/master/function.png "hypothesis function") 

Thus, we determine the weights Theta, by minimizing the cost function using Gradient Descent Optimization Technique.

**Vectorizing the Input:**

Each word is represented as a one-hot vector. This can be understood as follows:

Consider, that the set of vocabulary is {sweet, is, sugar, lemon}, then representation of:

* sweet = [ 1 0 0 0 ]
* is = [ 0 1 0 0 ]
* sugar = [ 0 0 1 0 ]
* lemon = [ 0 0 0 1 ]

Now, each sentence is represented as a combination of one-hot vectors of its constituent words. 

**For example:** "sugar is sweet" is represented as [ 1 1 1 0 ] 

For intuiition, the vectorized represention of training dataset is represented in 2 and 3 Dimensions, as follows:

![alt text](https://github.com/shubhi-sareen/Sentiment-Analysis/blob/master/projection.png "2-D") 
![alt text](https://github.com/shubhi-sareen/Sentiment-Analysis/blob/master/3d.png "2-D") 

where the blue dots represented the sentences with positive sentiment, and red dosits represent the sentences with negative sentiment. It can be observed from these plots, that the sentences with positive and negative form individual planes, and the distance between these planes will be much larger in the original dimensions.

For **10000 iterations** and a **learning rate** of **0.3**, an accuracy of **~98%** is achieved.

Dataset Source (from Kaggle): https://inclass.kaggle.com/c/si650winter11/data
