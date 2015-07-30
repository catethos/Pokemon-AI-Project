import random
import math
import sys
from xml.etree.ElementTree import ElementTree, Element, SubElement, tostring


def parse_csv(csvfile, mode):
	f = open(csvfile, mode)
	retval = []
	for line in f.readlines():
		line = line.split(',')
		newline = [1]
		for val in line:
			newline.append(int(val))
		retval.append(newline)
	f.close()
	return retval

def parse_labels(labelfile):
	f = open(labelfile)
	retval = []
	for line in f.readlines():
		retval.append(int(line) - 5)
	f.close()
	return retval

def vector_multiply(vec1, vec2):
	if (len(vec1) != len(vec2)):
		print "vector_multiply failed"
		print "len(vec1) = " + str(len(vec1)) + " != len(vec2) = " + str(len(vec2))
		print "vec1 = " + str(vec1)
		print "vec2 = " + str(vec2)
	total = 0.0
	for i in range(len(vec1)):
		total += (vec1[i] * vec2[i])
	return total

def sigmoid(z):
	return (1.0 / (1.0 + math.exp(-1 * z)))

def sigmoidPrime(z):
	return (math.exp(z) / ((1.0 + math.exp(z)) * (1.0 + math.exp(z))))

def sigmoid_to_int(z):
	if (z >= 0.5):
		return 1
	else:
		return 0

def FeedForwardNN(examples, classifications, learning_rate, hidden_nodes, iterations, lower_weight_limit, upper_weight_limit):
	W = [[random.uniform(lower_weight_limit, upper_weight_limit) for i in range(len(examples[0]))] for j in range(hidden_nodes)]
	output_W = [random.uniform(lower_weight_limit, upper_weight_limit) for i in range(len(W))]

	for i in range(iterations):
		for count, e in enumerate(examples):
			# forward phase
			z = []
			a = []
			for w in W:
				new_z = vector_multiply(w, e)
				z.append(new_z)
				a.append(sigmoid(new_z))
			output_a = vector_multiply(output_W, z)
			output_z = sigmoid(output_a)

			# backward phase
			output_d = sigmoidPrime(output_a) * (classifications[count] - sigmoid_to_int(output_z))
			for index, w in enumerate(output_W):
				output_W[index] = output_W[index] + (learning_rate * a[index] * output_d)
			d = []
			for index, w in enumerate(output_W):
				d.append(sigmoidPrime(a[index]) * w * output_d)
			for index, w in enumerate(W):
				for j, weight in enumerate(w):
					w[j] = w[j] + (learning_rate * e[j] * d[index])
	return W, output_W

def testNN(hidden_weights, output_weights, x, y):
	return (sigmoid_to_int(sigmoid(vector_multiply(output_weights, [sigmoid(vector_multiply(w, x)) for w in hidden_weights]))) == y)

#load a neural network based on the provided weights
def loadNN(classifications, learning_rate, hidden_nodes, iterations, lower_weight_limit, upper_weight_limit):
	W = [[random.uniform(lower_weight_limit, upper_weight_limit) for i in range(len(examples[0]))] for j in range(hidden_nodes)]
	output_W = [random.uniform(lower_weight_limit, upper_weight_limit) for i in range(len(W))]

	for i in range(iterations):
		for count, e in enumerate(examples):
			# forward phase
			z = []
			a = []
			for w in W:
				new_z = vector_multiply(w, e)
				z.append(new_z)
				a.append(sigmoid(new_z))
			output_a = vector_multiply(output_W, z)
			output_z = sigmoid(output_a)

			# backward phase
			output_d = sigmoidPrime(output_a) * (classifications[count] - sigmoid_to_int(output_z))
			for index, w in enumerate(output_W):
				output_W[index] = output_W[index] + (learning_rate * a[index] * output_d)
			d = []
			for index, w in enumerate(output_W):
				d.append(sigmoidPrime(a[index]) * w * output_d)
			for index, w in enumerate(W):
				for j, weight in enumerate(w):
					w[j] = w[j] + (learning_rate * e[j] * d[index])
	return W, output_W



#Try to parse weights file, if none exists create it
#XML file used as easiest to understand and process
#although not the most space efficient 
'''
Weights will be stored in a graph like structure = G(v,e)
<data>
    <output_node>
        <hidden_node weight=0.1>
            <input_node weight=0.3/>
            <input_node weight=0.3/>
        <hidden_node/>
    </output_node>
    <output_node>
        ...
        ...
    </output_node>
</data>
'''

#load in the file tree
#https://docs.python.org/2/library/xml.etree.elementtree.html
def initWeights(lower_weight_limit, upper_weight_limit, num_inputs, num_hidden):
    return  [[random.uniform(lower_weight_limit, upper_weight_limit) for i in range(num_inputs)] for j in range(num_hidden)]


def parse_xml(xmlfile):
        tree = ElementTree.parse('data/weights.xml')
        root = tree.getroot()
        for child in root:
            print child.tag, child.attrib
            for x in child:
                print x.attrib

	return root

#Writes a tree structure based on weights and XML
def write_xml(weights):
    output_node = Element('output_node')
    for hw in weights[0]:
        hidden_node = SubElement(output_node, "hidden_node")
        hidden_node.text = str(hw)

    #print tostring(output_node) 
    
    tree = ElementTree(output_node)
    tree.write('data/test.xml')
    

#generate a bunch of random weights
weights = initWeights(0,1,30, 3)
write_xml(weights)






'''
for j in range(5, 16):
	print str(j) + " HIDDEN NODES"

        	#trainLabels = parse_labels("trainLabels.csv")

	#testData = parse_csv("testData.csv")
	#testLabels = parse_labels("testLabels.csv")
	hidden_weights, output_weights = FeedForwardNN(trainData, trainLabels, 0.001, j, 1000, -0.5, 0.5)

	trainCorrect = 0
	trainIncorrect = 0

	testCorrect = 0
	testIncorrect = 0

	print ("Testing on training data")
	for index, data in enumerate(trainData):
		if (testNN(hidden_weights, output_weights, data, trainLabels[index])):
			trainCorrect += 1
		else:
			trainIncorrect += 1

	print "Correct: " + str(trainCorrect)
	print "Incorrect: " + str(trainIncorrect)
	print "Result: " + str(float(trainCorrect) / (trainCorrect + trainIncorrect) * 100) + "%"

	print ("Testing on testing data")
	for index, data in enumerate(testData):
		if (testNN(hidden_weights, output_weights, data, testLabels[index])):
			testCorrect += 1
		else:
			testIncorrect += 1

	print "Correct: " + str(testCorrect)
	print "Incorrect: " + str(testIncorrect)
	print "Result: " + str(float(testCorrect) / (testCorrect + testIncorrect) * 100) + "%"

	print "\n"
'''
