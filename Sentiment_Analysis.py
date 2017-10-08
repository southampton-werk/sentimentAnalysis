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

#Softmax
def softmax(x):
	if len(x.shape) > 1:
		x = np.apply_along_axis(softmax,1,x)
	else:
		e = np.exp(x-max(x))
		x = e/np.sum(e)
	return x

#NeuralNetworks
train_input_vector = []
for lines in train_X:
	arr = np.zeros(count)
	for words in lines:
		arr[uniqueWords[words]] = 1
	train_input_vector.append(arr)

train_input = np.array(train_input_vector)

train_Y_arr = np.zeros((len(train_Y),2))
for i in range(len(train_Y)):
	if train_Y[i] == 0:
		train_Y_arr[i][0]=1
	else:
		train_Y_arr[i][1] = 1
hidden_layer_size = 500
output_layer_size = 2
params = np.random.randn((train_input.shape[1] + 1)*hidden_layer_size + (hidden_layer_size + 1)*output_layer_size)
offset = 0
Theta1 = np.reshape(params[offset:offset+ train_input.shape[1] * hidden_layer_size], (train_input.shape[1], hidden_layer_size))
offset += train_input.shape[1] * hidden_layer_size
bias1 = np.reshape(params[offset:offset + hidden_layer_size], (1, hidden_layer_size))
offset += hidden_layer_size
Theta2 = np.reshape(params[offset:offset + hidden_layer_size * output_layer_size], (hidden_layer_size, output_layer_size))
offset += hidden_layer_size * output_layer_size
bias2 = np.reshape(params[offset:offset + output_layer_size], (1, output_layer_size))
max_iter = 1000
learning_rate = 1
for i in range(max_iter):
	#Forward Propogation
	h = sigmoid(np.dot(train_input,Theta1) + bias1)
	y = sigmoid(np.dot(h,Theta2) + bias2)
	#y = y.reshape((y.shape[0],))
	#H1 = np.zeros(y.shape)
	#for i in range(y.shape[0]):
	#	if y[i] > 0:
	#		H1[i] = np.log(y[i])
	#H2 = np.zeros(y.shape)
	#for i in range(y.shape[0]):
	#	if (1 - y[i]) > 0:
	#		H2[i] = np.log(1 - y[i])
	#S = np.sum(-(train_Y_arr*H1 + (1-train_Y_arr)*H2));
	#print S

	#cost = -np.sum(train_Y_arr * np.log(y))
	#print h, y, cost
	
	#Back Propogation
	error_outer = train_Y_arr - y
	D_outer = error_outer*sigmoid_grad(y) 
	#D_outer = D_outer.reshape((D_outer.shape[0],1))
	error_hidden = D_outer.dot(Theta2.T)
	D_hidden = error_hidden * sigmoid_grad(h)

	Theta2 += h.T.dot(D_outer)*learning_rate
	bias2 += np.sum(D_outer,axis=0,keepdims=True)*learning_rate

	Theta1 += train_input.T.dot(D_hidden)*learning_rate
	bias1 += np.sum(D_hidden,axis=0,keepdims=True)*learning_rate

test_input_vector = []
for lines in test_X:
	arr = np.zeros(count)
	for words in lines:
		if words in uniqueWords:
			arr[uniqueWords[words]] = 1
	test_input_vector.append(arr)
test_input = np.array(test_input_vector)
inner = sigmoid(np.dot(test_input,Theta1) + bias1)
prediction = sigmoid(np.dot(inner, Theta2) + bias2)
'''pred = np.zeros(test_input.shape[0])
for i in range(len(prediction)):
	if np.round(prediction[i][1]) == 1:
		pred[i] = 1'''
test_Y_arr = np.zeros((len(test_Y),2))
for i in range(len(test_Y)):
	if train_Y[i] == 0:
		test_Y_arr[i][0]=1
	else:
		test_Y_arr[i][1] = 1
#pred = pred.reshape((pred.shape[0],1))
print test_Y_arr
print prediction
print 'Accuracy: {0}'.format((prediction == test_Y_arr).sum().astype(float) / prediction.shape[0])


