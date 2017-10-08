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