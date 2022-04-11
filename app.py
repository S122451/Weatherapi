from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import Column, Integer, String, ForeignKey
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
import markdown
import markdown.extensions.fenced_code
from pygments.formatters import HtmlFormatter
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="WSBeg",
    password="",
    hostname="WSBeg.mysql.pythonanywhere-services.com",
    databasename="WSBeg$weerAPIdb",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"  # aanpassen!

db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)

@app.cli.command("db_create")
def db_create():
    db.create_all()
    print("Databank aangemaakt!")


@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print("Databank verwijderd!")


@app.cli.command('db_seed')
def db_seed():
    CountryBelgium = landdb(naam="Belgie")
    CountryNether = landdb(naam="Nederland")
    CountryFran = landdb(naam="Frankrijk")
    CountryGermn = landdb(naam="Duitsland")

    WeatherinfoOne = weerdb(id="1",idland="2",weerdatum="07-03-2022",mintemp="-1", maxtemp="7",zonneschijn="80", neerslagkans="0",windkracht="2", windrichting="o")
    WeatherinfoTwo = weerdb(id="2",idland="1", weerdatum="07-03-2022", mintemp="-3", maxtemp="8", zonneschijn="0", neerslagkans="0", windkracht="2", windrichting="o")
    WeatherinfoThree = weerdb(id="3",idland="3", weerdatum="07-03-2022", mintemp="0", maxtemp="8", zonneschijn="0", neerslagkans="10", windkracht="4", windrichting="z")
    WeatherinfoFour = weerdb(id="4",idland="4", weerdatum="07-03-2022", mintemp="-4", maxtemp="9", zonneschijn="0", neerslagkans="60", windkracht="3", windrichting="n")

    testgebruiker = User(voornaam="Wurud",
                     familienaam="Salih",
                     email="wurud.salih@ap.be",
                     wachtwoord="test")

    db.session.add(CountryBelgium)
    db.session.add(CountryNether)
    db.session.add(CountryFran)
    db.session.add(CountryGermn)

    db.session.add(WeatherinfoOne)
    db.session.add(WeatherinfoTwo)
    db.session.add(WeatherinfoThree)
    db.session.add(WeatherinfoFour)

    db.session.add(testgebruiker)
    db.session.commit()
    print("Database voorzien van data")

@app.route('/')
def verwelkom():
    return "Welkom tot de weer API"

@app.route('/home')
def info():
    readme_file = open("README.md", "r")
    md_template_string = markdown.markdown(
        readme_file.read(), extensions=["fenced_code", "codehilite"]
    )
    formatter = HtmlFormatter(style="emacs", full=True, cssclass="codehilite")
    css_string = formatter.get_style_defs()
    md_css_string = "<style>" + css_string + "</style>"
    md_template = md_css_string + md_template_string
    return md_template

#Verschillende landen worden getoond
@app.route("/weer/land",methods=["GET"])
def weerland():
    land_list = landdb.query.all()
    result = land_schema.dump(land_list)
    return jsonify(result), 200

#Haalt weer data op
@app.route("/weer/info",methods=["GET"])
def weeerinf():
    weerinf_list = weerdb.query.all()
    result = weather_schema.dump(weerinf_list)
    return jsonify(result), 200
#Haalt alle weer data op van de gekozen land
@app.route("/weer/<string:landAR>",methods=["GET"])
def weerinfoweek(landAR: String):
    Updata = landdb.query.filter_by(naam=landAR)
    if Updata:
        result = land_schema.dump(Updata)
        resultweer = weerdb.query.filter_by(idland=result[0]['id'])
        resulttwo = weather_schema.dump(resultweer)
        return jsonify(resulttwo), 200
    else:
        return jsonify(message="Deze land bestaat nog niet in de lijst"), 404

#Haalt weer data op van gekozen land en datum
@app.route("/weer/<string:landAR>/<string:DatumR>",methods=["GET"])
def weerinfodate(landAR: String,DatumR: String):
    Updata = landdb.query.filter_by(naam=landAR)
    if Updata:
        result = land_schema.dump(Updata)
        Resultinfo = weerdb.query.filter_by(idland=result[0]['id']).filter_by(weatherdate=DatumR)
        resulttwo = weather_schema.dump(Resultinfo)
        return jsonify(resulttwo), 200
    else:
        return jsonify(message="Deze land bestaat nog niet in de lijst"), 404

#Registeren van nieuwe gebruiker
@app.route("/weer/registreren", methods=["POST"])
def registreren():
    email = request.form["email"]
    test = User.query.filter_by(email=email).first()
    if test:
        return jsonify(message="Dit email-adres bestaat reeds"), 409
    else:
        voornaam = request.form["voornaam"]
        familienaam = request.form["familienaam"]
        wachtwoord = request.form["wachtwoord"]
        user = User(voornaam=voornaam, familienaam=familienaam, email=email, wachtwoord=wachtwoord)
        db.session.add(user)
        db.session.commit()
        return jsonify(message="Gebruiker met succes aangemaakt"), 201

#inloggen van gebruiker
@app.route("/weer/login", methods=["POST"])
def login():
    if request.is_json:
        email = request.json["email"]
        wachtwoord = request.json["wachtwoord"]
    else:
        email = request.form["email"]
        wachtwoord = request.form["wachtwoord"]

    test = User.query.filter_by(email=email, wachtwoord=wachtwoord).first()
    if test:
        access_token = create_access_token(identity=email)
        return jsonify(message="Login succesvol!", access_token=access_token)
    else:
        return jsonify(message="Fout email of wachtwoord"), 401

#Ophalen en wijzigen van weerdata
@app.route("/weer/update", methods=["PUT"])
@jwt_required()
def update_weerinfo():
    id = int(request.form["id"])
    weerlist = weerdb.query.filter_by(id=id).first()
    if weerlist:
        weerlist.idland = request.form["idland"]
        weerlist.weerdatum = request.form["weerdatum"]
        weerlist.mintemp = request.form["mintemp"]
        weerlist.maxtemp = request.form["maxtemp"]
        weerlist.zonneschijn = request.form["zonneschijn"]
        weerlist.windkracht = request.form["windkracht"]
        weerlist.windrichting = request.form["windrichting"]

        db.session.commit()
        return jsonify(message="De weer info is aangepast"), 202
    else:
        return jsonify(message="De weer info die je wilde aanpassen is niet verwerkt."), 404

#Verwijderen van weer data
@app.route("/weer/verwijder_weer/<int:id>", methods=["DELETE"])
@jwt_required()
def verwijder_weer(id: int):
    weerlist = weerdb.query.filter_by(id=id).first()
    if weerlist:
        db.session.delete(weerlist)
        db.session.commit()
        return jsonify(message="De gekozen weer data werd met succes verwijderd"), 202
    else:
        return jsonify(message="De gekozen weer data die je wilde verwijderen bestaat niet"), 404

#Verwijderen van speficiek land
@app.route("/weer/verwijder_land/<int:id>", methods=["DELETE"])
@jwt_required()
def verwijder_land(id: int):

    land = landdb.query.filter_by(id=id).first()

    if land:
        weerdb.query.filter_by(idland=id).delete()
        db.session.delete(land)
        db.session.commit()
        return jsonify(message="De gekozen land data werd met succes verwijderd"), 202
    else:
        return jsonify(message="De gekozen land data die je wilde verwijderen bestaat niet"), 404

#toevoegen van weerdata
@app.route("/weer/nieuwe_weerdata", methods=["POST"])
@jwt_required()
def nieuwe_weerdata():
    land = request.form["idland"]
    datum = request.form["weerdatum"]
    test = weerdb.query.filter_by(idland=land).filter_by(weerdatum=datum).first()

    if test:
        return jsonify("Er bestaat reeds een weer data met hetzelfde datum"), 409
    else:
        nieuwe_weerdata = weerdb(
                                 id=request.form["id"],
                                 idland=land,
                                 weerdatum=datum,
                                 mintemp=request.form["mintemp"],
                                 maxtemp=request.form["maxtemp"],
                                 zonneschijn=request.form["zonneschijn"],
                                 neerslagkans=request.form["neerslagkans"],
                                 windkracht=request.form["windkracht"],
                                 windrichting=request.form["windrichting"],
                                 )
        db.session.add(nieuwe_weerdata)
        db.session.commit()
        return jsonify(message="De nieuwe weer data is toegevoegd"), 201

#toevoegen van een land
@app.route("/weer/nieuwe_land", methods=["POST"])
@jwt_required()
def nieuwe_landdata():
    land = request.form["naam"]
    test = landdb.query.filter_by(naam=land).first()

    if test:
        return jsonify("De land bestaat reeds al"), 409
    else:
        nieuwe_land = landdb(naam=land)
        db.session.add(nieuwe_land)
        db.session.commit()
        return jsonify(message="De nieuwe land data is toegevoegd"), 201

# database models
class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    voornaam = Column(String)
    familienaam = Column(String)
    email = Column(String, unique=True)
    wachtwoord = Column(String)

class landdb(db.Model):
    __tablename__ = 'land'
    id = Column(Integer, primary_key=True)
    naam = Column(String)

class weerdb(db.Model):
    __tablename__ = 'weer'
    id = Column(Integer, primary_key=True)
    idland = Column(Integer, ForeignKey('land.id'), primary_key=True)
    weerdatum = Column(String)
    mintemp = Column(Integer)
    maxtemp = Column(Integer)
    zonneschijn = Column(Integer)
    neerslagkans = Column(Integer)
    windkracht = Column(Integer)
    windrichting = Column(String)

class LandSchema(ma.Schema):
    class Meta:
        fields = ("id", "naam")

class WeatherSchema(ma.Schema):
    class Meta:
        fields = ("id", "idland","weerdatum","mintemp", "maxtemp","zonneschijn", "neerslagkans","windkracht", "windrichting")

class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "voornaam", "familienaam", "email", "wachtwoord")

userschema = UserSchema()
usersschema = UserSchema(many=True)

land_schema = LandSchema()
land_schema = LandSchema(many=True)

weather_schema = WeatherSchema()
weather_schema = WeatherSchema(many=True)

if __name__ == '__main__':
    app.run()
