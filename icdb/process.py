"""
        ____
   ____/ / /_
  / __  / __/
 / /_/ / /_
 \__,_/\__/     dealertrack technologies and George collaboration

Welcome to the Internet Car Database v{}
"""
import argparse
import csv
import logging

import sqlite3

from icdb.models import Car
from . import __version__
from .db import db_cursor

# Setup logging
logger = logging.getLogger(__name__)
FORMAT = "%(asctime)-15s %(name)s %(levelname)s %(message)s"
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.ERROR)


def get_input(question):
    return raw_input(question)


def _get_year(year=None):
    """
        Keep asking the user for a year until it is finally valid.
    """
    if year:
        if year.isdigit():
            if len(year) == 4:
                return year

    print("\n")     # better console style
    year = get_input("{:<20}".format("Enter car year [2013]: "))
    return _get_year(year)


def _get_element(ide=None):
    """
        Keep asking the user for an id element until it is finally selected and valid.
    """
    if ide:
        if ide.isdigit():
            return ide

    print("\n")  # better console style
    ide = get_input("{:>30}".format("What element do you want to modify [Id]?: "))
    return _get_element(ide)


def create_car():
    """
        Let the user input parameters to create a new car, and
        insert it to the database.
    """
    try:
        with db_cursor() as db:
            year = _get_year()
            make = get_input("{:>24}".format("Enter car make [Toyota]: "))
            model = get_input("{:>25}".format("Enter car model [Camry]: "))

            # instance of Object Car (Bonus points)
            car = Car(year, make, model)

            # before sentence
            # row = (year, make, model)

            # method to check if object has all the elements valids
            if not car.has_all_elements():
                logger.error("One or more of your answers were empty, please try again.")
                return

            print "Inserting a {} {} {} to the database...".format(year, make, model)
            db.execute("INSERT INTO cars(year, make, model) VALUES (?, ?, ?)", car.get_obj())
    except Exception as ex:
        print(ex.message)


def import_cars(csv_file):
    # opens the csv file
    f = open(csv_file, 'rb')
    try:
        # creates the reader object
        reader = csv.reader(f)
        # skip the first row (header)
        next(reader)
        with db_cursor() as db:
            # delete all records (cause the exercise say that we must replace the data)
            db.execute("DELETE FROM cars")
            # iterates the rows of the file in orders
            for row in reader:
                car = Car(row[0], row[1], row[2])   # one instance of Car for every row to use objects(bonus points)
                print "Inserting a {} {} {} to the database...".format(car.year, car.make, car.model)
                db.execute("INSERT INTO cars(year, make, model) VALUES (?, ?, ?)", car.get_obj())
    finally:
        # closing csv file
        f.close()


def update_car():
    # list all records with elements that will be selected
    list_cars()
    # get the element id from the list
    elem = _get_element()
    try:
        with db_cursor() as db:
            year = _get_year()
            make = get_input("{:<20}".format("Enter new car MAKE: "))
            model = get_input("{:<20}".format("Enter new car MODEL: "))

            # instance of Object Car (Bonus points)
            car = Car(year, make, model)

            # before sentence
            # row = (year, make, model)

            # method to check if object has all the elements valids
            if not car.has_all_elements():
                logger.error("One or more of your answers were empty, please try again.")
                return

            print "Updating a car with Id:{} in the database...".format(elem)
            db.execute("UPDATE cars SET year=?, make=?, model=? WHERE Id=?", (car.year, car.make, car.model, elem))
    except sqlite3.IntegrityError:
        print "Couldn't update the object"
    except Exception as ex:
        print(ex.message)


def delete_car():
    """
        Let the user input parameters to delete car based on.
    """
    list_cars()
    # get the element id from the list
    elem = _get_element()
    print "Deleting a car with Id:{} from the database...".format(elem)
    with db_cursor() as db:
        db.execute("DELETE FROM cars WHERE Id={0}".format(elem))


def list_cars():
    """
        List all cars in the database.
    """
    with db_cursor() as db:
        print("\n")  # better console style
        LAYOUT = "{:<4} {:<4} {:20} {:20}"
        print LAYOUT.format("ID", "Year", "Make", "Model")
        print LAYOUT.format("-" * 4, "-" * 4, "-" * 20, "-" * 20)
        for row in db.execute("SELECT * FROM cars"):
            print LAYOUT.format(*row)


def list_cars_by_year():
    """
        List the cars that belongs to an specific year asked to the user.
    """
    with db_cursor() as db:
        year = _get_year()
        print("\n")  # better console style
        LAYOUT = "{:20} {:20}"
        print LAYOUT.format("List of car filtered by year: ", year)
        print LAYOUT.format("-" * 40, "-")
        print LAYOUT.format("Make", "Model")
        print LAYOUT.format("-" * 20, "-" * 20)
        for row in db.execute("SELECT make, model FROM cars WHERE year={0}".format(year)):
            print LAYOUT.format(*row)


def main():
    parser = argparse.ArgumentParser(description=__doc__.format(__version__), formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-v', '--verbose', action='store_true', help='be verbose')

    actions = parser.add_mutually_exclusive_group(required=True)

    actions.add_argument('-i', '--importcsv', action='store', help='import a CSV file, overwriting the database')

    actions.add_argument('-a', '--add', action='store_true', help='add a car to the database')

    actions.add_argument('-u', '--update', action='store_true', help='update a car in the database')

    actions.add_argument('-d', '--delete', action='store_true', help='delete a car from the database')

    actions.add_argument('-l', '--listcars', action='store_true', help='list the cars in the database')

    actions.add_argument('-ly', '--listcarsyear', action='store_true', help='Cars list in database of an specific year')

    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.INFO)

    if args.importcsv:
        logger.info("importing csv")
        import_cars(args.importcsv)

    if args.add:
        logger.info("adding new car")
        create_car()

    if args.update:
        logger.info("updating a car")
        update_car()

    if args.delete:
        logger.info("deleting a car")
        delete_car()

    if args.listcars:
        logger.info("listing cars")
        list_cars()

    if args.listcarsyear:
        logger.info("listing cars by year")
        list_cars_by_year()
