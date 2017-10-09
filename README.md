# Sentiment-Analysis

Implemented text analysis using analytical and machine learning models to classify sentiment of the input sentence as positive or negative. Built using Python 2.7

* For all the methods below, training dataset comprises of 80% of total dataset and testing dataset is the remaining 20%

## Analytical Method of Sentence Scoring

**Training Phase**

For all the unique words in the training, unique words are identified and their positive and negative score is computed. Positive Score of a word is incremented if it is present in a sentence with positive sentiment, and similarly negative score is incremented if it is present in a sentence with negative sentiment.

For example:

| Word | Positive Score | Negative Score 
| --- | ---| --- |
| Aawesome | 387 | 1 |
| Hate | 5 | 451 |
| Harry | 874 | 810 |
| Vinci | 800 | 792 |

**Inference: **From the example, it can be observed that words which depict the underlying opinion (adjectives) have a huge difference in positive and negative score, wheras wordds like HArry, Vinci (Nouns) have similar positive and negative count depending upon the sampling.

**Testing Phase**
For all the input sentences in the testing dataset, sentence score is calculated by adding the positive score of the words and subtracting the negative score, provided that the word is present in the collection of Unique Words.A threshold for sentence score is to be choosen for classifiying sentences as positive orr negative.

Plotting the accuracy, precision and recall for various thresholds:
![alt text](https://github.com/shubhi-sareen/Sentiment-Analysis/master/plot_for_accuracy.png "Plot against various thresholds")

Dataset Source (from Kaggle): https://inclass.kaggle.com/c/si650winter11/data
