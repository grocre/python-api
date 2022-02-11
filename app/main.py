from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:senha@localhost:5432/pythonapi'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

class User(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def asdict(self): 
        return {"id": self.id, "name": self.name}

db.create_all()


@app.route("/users", methods=["GET"])
def getUsers():
    users_object = User.query.all()
    users = [user.asdict() for user in users_object]
    return {"users": users}

@app.route("/user/<id>", methods=["GET"])
def postUser(id):
    user_object = User.query.filter_by(id=id).first()
    user = user_object.asdict()
    return {"user": user}

@app.route("/user", methods=["POST"])
def getUser(): 
    try:
        request_data = request.json
        user = User(name=request_data["name"])
        db.session.add(user)
        db.session.commit()
        return {"status": 200}

    except Exception as e: 
        return {"Error": e} 

@app.route("/user/<id>", methods=["PUT"])
def updateUser(id): 
    try:  
        request_data = request.json
        user_object = User.query.filter_by(id=id).first()
        user_object.name = request_data["name"]
        db.session.add(user_object)
        db.session.commit()
        return {"status": 200}

    except Exception as e:
        return {"Error": e}

@app.route("/user/<id>", methods=["DELETE"])
def deleteUsers(id): 

    user_object = User.query.filter_by(id=id).first()
    try: 
        db.session.delete(user_object)
        db.session.commit()
        return {"status": 200}
        
    except Exception as e: 
        return {"Error": e}