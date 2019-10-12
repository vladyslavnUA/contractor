from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os


host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/pants')
client = MongoClient(host=host)
db = client.get_default_database()
pants = db.pants


app = Flask(__name__)

# @app.route("/login")
# def login:
# 	auth = request.authorization
# 	return " "

@app.route("/")
def pants_index():
	#this will show the type of pants we have
	return render_template("pants_index.html", pants=pants.find())

@app.route("/pants", methods=["POST"])
def playlists_submit():
	pant = {
		"pants_name": request.form.get("pants_name"),
		"description": request.form.get("description"),
		"price": request.form.get("price"),
        "color": request.form.get("color")
	}
	pant_id = pants.insert_one(pant).inserted_id
	print(pant_id)
	return redirect(url_for("pants_show", pant_id = pant_id))

@app.route("/pants/<pant_id>")
def pants_show(pant_id):
	pant = pants.find_one({'_id' : ObjectId(pant_id)})
	return render_template("pants_show.html", pant = pant)

@app.route("/pants/new")
def pants_new():
	return render_template("pants_new.html", pant ={}, title ="New pant")

@app.route("/pants/<pant_id>/edit")
def pants_edit(pant_id):
	pant = pants.find_one({"_id" : ObjectId(pant_id)})
	return render_template("pants_edit.html", pant = pant, title = "Edit pant")

@app.route("/pants/<pant_id>", methods = ['POST'])
def pants_update(pant_id):
	updated_pant = {
		"pants_name": request.form.get("pants_name"),
		"description": request.form.get("description"),
		"price": request.form.get("price"),
        "color": request.form.get("color")

	}

	pants.update_one( {"_id" : ObjectId(pant_id)}, {"$set" : updated_pant})
	return redirect(url_for("pants_show", pant_id = pant_id))


@app.route("/pants/<pant_id>/delete", methods=["POST"])
def pants_delete(pant_id):
	pants.delete_one({"_id" : ObjectId(pant_id)})
	return redirect(url_for("pants_index"))


if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
