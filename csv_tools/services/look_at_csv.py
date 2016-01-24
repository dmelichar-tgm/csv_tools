#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**************************
Print a CSV to the Console
**************************

This basic script prints the content of a CSV file
to the console it was executed from
"""

import itertools

import six

from csv_tools import CSVToolsReader
from csv_tools.cli import CSVToolsUtility
from csv_tools.headers import make_default_headers

__author__ = "Daniel Melichar"
__copyright__ = "Copyright 2015"
__credits__ = ["Daniel Melichar"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Daniel Melichar"
__email__ = "dmelichar@student.tgm.ac.at"
__status__ = "Deployed"

class LookAtCSV(CSVToolsUtility):
    description = 'Render a CSV file in the console as a fixed-width table.'

    def add_arguments(self):
        pass

    def main(self):
        rows = CSVToolsReader(self.input_file, **self.reader_kwargs)

        # Make a default header row if none exists
        if self.args.no_header_row:
            row = next(rows)

            column_names = make_default_headers(len(row))

            # Put the row back on top
            rows = itertools.chain([row], rows)
        else:
            column_names = next(rows)

        column_names = list(column_names)

        # prepend 'line_number' column with line numbers if --linenumbers option
        if self.args.line_numbers:
            column_names.insert(0, 'line_number')
            rows = [list(itertools.chain([str(i + 1)], row)) for i, row in enumerate(rows)]


        # Convert to normal list of rows
        rows = list(rows)

        # Insert the column names at the top
        rows.insert(0, column_names)

        widths = []

        for row in rows:
            for i, v in enumerate(row):
                try:
                    if len(v) > widths[i]:
                        widths[i] = len(v)
                except IndexError:
                    widths.append(len(v))

        # Dashes span each width with '+' character at intersection of
        # horizontal and vertical dividers.
        divider = '|--' + '-+-'.join('-'* w for w in widths) + '--|'

        self.output_file.write('%s\n' % divider)

        for i, row in enumerate(rows):
            output = []

            for j, d in enumerate(row):
                if d is None:
                    d = ''
                output.append(' %s ' % six.text_type(d).ljust(widths[j]))

            self.output_file.write('| %s |\n' % ('|'.join(output)))

            if (i == 0 or i == len(rows) - 1):
                self.output_file.write('%s\n' % divider)

def launch_new_instance():
    utility = LookAtCSV()
    utility.main()

if __name__ == "__main__":
    launch_new_instance()