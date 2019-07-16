==============================
Cycling UP API
==============================

Bicycle infrastructure dashboard  API for Brussels Mobility

Files
=====

The example application only needs very few files:

* ``config.py``: This file contains most of the configuration
                variables needed by the your app.
* ``app.py``: implementation of the pet shop operations with in-memory storage
* ``app.py``: implementation of the pet shop operations with in-memory storage

* ``api/swagger.yaml``: the pet shop REST API Swagger definition
* ``app.py``: implementation of the pet shop operations with in-memory storage
* ``Pipfile``: list of required Python libraries (used by Pipenv)
* ``Dockerfile``: to build the example as a runnable Docker image
* ``startup.sh``: shell script to execute the Docker image.
                 Used in the production server


Running Locally
===============

You can run the Python application directly on your local operating system (this requires Python 3 and `Pipenv <https://docs.pipenv.org/>`_):

.. code-block:: bash

    $ pipenv install --dev && pipenv shell
    $ cp .env.example .env                  # Add the .env file
    $ python app.py                         # start the embedded Flask server
    $ xdg-open http://localhost:5000        # Open the api on your preferred browser


Running with Docker
===================

You can build the application as a Docker image and run it:

using the `start.sh`_ script
----------------------------

.. code-block:: bash

    $ bash start.sh
    $ xdg-open http://localhost:5000        # Open the api on your preferred browser


or using
.. code-block:: bash

    $ docker build --tag cycling-up-api .
    $ docker run -it -p 5005:8080 --rm cycling-up-api
    $ ./test.sh # do some test HTTP requests
