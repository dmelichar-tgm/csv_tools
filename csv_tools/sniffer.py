#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
*******************
CSV Dialect Sniffer
*******************

This module goes through the common
delimiters and thereby tries to acknowledge the
CSV File's dialect
"""

import csv

__author__ = "Daniel Melichar"
__copyright__ = "Copyright 2015"
__credits__ = ["Daniel Melichar"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Daniel Melichar"
__email__ = "dmelichar@student.tgm.ac.at"
__status__ = "Deployed"


POSSIBLE_DELIMITERS = [',', '\t', ';', ' ', ':', '|']
class Sniffer(object):
    def sniff_dialect(sample):
        """
        A functional version of ``csv.Sniffer().sniff``, that extends the
        list of possible delimiters to include some seen in the wild.
        """
        try:
            dialect = csv.Sniffer().sniff(sample, POSSIBLE_DELIMITERS)
        except:
            dialect = None

        return dialect

    @staticmethod
    def read_file(self, filename):
        with open(filename ,'r') as csv_file:
            sample = csv_file.read(1024)
            dialect = self.sniff_dialect(sample)

            csv_file.seek(0)
            lines = []
            lines_reader = csv.DictReader(csv_file, dialect=dialect)

            for line in lines_reader:
                lines.append(line)

            return lines, lines_reader.fieldnames

    @staticmethod
    def write_file(self, filename, lines, delimiter=';'):

        with open(filename, 'w') as csv_file:
            if len(lines) == 0:
                return

            fieldnames = list(lines[0].keys())
            writer = csv.DictWriter(csv_file, delimiter=delimiter, fieldnames=fieldnames)
            writer.writerow(dict((fn, fn) for fn in fieldnames))

            for line in lines:
                writer.writerow(line)