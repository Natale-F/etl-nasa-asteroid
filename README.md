# etl-nasa-asteroid

Simple ETL project that request the asteroids's Nasa API to get weekly asteroids near to Earth (today -7 days) with corresponding informations, then load it 
into a postgre database.

The pipeline is done using [prefect](https://www.prefect.io/) package To discover this technology.

## Installation

Associated Python version: Python 3.10

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install project's dependencies.

```bash
pip install -r requirements.txt
```

**You need some ENV variables** to use this project use the .env.example file & fill it with a postgresql database 
credentials & get an api key using this [link](https://api.nasa.gov/).
Then put these informations in a .env file using the given template.


## Run locally the flow

First install dependencies using above command, then run at the project's root:
```bash
python flow_service.py
```

## Launch test

Install dependencies, then run 
```bash
pytest tests
```

## Project's structure

- **src**: contains the ETL codes & logger function.
- **tests**: contains code's associated tests.


## Roadmap

- Deploy this pipeline in GCP to be run every day
  - create a prefect server & configure it to be accessible
  - integrate this pipeline
  - improve production environment (understand how prefect deploy pipeline & optimize it)
- Improve the ETL (more columns ?, more tables ?, ...)
- do something with collected data !