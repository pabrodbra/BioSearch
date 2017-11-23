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

Ńow that our environment is setup, we install the packages needed: Django (1.11.7) and SPARQLWrapper (1.8.0)

* `pip install django==1.11.7`
* `pip install SPARQLWrapper==1.8.0`

To setup Django now execute the following commands:

* `python manage.py migrate`
* `python manage.py createsuperuser`

Lastly, we should be able to run BioSearch locally with:

*· To modify the ip and port use `python manage.py runserver 0.0.0.0:8000`

### Installing





* `virtualenv -p python3 tr3s`
* ``
* ``

A step by step series of examples that tell you have to get a development env running

Say what the step will be

```
Give the example
```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone who's code was used
* Inspiration
* etc