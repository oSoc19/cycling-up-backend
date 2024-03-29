==============
Cycling Up API
==============

API for bicycle infrastructure dashboard, created for Brussels Mobility.
The API fetches and processes raw data, as well as data fetched from Mobigis, and 
provides a way to access this data.

Specific routes, their paramters and return types can be found in the documentation, 
which is accessed by following the trivial route: ``/``


Getting started
===============

Installing and running locally
------------------------------

The API can be run in Python on your local operating system for develompent and debugging purposes.

Prerequisites are:

- python 3      https://www.python.org/download/releases/3.0/
- pipenv        https://docs.pipenv.org/

Run the following commands from the cycling-up-backend directory:

.. code-block:: bash

    $ pipenv install --dev && pipenv shell   # Install pipenv packages
    $ cp .env.example .env                   # Add the .env file
    $ python3 process/__init__.py            # Initialize required data
    $ python3 app.py                         # Start the embedded Flask server

Now the API can be accessed at http://localhost:5000


Installing and running with Docker
----------------------------------

You can build the application as a Docker image and run it:

* using the `start.sh` script

.. code-block:: bash

    $ bash start.sh

* or manually

.. code-block:: bash

    $ docker build --tag cycling-up-api .
    $ docker run -it -p 5005:5000 --rm cycling-up-api

Now the API can be accessed at http://localhost:5005

File structure
==============

The most important files and a small description are listed here:

::

    cycling-up-backend
    |
    ├── Dockerfile              # Configuration file for Docker.
    ├── Pipfile                 # List of required Python libraries (used by pipenv).
    ├── app.py                  # Main implementation file of the backend app.
    ├── config.py               # Contains most of the the configuration variables.
    ├── start.sh                # Bash script to execute the Docker image. Used in the production server.
    ├── api                     # Directory with all code needed to run API.
    │   ├── error_handlers.py       # Defines error handlers for all supported HTTP error codes.
    │   ├── getters.py              # Defines all getters for retrieving requested data.
    │   ├── routes.py               # Defines all supported API routes.
    │   └── swagger                 # Directory with all .yml API documentation files (used by flassger)
    │       └── ...
    ├── data                    # Directory from where API fetches data.
    │   └── ...
    ├── date_matching           # Directory with everything needed to match construction dates to infrastructure.
    │   └── ...
    ├── process                 # Directory with everything required for populating /data directory.
    │   ├── base_data               # All raw data (to be updated manually).
    │   │   └── ...
    │   ├── charts                  # Scripts for populating data/charts directory.
    │   │   └── ...
    │   ├── construction_date       # Scripts for populating data/infra_dates directory.
    │   │   └── ...
    │   ├── fetch_mobigis           # Scripts for populating data/mobigis directory.
    │   │   └── ...
    │   └── __init__.py             # Runs all required scripts for populating the data/ directory properly.
    └── ...