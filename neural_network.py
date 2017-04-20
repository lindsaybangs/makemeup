from random import seed
from random import randrange
import numpy as np
import csv, math

def loadData(filename):
	lines = csv.reader(open(filename, "rb"))
	y = []
	dataset = list(lines)
	for i in range(len(dataset)):
		dataset[i] = [float(x) for x in dataset[i]]
		y.append(int(dataset[i].pop()))

	return np.asarray(dataset), np.asarray(y)

# Helper function to predict an output (0 or 1)
def predict(model, x):
	W1, b1, W2, b2 = model['W1'], model['b1'], model['W2'], model['b2']
	# Forward propagation
	z1 = x.dot(W1) + b1
	a1 = np.tanh(z1)
	z2 = a1.dot(W2) + b2
	exp_scores = np.exp(z2)
	probs = exp_scores / np.sum(exp_scores, axis=1, keepdims=True)
	return np.argmax(probs, axis=1)


class LearningComponent:
	def __init__(self, X, y):
		self.X = X
		self.y = y
		self.num_examples = len(X)
		self.nn_input_dim = 3
		self.nn_output_dim = 2
		self.epsilon = 0.01 # learning rate for gradient descent
		self.reg_lambda = 0.01 # regularization strength
		self.model = None


	def build_model(self, nn_hdim, num_passes=20000, print_loss=False):
		X = self.X
		y = self.y
		num_examples = self.num_examples
		nn_input_dim = self.nn_input_dim
		nn_output_dim = self.nn_output_dim
		reg_lambda = self.reg_lambda
		epsilon = self.epsilon
		 
		# Initialize the parameters to random values. We need to learn these.
		np.random.seed(0)
		W1 = np.random.randn(nn_input_dim, nn_hdim) / np.sqrt(nn_input_dim)
		b1 = np.zeros((1, nn_hdim))
		W2 = np.random.randn(nn_hdim, nn_output_dim) / np.sqrt(nn_hdim)
		b2 = np.zeros((1, nn_output_dim))
	 
		# This is what we return at the end
		self.model = {}
		 
		# Gradient descent. For each batch...
		for i in xrange(0, num_passes):
	 
			# Forward propagation
			z1 = X.dot(W1) + b1
			a1 = np.tanh(z1)
			z2 = a1.dot(W2) + b2
			exp_scores = np.exp(z2)
			probs = exp_scores / np.sum(exp_scores, axis=1, keepdims=True)
	 
			# Backpropagation
			delta3 = probs
			delta3[range(num_examples), y] -= 1
			dW2 = (a1.T).dot(delta3)
			db2 = np.sum(delta3, axis=0, keepdims=True)
			delta2 = delta3.dot(W2.T) * (1 - np.power(a1, 2))
			dW1 = np.dot(X.T, delta2)
			db1 = np.sum(delta2, axis=0)
	 
			# Add regularization terms
			dW2 += reg_lambda * W2
			dW1 += reg_lambda * W1
	 
			# Gradient descent, each value is updated a little bit and then the loss is compared
			W1 += -epsilon * dW1
			b1 += -epsilon * db1
			W2 += -epsilon * dW2
			b2 += -epsilon * db2
			 
			# Assign new parameters to the model
			self.model = { 'W1': W1, 'b1': b1, 'W2': W2, 'b2': b2}
			 
			# Optionally print the loss.
			# This is expensive because it uses the whole dataset, so we don't want to do it too often.
			if print_loss and i % 1000 == 0:
			  print "Loss after iteration %i: %f" %(i, self.calculate_loss(self.model))
		 
		return self.model
	
	def calculate_loss(self, model):
		W1, b1, W2, b2 = model['W1'], model['b1'], model['W2'], model['b2']
		# Forward propagation to calculate our predictions
		z1 = self.X.dot(W1) + b1
		a1 = np.tanh(z1)
		z2 = a1.dot(W2) + b2
		exp_scores = np.exp(z2)
		probs = exp_scores / np.sum(exp_scores, axis=1, keepdims=True)
		# Calculating the loss
		corect_logprobs = -np.log(probs[range(self.num_examples), self.y])
		data_loss = np.sum(corect_logprobs)
		# Add regulatization term to loss (optional)
		data_loss += self.reg_lambda/2 * (np.sum(np.square(W1)) + np.sum(np.square(W2)))
		return 1./self.num_examples * data_loss

	def get_model(self):
		return self.model

	def kfold_test(self, n_folds):
		dataset = self.generate_data(self.X, self.y)
		folds = cross_validation_split(dataset, n_folds)
		scores = list()
		for fold in folds:
			train_set = list(folds)
			train_set.remove(fold)
			train_set = sum(train_set, [])
			test_set = list()
			for row in fold:
				row_copy = list(row)
				test_set.append(row_copy)
				row_copy[3] = None
			predicted = [predict(self.model, np.asarray([row[0],row[1],row[2]])) for row in fold] 
			actual = [row[3] for row in fold]
			accuracy = accuracy_metric(actual, predicted)
			scores.append(accuracy)
		return scores

	def generate_data(self, xx, yy):
		# convert both from nparray to list
		X = xx.tolist()
		y = yy.tolist()

		for i in range(len(X)):
			X[i].append(y[i])
		return X

def cross_validation_split(dataset, n_folds):
	dataset_split = list()
	dataset_copy = list(dataset)
	fold_size = int(len(dataset) / n_folds)
	for i in range(n_folds):
		fold = list()
		while len(fold) < fold_size:
			index = randrange(len(dataset_copy))
			fold.append(dataset_copy.pop(index))
		dataset_split.append(fold)
	return dataset_split

def accuracy_metric(actual, predicted):
	correct = 0
	for i in range(len(actual)):
		if actual[i] == predicted[i]:
			correct += 1
	return correct / float(len(actual)) * 100.0

def train(layers=4, debug=True):
	X, y = loadData('data/temps.csv')
	global component 
	component = LearningComponent(X, y)
	model = component.build_model(layers, print_loss=debug)

def get_prediction(hexa):
	global component

	if component is None or component.get_model() is None:
		return 'NONE'
	r,g,b = get_hex(hexa)
	x = np.asarray([r,g,b])
	result = predict(component.get_model(), x)
	return 'WARM' if result == 1 else 'COOL'

def get_hex(triplet):
	triplet = triplet.replace("#", "")
	if len(triplet) == 3:
		triplet = triplet[0] + triplet[0] + triplet[1] + triplet[1] + triplet[2] + triplet[2]

	value = int(triplet, 16)
	b = math.floor(value % 256)
	g = math.floor((value / 256) % 256)
	r = math.floor((value / (256*256)) % 256)
	return r,g,b

def kfold_test(n_folds):
	global component
	l = component.kfold_test(n_folds)
	return sum(l) / float(len(l))



component = None

def main():
	print("This script creates a neural network from scratch following that tutorial")
	print(get_prediction('#0000FF'))
	train(layers=4, debug=True)
	print(get_prediction('#0000FF'))
	global component
	print(kfold_test(5))



if __name__ == "__main__": main()