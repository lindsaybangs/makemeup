import math
import json

blue_eyes = ['Cool Gray', 'Antique Brass', 'Dark Chocolate', 'Gray', 'Dark Brown', 'Cocoa', 'Apricot', 'Harvest Gold', 'Ash', 'Light Orange', 'Beaver', 'Plum', 'Peach', 'Mauve', 'Blue Violet', 'Violet (Purple)', 'Pink', 'Raspberry', 'Blush', 'Salmon', 'Bubble Gum', 'Fiery Rose', 'Orchid', 'Warm Gray', 'Brown', 'Light Brown', 'Slate', 'Pale Rose', 'Black', 'Sand', 'Copper', 'Taupe', 'Coral Reef', 'White']
brown_eyes = ['Aqua Green', 'Cerulean', 'Bubble Gum', 'Absolute Zero', 'Apricot', 'Fern', 'Jade Green', 'Green Blue', 'Harvest Gold', 'Fiery Rose', 'Yellow Green', 'Light Blue', 'Lilac', 'Green', 'Magenta', 'Lime Green', 'Granny Smith Apple', 'Olive', 'Plum', 'Sky Blue', 'Mahogany', 'Maroon', 'Mango', 'Blue Bolt', 'Blue', 'Pine Green', 'Mauve', 'Blue Violet', 'Ruby Red', 'Violet (Purple)', 'Pink', 'Raspberry', 'Blush', 'True Blue', 'White', 'Salmon', 'Orchid', 'Brick Red', 'Black', 'Turquoise', 'Sand', 'Coral Reef', 'Teal', 'Cornflower']
green_eyes = ['Black', 'White', 'Taupe', 'Red Orange', 'Orange', 'Cocoa', 'Harvest Gold', 'Dark Chocolate', 'Plum', 'Mauve', 'Blue Violet', 'Pink', 'Orchid', 'Pale Rose', 'Cantaloupe', 'Tan', 'Brown']

class Point:
	def __init__(self, x, y, z, label):
		self.x = x
		self.y = y
		self.z = z
		self.label = label

	def distance(self, point):
		x = abs(point.x - self.x)
		y = abs(point.y - self.y)
		z = abs(point.z - self.z)
		return math.sqrt(x*x + y*y + z*z)

def get_dataset():
	colours = []
	with open('data/colours.json') as file:
		data = json.load(file)

	for row in data:
		p = rgb_from_hex(row['label'], row['hex'])
		colours.append(p)
	return colours

def rgb_from_hex(label, triplet):
	triplet = triplet.replace("#", "")
	if len(triplet) == 3:
		triplet = triplet[0] + triplet[0] + triplet[1] + triplet[1] + triplet[2] + triplet[2]

	value = int(triplet, 16)
	b = math.floor(value % 256)
	g = math.floor((value / 256) % 256)
	r = math.floor((value / (256*256)) % 256)

	#print("{0}: {1},{2},{3}".format(triplet, r, g, b))

	return Point(r, g, b, label)


class ColourClassifier:
	def __init__(self):
		self.data = get_dataset()
		self.last_result = -1

	def learn(self, data):
		self.data = data

	def classify(self, r, g, b):
		new_point = Point(r, g, b, 'unknown')
		minimum = float("inf")
		min_idx = -1

		for i in range(len(self.data)):
			dist = new_point.distance(self.data[i])
			if dist < minimum:
				minimum = dist
				min_idx = i
		self.last_result = min_idx
		return self.data[min_idx].label

	def classify_hex(self, label, hexa):
		point = rgb_from_hex(label, hexa)
		return self.classify(point.x, point.x, point.z)


def main():
	print("Colour Classifier")
	colours = get_dataset()
	cc = ColourClassifier()
	cc.classify(150, 150, 150)


if __name__ == "__main__": main()