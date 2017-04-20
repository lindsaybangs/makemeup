from __future__ import division

import csv
import mm_database as db
import colour_classifier
from colour_classifier import *

e_id_index = 0
e_bold_index = 4
e_temp_index = 5
e_like_index = 12
e_dislike_index = 13
e_wear_index = 15

l_id_index = 16
l_bold_index = 20
l_colour_index = 21
l_like_index = 25
l_dislike_index = 26
l_wear_index = 27

user = {}
def get_user():
	if not user:
		user['username'] = 'Lindsay'
		user['hair_colour'] = 'BLONDE'
		user['eye_colour'] = 'BLUE'
		user['skin_temperature'] = 'COOL'
		user['skin_tone'] = 15
	return user

def set_user(new_user):
	user['username'] = new_user['username']
	user['hair_colour'] = new_user['hair_colour']
	user['eye_colour'] = new_user['eye_colour']
	user['skin_temperature'] = new_user['skin_temperature']
	user['skin_tone'] = int(new_user['skin_tone'])

	#Update the database for a new user
	reset_likes()
	reset_wears()
	initalization()


def initalization():
	print("initialization")
	colour_index_list = [0, 16, 6, 7, 8, 9, 10, 11, 22, 23, 24]
	eyeshadows, lipsticks = db.initialize()

	# Create pairs of data
	pairs = []
	for e in eyeshadows:
		for l in lipsticks:
			pairs.append(e + l)

	# Get the score for each pair together
	# Save the pair and the score in the database
	rows = []
	for pair in pairs:
		e_id = pair[e_id_index]
		l_id = pair[l_id_index]
		score, popularity = determine_score(pair)
		rows.append([e_id, l_id, score, popularity])
	db.create_pairs(rows)



def determine_score(pair):

	wears = (pair[e_wear_index] + pair[l_wear_index]) / 2

	likes, dislikes = determine_relationship(pair)
	#print('likes: {0}  dislikes: {1}'.format(likes, dislikes))
	likes += pair[e_like_index] + pair[l_like_index]
	dislikes += pair[e_dislike_index] + pair[l_dislike_index]
	#print('likes: {0}  dislikes: {1}'.format(likes, dislikes))

	score = (likes - dislikes) / (likes + dislikes + 1)
	pop = score - (0.03 * wears)
	return score, pop


def determine_relationship(pair):

	# Go through each of the Style Rules
	# General rules for matching the eyeshadow and lipstick to each other
	positive = 0
	negative = 0
	
	# Do not pair a bold lip and bold eye
	if pair[e_bold_index] == 'BOLD' and pair[l_bold_index] == 'BOLD':
		negative = negative + 1

	# Pair a bold eye with a subtle lip
	if pair[e_bold_index] == 'BOLD' and pair[l_bold_index] == 'NUDE':
		positive = positive + 1
	# Pair a bold lip with a subtle eye
	if pair[e_bold_index] == 'SUBTLE' and pair[l_bold_index] == 'BOLD':
		positive = positive + 1

	# Pair a warm eyeshadow with a warm lip
	lipstick_temp = 'WARM' if pair[l_colour_index] > pair[l_colour_index + 2] else 'COOL'
	if pair[e_temp_index] == lipstick_temp:
		positive = positive + 1
	else:
		negative = negative + 1

	# Compare the makeup with the user
	if lipstick_temp == user['skin_temperature']:
		positive += 1
	else:
		negative += 1

	# Get the closest colour name of the eyeshadow
	cc = ColourClassifier()
	primary_colour = cc.classify(pair[6], pair[7], pair[8])
	secondary_colour = cc.classify(pair[9], pair[10], pair[11])

	# Determine the correct eyeshadow colours for their eye colour
	if user['eye_colour'] == 'BROWN':
		if primary_colour in brown_eyes and secondary_colour in brown_eyes:
			positive += 1

	if user['eye_colour'] == 'BLUE':
		if primary_colour in blue_eyes and secondary_colour in blue_eyes:
			positive += 1

	if user['eye_colour'] == "GREEN":
		if primary_colour in green_eyes and secondary_colour in green_eyes:
			positive += 1

	return positive, negative

def get_recommendations():
	top_results = db.get_top_n_pairs(25)
	# we have the id's for the top 25 eyeshadows and top 25 lipsticks
	results = []
	for pair in top_results:
		res = {}
		res['eyeshadow_id'] = pair[0]
		res['lipstick_id'] = pair[1]
		res['score'] = pair[2]
		res['popularity'] = pair[3]

		# Get the info for the matching eyeshadow
		eyeshadow = db.get_eyeshadow_for_id(pair[0])
		# Get the info for the matching lipstick
		lipstick = db.get_lipstick_for_id(pair[1])
		res['eyeshadow_comp'] = eyeshadow[2]
		res['eyeshadow_name'] = eyeshadow[3]
		res['lipstick_comp'] = lipstick[2]
		res['lipstick_name'] = lipstick[3]
		res['likes'] = eyeshadow[12] + lipstick[9]
		res['dislikes'] = eyeshadow[13] + lipstick[10]
		res['wears'] = eyeshadow[15] + lipstick[11]
		results.append(res)


	return results

def like(eyeshadow_id, lipstick_id):
	print("style_engine liking")
	db.increment_likes(eyeshadow_id, lipstick_id)

def dislike(eyeshadow_id, lipstick_id):
	print("style_engine disliking")
	db.increment_dislikes(eyeshadow_id, lipstick_id)

def wear(eyeshadow_id, lipstick_id):
	db.increment_wears(eyeshadow_id, lipstick_id)

def reset_likes():
	db.reset_likes_dislikes()

def reset_wears():
	db.reset_wears()

def update_scores():
	initalization();

def reset():
	user['username'] = 'Lindsay'
	user['hair_colour'] = 'BLONDE'
	user['eye_colour'] = 'BLUE'
	user['skin_temperature'] = 'COOL'
	user['skin_tone'] = 15
	initalization()


def main():
	print("Style Engine")
	# Default user
	reset()

if __name__ == "__main__": main()