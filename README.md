# Make Me Up
Developed by Lindsay Bangs 100858480

## List of Files
•	colour_classifier.py
•	mm_database.py
•	neural_network.py
•	server.py
•	style_engine.py
•	data/
	o	colours.json
	o	eyeshadow.csv
	o	lipsticks.csv
	o	makemeup.db
	o	temps.csv
•	static/	
	o	images/
•	templates/
	o	classification.html
	o	index.html
	o	user_profile.html

## Requirements
The code for Make Me Up was written with `Python 2.7` and leverages a `sqlite3` database.  Both are included with MacOS.
Note: for the server to successfully run, the database must already exist with the correct tables.

The dependencies for Python are as follows
-	sqlite3
-	Flask
-	Numpy

## Command (Unix)
`export FLASK_APP=server.py`
`python -m flask run`

The URL of the application is
`http://localhost:5000/`
