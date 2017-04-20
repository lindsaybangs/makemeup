import sqlite3

db_filename = "data/makemeup.db"
eyeshadow_table = "eyeshadow"
lipstick_table = "lipstick"
pairs_table = "pairs"

# Connecting to the database file

def initialize():
	conn = sqlite3.connect(db_filename)
	c = conn.cursor()

	# Read in makeup from the database
	c.execute('SELECT * FROM {tn}'.format(tn=eyeshadow_table))
	eyeshadows = c.fetchall()

	c.execute('SELECT * FROM {tn}'.format(tn=lipstick_table))
	lipsticks = c.fetchall()

	conn.close()

	return eyeshadows, lipsticks


def create_pairs(rows):
	conn = sqlite3.connect(db_filename)
	c = conn.cursor()
	# Drop the pairs table since we are reinitializing
	c.execute('DELETE FROM {tn}'.format(tn=pairs_table))
	# Insert all of the new pairs
	c.executemany('INSERT into {tn} values (?,?,?,?)'.format(tn=pairs_table), rows)
	conn.commit()

	conn.close()

def get_top_n_pairs(num_pairs):
	conn = sqlite3.connect(db_filename)
	c = conn.cursor()
	c.execute('SELECT * FROM {tn} ORDER BY {cn} DESC LIMIT {lim};'.format(tn=pairs_table, cn="score", lim=num_pairs))
	results = c.fetchall()
	conn.close()
	return results

def get_eyeshadow_for_id(_id):
	conn = sqlite3.connect(db_filename)
	c = conn.cursor()
	c.execute('SELECT * FROM {tn} WHERE {cn} = {id};'.format(tn=eyeshadow_table, cn="id", id=_id))
	result = c.fetchone()
	conn.close()
	return result

def get_lipstick_for_id(_id):
	conn = sqlite3.connect(db_filename)
	c = conn.cursor()
	c.execute('SELECT * FROM {tn} WHERE {cn} = {id};'.format(tn=lipstick_table, cn="id", id=_id))
	result = c.fetchone()
	conn.close()
	return result

def increment_likes(eyeshadow_id, lipstick_id):
	print('database: {0}, {1}'.format(eyeshadow_id, lipstick_id))
	conn = sqlite3.connect(db_filename)
	c = conn.cursor()
	c.execute('UPDATE {tn} SET {cn} = {cn} + 1 WHERE id = {id};'.format(tn=eyeshadow_table, cn="likes", id=eyeshadow_id))
	c.execute('UPDATE {tn} SET {cn} = {cn} + 1 WHERE id = {id};'.format(tn=lipstick_table, cn="likes", id=lipstick_id))
	conn.commit()
	conn.close()

def increment_dislikes(eyeshadow_id, lipstick_id):
	conn = sqlite3.connect(db_filename)
	c = conn.cursor()
	c.execute('UPDATE {tn} SET {cn} = {cn} + 1 WHERE id = {id};'.format(tn=eyeshadow_table, cn="dislikes", id=eyeshadow_id))
	c.execute('UPDATE {tn} SET {cn} = {cn} + 1 WHERE id = {id};'.format(tn=lipstick_table, cn="dislikes", id=lipstick_id))
	conn.commit()
	conn.close()

def increment_wears(eyeshadow_id, lipstick_id):
	conn = sqlite3.connect(db_filename)
	c = conn.cursor()
	c.execute('UPDATE {tn} SET {cn} = {cn} + 1 WHERE id = {id};'.format(tn=eyeshadow_table, cn="wears", id=eyeshadow_id))
	c.execute('UPDATE {tn} SET {cn} = {cn} + 1 WHERE id = {id};'.format(tn=lipstick_table, cn="wear", id=lipstick_id))
	conn.commit()
	conn.close()

def reset_likes_dislikes():
	conn = sqlite3.connect(db_filename)
	c = conn.cursor()
	c.execute('UPDATE {tn} SET {cn} = 0, {cn2} = 0;'.format(tn=eyeshadow_table, cn="likes", cn2="dislikes"))
	c.execute('UPDATE {tn} SET {cn} = 0, {cn2} = 0;'.format(tn=lipstick_table, cn="likes", cn2="dislikes"))
	conn.commit()
	conn.close()	

def reset_wears():
	conn = sqlite3.connect(db_filename)
	c = conn.cursor()
	c.execute('UPDATE {tn} SET {cn} = 0;'.format(tn=eyeshadow_table, cn="wears"))
	c.execute('UPDATE {tn} SET {cn} = 0;'.format(tn=lipstick_table, cn="wear"))
	conn.commit()
	conn.close()

