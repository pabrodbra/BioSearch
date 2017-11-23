# BioSearch

BioSearch is a web services which provides information relating pathways, reactions and proteins from different databases using semantic searches.

## Getting Started

To run BioSearch on your local computer we recommend you to have installed Python 3.5.2 since it was the version this project was developed.

* `git remote add origin https://github.com/pabrodbra/BioSearch.git`

### Prerequisites

We recommend you to create a virtualenv for this project. To install it do the following:

* `apt-get install python3`
* `apt-get install virtualenv`

To create the virtualenv:

* `virtualenv -p python3 BioSearch`

And to activate it:

* `cd BioSearch`
* `source bin/activate`

### Installing

Ńow that our environment is setup, we install the packages needed: Django (1.11.7) and SPARQLWrapper (1.8.0)

* `pip install django==1.11.7`
* `pip install SPARQLWrapper==1.8.0`

To setup Django now execute the following commands:

* `python manage.py migrate`
* `python manage.py createsuperuser`

## Deployment

Lastly, we should be able to run BioSearch locally with:

*· To modify the ip and port use `python manage.py runserver 0.0.0.0:8000`

Example URL:

```
localhost:8000
```

## Authors

* **Juan Ignacio Alvarez** - *QUE PONGO* - [juanjuanignacio](https://github.com/juanjuanignacio)
* **Guillermo Lopez Garcia** - *QUE PONGO* - [guilopgar](https://github.com/guilopgar)
* **Pablo Rodriguez Brazzarola** - *QUE PONGO* - [pabrodbra](https://github.com/pabrodbra)