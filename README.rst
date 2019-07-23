==============================
Cycling UP API
==============================

Bicycle infrastructure dashboard  API for Brussels Mobility


Files
==========

::

    cycling-up-backend
    |
    ├── Dockerfile              # Configuration file for Docker.
    ├── Pipfile                 # List of required Python libraries (used by Pipenv)
    ├── app.py                  # Main implementation file of the backend app.
    ├── config.py               # This file contains the configuration variables.
    ├── start.sh                # Shell script to execute the Docker image. Used in the production server.
    ├── api                     # Directory with all scripts needed to run API.
    │   ├── error_handlers.py       # Defines error handlers for all supported HTTP error codes.
    │   ├── getters.py              # Defines all getters for retrieving requested data.
    │   ├── routes.py               # Defines all supported API routes.
    │   └── swagger                 # Directory with all .yml documentation files.
    │       └── ...
    ├── data                    # Directory from where API fetches data.
    │   └── ...
    ├── date_matching           # Directory with everything needed to match construction dates.
    │   └── ...
    ├── logs                    # Directory with all server logs.
    │   └── ...
    ├── process                 # Directory with everything required for populating /data directory.
    │   ├── base_data               # All raw data (to be updated manually)
    │   │   └── ...
    │   ├── charts                  # Scripts for populating data/charts directory.
    │   │   └── ...
    │   ├── construction_date       # Scripts for populating data/infra_dates directory.
    │   │   └── ...
    │   ├── fetch_mobigis           # Scripts for populating data/mobigis directory.
    │   │   └── ...
    │   └── __init__.py             # Runs all required scripts for populating the data/ direcory properly.
    └── ...


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
