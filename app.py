from flask import Flask, render_template, abort, jsonify, request
from flask import session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask_cors import cross_origin
from werkzeug.utils import secure_filename
import time, json

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'dfewfew123213rwdsgert34tgfd1234trgf'  #csrf feature requires a security key
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:beautiful@paws-database.can16ihez9jf.us-east-2.rds.amazonaws.com:3306/pet_db'
db = SQLAlchemy(app)

class Pet(db.Model):
    id = db.Column(db.Integer, primary_key = True, index = True)
    name = db.Column(db.String(100), unique=True)
    age = db.Column(db.String(100))
    bio = db.Column(db.String(100))
    # user_posted = db.Column(db.String(100), db.ForeignKey('users.id'))
    
class Users(db.Model):
    id = db.Column(db.Integer, primary_key = True, index = True)
    full_name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique = True)
    password = db.Column(db.String(100))
    # pets = db.relationship('Pet', backref = 'userdetail')

# db.create_all()

# print("DB created")
# team = Users(full_name = "Pet Rescue Team", email = "team@petrescue.co", password = "adminpass")
# db.session.add(team)

# nelly = Pet(name = "Nelly", age = "5 weeks", bio = "I am a tiny kitten rescued by the good people at Paws Rescue Center. I love squeaky toys and cuddles.")
# yuki = Pet(name = "Yuki", age = "8 months", bio = "I am a handsome gentle-cat. I like to dress up in bow ties.")
# basker = Pet(name = "Basker", age = "1 year", bio = "I love barking. But, I love my friends more.")
# mrfurrkins = Pet(name = "Mr. Furrkins", age = "5 years", bio = "Probably napping.")

# db.session.add(nelly)
# db.session.add(yuki)
# db.session.add(basker)
# db.session.add(mrfurrkins)

# try:
#     db.session.commit()
#     print(" transaction committed ")
# except Exception as identifier:
#     print(" transaction rolledback ")
#     print(identifier)
#     db.session.rollback()
# finally:
#     db.session.close()

@app.route("/cats/<int:cat_id>", methods = ["GET"])
@cross_origin(origin='*')
def get_cat(cat_id):
    idVal = Pet.query.get(cat_id)
    if idVal is None:
        return jsonify({"msg":"Cat not found"}), 404
    return jsonify(id=idVal.id,name=idVal.name,age=idVal.age, bio=idVal.bio, file='https://scontent.fmaa3-1.fna.fbcdn.net/v/t1.0-9/38880903_1827657290621505_5314204949926641664_o.jpg?_nc_cat=100&_nc_sid=09cbfe&_nc_ohc=v5I77zpYaQcAX_IKZa7&_nc_ht=scontent.fmaa3-1.fna&oh=72819b829be0ce81eeb3427b42f58700&oe=5FB4F1F5'), 200

@app.route("/cats", methods = ["GET"])
@cross_origin(origin='*')
def get_all_cat():
    catList = Pet.query.all()
    finalRes = []
    for i in catList:
        finalRes.append({"id":i.id, "name":i.name, "age":i.age, "bio":i.bio, "file":'https://scontent.fmaa3-1.fna.fbcdn.net/v/t1.0-9/38880903_1827657290621505_5314204949926641664_o.jpg?_nc_cat=100&_nc_sid=09cbfe&_nc_ohc=v5I77zpYaQcAX_IKZa7&_nc_ht=scontent.fmaa3-1.fna&oh=72819b829be0ce81eeb3427b42f58700&oe=5FB4F1F5'})
    finalResDict = {"data": finalRes}    
    return jsonify(finalResDict), 200

@app.route("/cats/<int:cat_id>", methods = ["DELETE"])
def delete_cat(cat_id):
    delVal = Pet.query.get(cat_id)
    if delVal is None:
       return jsonify({"msg":"Cat not found"}), 404
    db.session.delete(delVal)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
    return jsonify({}), 204

@app.route("/cats/<int:cat_id>", methods = ["PUT"])
@cross_origin(origin='*')
def edit_cat(cat_id):
    new_cat_content = request.get_json(silent=False)
    idVal = Pet.query.get(cat_id)
    if idVal is None:
        return jsonify({"msg":"Cat not found"}), 404
    idVal.name = new_cat_content["name"]
    idVal.age = new_cat_content["age"]
    idVal.bio = new_cat_content["bio"]
    try:
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({"msg":"Error occured while editing"}), 500
    return jsonify(id=idVal.id,name=idVal.name,age=idVal.age, bio=idVal.bio), 200

@app.route("/cats", methods = ["POST"])
@cross_origin(origin='*')
def add_cat():
    new_cat_content = request.get_json(silent=False)
    
    print('Files',request.files)
    print('Forms',request.form)
    file = request.files.get('file')
    filename = secure_filename('nive.jpg')
    # destination="/".join([target, filename])
    if file:
        file.save(filename)
    else:
        print("In else")

    new_pet = Pet(name = new_cat_content["name"], age = new_cat_content["age"] , bio = new_cat_content["bio"])
    try:
        db.session.add(new_pet)
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({"msg":"Error occured while adding"}), 500
    return jsonify(id=new_pet.id,name=new_pet.name,age=new_pet.age, bio=new_pet.bio), 200

if __name__ == "__main__":
    app.run(debug = True, host = "127.0.0.1", port = 5000)

