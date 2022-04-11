# Flask Weer API
***Welkom tot de weer Api***
## introductie over Weer API
_________________
Met deze API kun je de weer informatie op halen van verschillende landen. Na het registeren en inloggen kun je ook zo landen, weer data toevoegen of aanpassen en ook nog het verwijderen van weer data en landen.

## Installatie voor de Weer API
_________________
> pip install flask

> pip install SQLAlchemy
 
> pip install flask-marshmallow

> pip install Flask-SQLAlchemy

> pip install Flask-JWT-Extended

## Gebruik van Weer API
_________________
- Tonen van verschillende landen [method:GET]
> (url)/weer/land
- Tonen van alle weerdata [method:GET]
> (url)/weer/info
- Tonen van alle weerdata van speficiek land [method:GET]
> (url)/weer/(landnaam)
- Tonen van alle weerdata van speficiek land en datum [method:GET]
> (url)/weer/(landnaam)/(datum)
> 
> Voorbeeld: (url)/weer/Nederland/08-03-2022

- Registeren van een nieuwe gebruiker [method:POST]
> (url/weer/registreren
- Inloggen van gebruiker [method: POST]
> (url)/weer/login
- Wijzigen van weer data [method:PUT]
> (url)/weer/update
- Verwijderen van weer data [method:DELETE]
> (url)/weer/verwijder_weer/(id)
- Verwijderen van land [method:DELETE]
> (url)/weer/verwijder_land/(id)

### Links
- [Flask](https://pypi.org/project/Flask/)
- [SQLAlchemy](https://pypi.org/project/SQLAlchemy/)
- [flask-marshmallow](https://pypi.org/project/flask-marshmallow/)
- [Flask-SQLAlchemy](https://pypi.org/project/Flask-SQLAlchemy/)
- [Flask-JWT-Extended](https://pypi.org/project/Flask-JWT-Extended/)
- [Postman](https://www.postman.com/)