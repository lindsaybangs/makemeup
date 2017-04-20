from flask import Flask, request, current_app, render_template, url_for, redirect
app = Flask(__name__)

import style_engine, colour_classifier, neural_network

@app.route("/")
def greeting():
	user = style_engine.get_user()
	recommendations = style_engine.get_recommendations()
	return render_template('index.html', user=user, recommendations=recommendations)

@app.route("/user_profile", methods=['GET'])
def get_profile():
	return render_template('user_profile.html')

@app.route("/user_profile", methods=['POST'])
def update_profile():
	data = request.form
	style_engine.set_user(data)
	return redirect(url_for('greeting'))

@app.route("/user", methods=['GET'])
def get_user():
	# Get the user and convert them into HTML
	user = style_engine.get_user()
	html = "<dl><dt>Username</dt><dd>{un}</dd><dt>Hair Colour</dt><dd>{hc}</dd><dt>Eye Colour</dt><dd>{ec}</dd> \
		<dt>Skin Temperature</dt><dd>{ste}</dd><dt>Skin Tone</dt><dd>{sto}</dd>\
		</dl>".format(un=user['username'], hc=user['hair_colour'], ec=user['eye_colour'], ste=user['skin_temperature'], sto=user['skin_tone'])
	return html

@app.route("/reset", methods=['GET'])
def reset():
	style_engine.reset()
	return "Reset successful"

@app.route("/update_scores", methods=['GET'])
def update_scores():
	style_engine.update_scores()
	return 'success'

@app.route("/like", methods=['POST'])
def update_likes():
	e_id = request.form['e_id']
	l_id = request.form['l_id']
	style_engine.like(e_id, l_id)
	return redirect(url_for('greeting'))

@app.route("/dislike", methods=['POST'])
def update_dislikes():
	e_id = request.form['e_id']
	l_id = request.form['l_id']
	style_engine.dislike(e_id, l_id)
	return redirect(url_for('greeting'))

@app.route("/reset_likes", methods=['GET'])
def reset_likes():
	style_engine.reset_likes()
	return 'success'

@app.route("/wear", methods=['POST'])
def update_wears():
	e_id = request.form['e_id']
	l_id = request.form['l_id']
	style_engine.wear(e_id, l_id)
	return redirect(url_for('greeting'))

@app.route("/reset_wears", methods=['GET'])
def reset_wears():
	style_engine.reset_wears()
	return 'success'

@app.route("/classification", methods=['GET'])
def get_classification():
	return render_template("classification.html")


@app.route("/find_crayola_name", methods=['POST'])
def get_crayola_name():
	cc = colour_classifier.ColourClassifier()
	colour = cc.classify_hex("unknown", request.form['hex_value'])
	return colour

@app.route("/find_temperature", methods=['POST'])
def get_temperature():
	return neural_network.get_prediction(request.form['hex_value'])

@app.route("/train_temperature", methods=['GET'])
def train_temperature():
	neural_network.train(layers=4, debug=False)
	result = neural_network.kfold_test(5)
	return '{0}'.format(result)








