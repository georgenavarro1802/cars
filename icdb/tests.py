import unittest

import mock

from .db import _create_database, db_cursor
from .process import _get_year, create_car, delete_car, _get_element, import_cars, list_cars, list_cars_by_year


class IcdbProcessTestCases(unittest.TestCase):
    @mock.patch('icdb.process.get_input')
    def test_get_year(self, mock_get_input):
        """
            Test _get_year() works as we expect it to.
        """
        mock_get_input.return_value = "0001"
        self.assertEquals(_get_year(), "0001")

    # (bonus points)
    @mock.patch('icdb.process.get_input')
    def test_get_element(self, mock_get_input):
        """
            Test _get_element() works as we expect it to.
        """
        mock_get_input.return_value = "10"
        self.assertEquals(_get_element(), "10")

    # (bonus points)
    @mock.patch('icdb.process.db_cursor')
    @mock.patch('icdb.process.get_input')
    def test_list_cars(self, mock_get_input, mock_db):
        """
            Test list_cars() works as we expect it to.
        """
        mock_get_input.return_value = "2001"
        list_cars()
        self.assertTrue(mock.call().__enter__().execute('SELECT * FROM cars') in mock_db.mock_calls)

    # (bonus points)
    @mock.patch('icdb.process.db_cursor')
    @mock.patch('icdb.process.get_input')
    def test_list_cars(self, mock_get_input, mock_db):
        """
            Test list_cars_by_year() works as we expect it to.
        """
        mock_get_input.return_value = "2013"
        list_cars_by_year()
        self.assertTrue(mock.call().__enter__().execute('SELECT make, model FROM cars WHERE year={0}'.format("2013")) in mock_db.mock_calls)

    @mock.patch('icdb.process.db_cursor')
    @mock.patch('icdb.process._get_year')
    @mock.patch('icdb.process.get_input')
    def test_create_car_fail(self, mock_get_input, mock_get_year, mock_db):
        """
            Verify that creating a car with empty values returns `None`.
        """
        mock_get_year.return_value = ""
        mock_get_input.return_value = ""
        self.assertIsNone(create_car())

    @mock.patch('icdb.process.db_cursor')
    @mock.patch('icdb.process._get_year')
    @mock.patch('icdb.process.get_input')
    def test_create_car(self, mock_get_input, mock_get_year, mock_db):
        """
            Verify that creating a car with valid values performs the INSERT.
        """
        mock_get_year.return_value = "2001"
        mock_get_input.return_value = "Ford"
        create_car()
        self.assertTrue(mock.call().__enter__().execute('INSERT INTO cars(year, make, model) VALUES (?, ?, ?)',
                                                        ('2001', 'Ford', 'Ford'))
                        in mock_db.mock_calls)

    # (bonus points)
    @mock.patch('icdb.process.db_cursor')
    @mock.patch('icdb.process.get_input')
    def test_delete_car(self, mock_get_input, mock_db):
        """
            Verify that deleting a car with valid element id performs the DELETE.
        """
        mock_get_input.return_value = "2"
        delete_car()
        self.assertTrue(mock.call().__enter__().execute("DELETE FROM cars WHERE Id={:d}".format(int("2")))
                        in mock_db.mock_calls)

    @mock.patch('icdb.process.db_cursor')
    def test_import_car(self, mock_db):
        """
            Verify only if importing a list of car from csv file its performs the INSERT.
        """
        import_cars("csv-data/car-set-1.csv")


class IcdbDbTestCases(unittest.TestCase):

    @mock.patch('icdb.db.sqlite3')
    def test_create_database(self, mock_sqlite3):
        """
            Test that _create_database sets up the cars table.
        """
        mock_cursor = mock.MagicMock()
        mock_sqlite3.connect.return_value = mock_cursor
        _create_database()
        self.assertTrue(mock_cursor.cursor.called)
        mock_cursor.cursor.assert_has_calls([
            mock.call(),
            mock.call().execute('CREATE TABLE cars (Id integer primary key, year integer, make text, model text)'),
            mock.call().close()])
