from random import randrange
import re
import numpy as np
import matplotlib.pyplot as plt 

with open("training.txt") as f:
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

threshold = -2
accuracy = []
precision = []
recall = []
while threshold <= 2:
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

		if sentence_score > threshold and test_Y[i] == 1:
			true_positives += 1
		elif sentence_score > threshold and test_Y[i] == 0:
			false_positves += 1
		elif sentence_score < threshold and test_Y[i] == 1:
			false_negatives += 1
		elif sentence_score < threshold and test_Y[i] == 0:
			true_negatives += 1
		elif sentence_score == threshold:
			if test_Y[i] == 0:
				false_positves+=1
			else:
				false_negatives+=1

	accuracy.append((true_positives + true_negatives)/float(true_positives + true_negatives + false_negatives + false_positves))
	precision.append(true_positives/float(true_positives + false_positves))
	recall.append(true_positives/float(true_positives + false_negatives))
	threshold+=0.5
print accuracy
print precision
print recall
x = [-2,-1.5,-1,-0.5,0,0.5,1,1.5,2]
plt.plot(x,accuracy,color='green',marker='o',label="Accuracy")
plt.plot(x,precision,color='red',marker='^',label="Precision")
plt.plot(x,recall,color='blue',marker='*',label="Recall")
plt.axvline(x=0, color='pink', linestyle='-')
plt.xlabel("Threshold")
plt.ylabel("Values")
plt.legend(bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.)
plt.show()
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

train_input = np.array(train_input_vector)

#Sigmoid
def sigmoid(input):
	return 1/(1+np.exp(-input))

#Sigmoid Gradient
def sigmoid_grad(x):
	return x*(1-x)

#LogisticRegression
max_iter = 10000
learning_rate = 0.3
intercept = np.ones((train_input.shape[0],1))
train_input = np.hstack((intercept, train_input))
theta = np.zeros(train_input.shape[1])
train_Y_arr = np.array(train_Y)
for iter in range(max_iter):
	current_val = np.dot(train_input,theta)
	current_predictions = sigmoid(current_val)
	#Update Theta
	error = train_Y_arr - current_predictions
	gradient = np.dot(train_input.T, error)
	theta += learning_rate * gradient

test_input_vector = []
for lines in test_X:
	arr = np.zeros(count)
	for words in lines:
		if words in uniqueWords:
			arr[uniqueWords[words]] = 1
	test_input_vector.append(arr)

test_input = np.array(test_input_vector)
intercept = np.ones((test_input.shape[0],1))
test_input = np.hstack((intercept, test_input))
final_cost = np.dot(test_input, theta)
prediction = np.round(sigmoid(final_cost))
test_Y_arr = np.array(test_Y)

print 'Accuracy: {0}'.format((prediction == test_Y_arr).sum().astype(float) / len(prediction)) #98.09

