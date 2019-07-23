==============================
Cycling UP API
==============================

Bicycle infrastructure dashboard  API for Brussels Mobility

Files
=====

The example application only needs very few files:

* ``config.py`` :        This file contains most of the configuration variables needed by the backend.
* ``app.py`` :           Main implementation file of the backend app.
* ``api/swagger.yaml`` : The cycling-ip REST API Swagger definition.
* ``Pipfile`` :          List of required Python libraries (used by Pipenv)
* ``Dockerfile`` :       To build the example as a runnable Docker image
* ``start.sh`` :         Shell script to execute the Docker image. Used in the production server


Running Locally
===============

You can run the Python application directly on your local operating system (this requires Python 3 and `Pipenv <https://docs.pipenv.org/>`_):

.. code-block:: bash

    $ pipenv install --dev && pipenv shell   # Install pipenv packages
    $ cp .env.example .env                   # Add the .env file
    $ python3 process/__init__.py            # Initialize required data
    $ python3 app.py                         # Start the embedded Flask server

Now the API can be accessed at http://localhost:5000


Running with Docker
===================

You can build the application as a Docker image and run it:

* using the `start.sh` script (API access at http://localhost:5005)

.. code-block:: bash

    $ bash start.sh

* or manually (API access at http://localhost:5005)

.. code-block:: bash

    $ docker build --tag cycling-up-api .
    $ docker run -it -p 5005:5000 --rm cycling-up-api
