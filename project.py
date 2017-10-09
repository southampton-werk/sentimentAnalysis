from random import randrange
import re
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
with open("training.txt") as f:
    content = f.readlines()

content = [x.strip() for x in content]
test_Y = []
train_Y = []
train_X = []
test_X = []
size_train_x = int(0.8*len(content))
stopwords =["i","be","by","at","up","this","was","some","if","have","been","will","and","all","which","last","would","over","on","not","no","it","of","or","in","from","about","were","a","an","the","has","had","for","with","other","its","to","between","is","are","also","before","after","they","their","there","than","but","he","she"]

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
ss = []
#Sentence Scoring

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

for i in range(len(train_X)):
	
	lines = train_X[i]
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

	ss.append(sentence_score)

plt.scatter(ss,train_Y)
plt.axvline(x=0, color='r', linestyle='-')
plt.xlim(np.min(np.array(ss)), np.max(np.array(ss)))
plt.ylim(-1,2)
plt.xlabel("Sentence Score")
plt.ylabel("Sentiment")
plt.show()
#Logistic Regression
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

la = np.linalg
U,s,Vh = la.svd(train_input,full_matrices=False)

zeros_U0 = []
ones_U0 = []

zeros_U1 = []
ones_U1 = []

for i in range(len(U[:,0])):
	if train_Y[i] == 0:
		zeros_U0.append(U[i][0])
	else:
		ones_U0.append(U[i][0])

for i in range(len(U[:,1])):
	if train_Y[i] == 0:
		zeros_U1.append(U[i][1])
	else:
		ones_U1.append(U[i][1])
plt.scatter(zeros_U0,zeros_U1,color='r')
plt.scatter(ones_U0,ones_U1,color='b')
plt.xlim(np.min(U[:,0]),np.max(U[:,0]))
plt.ylim(np.min(U[:,1]),np.max(U[:,1]))
plt.show()

zeros_U2 = []
ones_U2 = []

for i in range(len(U[:,2])):
	if train_Y[i] == 0:
		zeros_U2.append(U[i][2])
	else:
		ones_U2.append(U[i][2])
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(zeros_U0, zeros_U1, zeros_U2, zdir='z', s=20, c='r', depthshade=True)
ax.scatter(ones_U0, ones_U1, ones_U2, zdir='z', s=20, c='b', depthshade=True)
plt.show()