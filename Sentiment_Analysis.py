from random import randrange
import re
import numpy as np
import matplotlib.pyplot as plt 

with open("Desktop/training.txt") as f:
    content = f.readlines()

content = [x.strip() for x in content]
test_Y = []
train_Y = []
train_X = []
test_X = []
size_train_x = int(0.8*len(content))

while len(train_X) <= size_train_x:
	index = randrange(len(content))
	line = content.pop(index)
	x_y = line.split("\t")
	train_X.append([x.lower() for x in x_y[1].split(" ")])
	train_Y.append(int(x_y[0]))

for lines in content:
	x_y = lines.split("\t")
	test_X.append([x.lower() for x in x_y[1].split(" ")])
	test_Y.append(int(x_y[0]))


#Sentence_Scoring
stopwords =["i","be","by","at","up","this","was","some","if","have","been","will","and","all","which","last","would","over","on","not","no","it","of","or","in","from","about","were","a","an","the","has","had","for","with","other","its","to","between","is","are","also","before","after","they","their","there","than","but","he","she"]

positive_count = {}
negative_count = {}

for i in range(len(train_X)):
	lines = train_X[i]
	for words in lines:
		if words in stopwords or len(words) == 1 or "\\" in words or words == ' ':
			continue
		if "." in words:
			for j in range(len(words)):
				if j == ".":
					break
				words = words[:j]
		if "!" in words:
			for j in range(len(words)):
				if j == ".":
					break
				words = words[:j]
		if words.isalpha() is False:
			continue
		if train_Y[i] == 1:
			if words in positive_count:
				positive_count[words]+=1
			else:
			 	positive_count[words]=1
		else:
			if words in negative_count:
				negative_count[words]+=1
			else:
			 	negative_count[words]=1


true_positives = 0
false_positves = 0
true_negatives = 0
false_negatives = 0



for i in range(len(test_X)):
	
	lines = test_X[i]
	sentence_score = 0
	
	for words in lines:
		if words in stopwords or len(words) == 1 or "\\" in words or words == ' ':
			continue
		if "." in words:
			for j in range(len(words)):
				if j == ".":
					break
				words = words[:j]
		if "!" in words:
			for j in range(len(words)):
				if j == ".":
					break
				words = words[:j]
		if words.isalpha() is False:
			continue
		total = 0
		if words in positive_count:
			total+=positive_count[words]
		if words in negative_count:
			total+=negative_count[words]
		if words in positive_count:
			sentence_score += positive_count[words]/float(total)
		if words in negative_count:
			sentence_score -= negative_count[words]/float(total)

	if sentence_score > 0 and test_Y[i] == 1:
		true_positives += 1
	elif sentence_score > 0 and test_Y[i] == 0:
		false_positves += 1
	elif sentence_score < 0 and test_Y[i] == 1:
		false_negatives += 1
	elif sentence_score < 0 and test_Y[i] == 0:
		true_negatives += 1
	elif sentence_score == 0:
		if test_Y[i] == 0:
			false_positves+=1
		else:
			false_negatives+=1

accuracy = (true_positives + true_negatives)/float(true_positives + true_negatives + false_negatives + false_positves)
precision = true_positives/float(true_positives + false_positves)
recall = true_positives/float(true_positives + false_negatives)
print accuracy
print precision
print recall

#Machine-Learning Techniques
uniqueWords = {}
count = 0
for lines in train_X:
	for words in lines:
		if words not in uniqueWords:
			uniqueWords[words] = count
			count+=1

train_input_vector = []
for lines in train_X:
	arr = np.zeros(count)
	for words in lines:
		arr[uniqueWords[words]] = 1
	train_input_vector.append(arr)