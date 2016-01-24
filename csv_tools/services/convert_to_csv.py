#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
*********************
Convert a file to CSV
*********************

With this service you can convert the
supported file types into a CSV

For more details, see the the Documentation
for the convert module
"""

from csv_tools import convert
from csv_tools.cli import CSVToolsUtility

__author__ = "Daniel Melichar"
__copyright__ = "Copyright 2015"
__credits__ = ["Daniel Melichar"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Daniel Melichar"
__email__ = "dmelichar@student.tgm.ac.at"
__status__ = "Deployed"


class ConvertToCSV(CSVToolsUtility):
    description = 'Convert common, but less awesome, tabular data formats to CSV.'
    epilog = 'Some command line flags only pertain to specific input formats.'
    override_flags = ['f']

    def add_arguments(self):
        self.argparser.add_argument(metavar="FILE", nargs='?', dest='input_path', help='The CSV file to operate on. If omitted, will accept input on STDIN.')
        self.argparser.add_argument('-f', '--format', dest='filetype', help='The format of the input file. If not specified will be inferred from the file type. Supported formats: %s.' % ', '.join(sorted(convert.SUPPORTED_FORMATS)))
        self.argparser.add_argument('-y', '--snifflimit', dest='snifflimit', type=int, help='Limit CSV dialect sniffing to the specified number of bytes. Specify "0" to disable sniffing entirely.')
        self.argparser.add_argument('--sheet', dest='sheet',help='The name of the XLSX sheet to operate on.')
        self.argparser.add_argument('--no-inference', dest='no_inference', action='store_true', help='Disable type inference when parsing the input.')

    def main(self):

        # Find out what file w're working with
        if self.args.filetype:
            filetype = self.args.filetype

            if filetype not in convert.SUPPORTED_FORMATS:
                self.argparser.error('"%s" is not a supported format' % self.args.filetype)
        else:
            if not self.args.input_path or self.args.input_path == '-':
                self.argparser.error('You must specify a format when providing data via STDIN (pipe).')

            filetype = convert.guess_format(self.args.input_path)

            if not filetype:
                self.argparser.error('Unable to automatically determine the format of the input file. Try specifying a format with --format.')


        # Open the file in the correct manner
        if filetype in ('xls', 'xlsx'):
            self.input_file = open(self.args.input_path, 'rb')
        else:
            self.input_file = self._open_input_file(self.args.input_path)


        # The additional parameters
        kwargs = self.reader_kwargs

        # Do we have a limit on sniffing?
        if self.args.snifflimit:
            kwargs['snifflimit'] = self.args.snifflimit

        # What sheet are we working on?
        if self.args.sheet:
            kwargs['sheet'] = self.args.sheet

        # Do we want to inherit the filetypes
        if self.args.no_inference:
            kwargs['type_inference'] = False

        # Are headers present?
        if filetype == 'csv' and self.args.no_header_row:
            kwargs['no_header_row'] = True

        data = convert.convert(self.input_file, filetype, **kwargs)

        self.output_file.write(data)

def launch_new_instance():
    utility = ConvertToCSV()
    utility.main()


if __name__ == "__main__":
    launch_new_instance()
