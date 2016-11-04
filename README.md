# Cars Python Assessment  
Python Developer Evaluation Answer consists of a Command Python Demo Project using SQLite and Python libraries for testing like nose and mock

# Python Developer Evaluation

This evaluation consists of a Python project called ICDB, the Internet Car
Database, which is a SQLite database of cars.

The code is currently able to add and list cars.

## Setup

To install the dependencies, setup a new virtualenv and run:

    python setup.py develop

Then, load some sample data:

    $ icdb -a
      Enter car year [2013]: 2014
    Enter car make [Toyota]: Ferrari
    Enter car model [Camry]: Enzo
    Inserting a 2014 Ferrari Enzo to the database...

To execute the tests, run:

    $ nosetests -sv
    Test that _create_database sets up the cars table. ... ok
    Verify that creating a car with valid values performs the INSERT. ... ok
    Verify that creating a car with empty values returns `None`. ... ok
    Test _get_year() works as we expect it to. ... ok

    ----------------------------------------------------------------------
    Ran 4 tests in 0.014s

    OK

## Goals

To complete this evaluation, you need to:

* Add functionality for replacing the data in the database with data from a
  CSV file; an example is in the csv-data directory.
* Add functionality for updating a car.
* Add functionality for deleting a car.

## Bonus

For bonus points:

* Write unit tests, ideally before the code itself.
* Model the data using objects, and rewrite the database related methods
  using classes / OOP instead.

## All goals and bonus points items have been met and you can see the implentation in source code. 
## Also, i created another command argument parser (-ly) that is pointing to a function that performs a filter by year, and show a car's list by year (filtering search)
