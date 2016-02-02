#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
*******************************
Test: csv_tools.services.insert_csv.py
*******************************
"""

import sys

import six

try:
    import unittest2 as unittest
    from mock import patch
except ImportError:
    import unittest
    from mock import patch

from csv_tools.services.insert_csv import InsertCSV, launch_new_instance
from tests.utils import stdin_as_string

__author__ = "Daniel Melichar"
__copyright__ = "Copyright 2015"
__credits__ = ["Daniel Melichar"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Daniel Melichar"
__email__ = "dmelichar@student.tgm.ac.at"
__status__ = "Deployed"

class TestInsertCSV(unittest.TestCase):
    def test_launch_new_instance(self):
        with patch.object(sys, 'argv', ['InsertCSV', 'examples/test_data_good.csv']):
            launch_new_instance()

    def test_create_table(self):
        args = ['--table', 'foo', 'examples/test_data_good.csv']
        output_file = six.StringIO()

        utility = InsertCSV(args, output_file)
        utility.main()

        sql = output_file.getvalue()

        self.assertTrue('CREATE TABLE foo' in sql)
        self.assertTrue('text VARCHAR(17) NOT NULL' in sql)
        self.assertTrue('date DATE' in sql)
        self.assertTrue('integer INTEGER' in sql)
        self.assertTrue('boolean BOOLEAN' in sql)
        self.assertTrue('float FLOAT' in sql)
        self.assertTrue('time TIME' in sql)
        self.assertTrue('datetime DATETIME' in sql)

    def test_stdin(self):
        args = ['--table', 'foo']
        output_file = six.StringIO()

        input_file = six.StringIO('a,b,c\n1,2,3\n')

        with stdin_as_string(input_file):
            utility = InsertCSV(args, output_file)
            utility.main()

            sql = output_file.getvalue()

            self.assertTrue('CREATE TABLE foo' in sql)
            self.assertTrue('a INTEGER NOT NULL' in sql)
            self.assertTrue('b INTEGER NOT NULL' in sql)
            self.assertTrue('c INTEGER NOT NULL' in sql)

    def test_stdin_and_filename(self):
        args = ['examples/test_data_good.csv']
        output_file = six.StringIO()

        input_file = six.StringIO("a,b,c\n1,2,3\n")

        with stdin_as_string(input_file):
            utility = InsertCSV(args, output_file)
            utility.main()

            sql = output_file.getvalue()

            self.assertTrue('CREATE TABLE stdin' in sql)
            self.assertTrue('CREATE TABLE dummy' in sql)