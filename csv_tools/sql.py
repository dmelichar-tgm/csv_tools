#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**************
SQL Management
**************

This module holds various tools and methods that
are needed for CSV Tools. For example you can
create a Table, create columns, read from a DB, etc.

At the moment, only MySQL, PostgreSQL and SQLLite are working.
However, you can simply add new DBs with the wonderful
SQLAlchemy library.
"""

import datetime

import six

from sqlalchemy import Column, MetaData, Table, create_engine
from sqlalchemy import BigInteger, Boolean, Date, DateTime, Float, Integer, String, Time
from sqlalchemy.schema import CreateTable

__author__ = "Daniel Melichar"
__copyright__ = "Copyright 2015"
__credits__ = ["Daniel Melichar"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Daniel Melichar"
__email__ = "dmelichar@student.tgm.ac.at"
__status__ = "Deployed"

NoneType = type(None)

DIALECTS = {
    'mysql': 'mysql.mysqlconnector',
    'postgresql': 'postgresql.psycopg2',
    'sqlite': 'sqlite.pysqlite'
}

NULL_COLUMN_MAX_LENGTH = 32
SQL_INTEGER_MAX = 2147483647
SQL_INTEGER_MIN = -2147483647

def make_column(column, no_constraints=False):
    """
    Creates a sqlalchemy column from a CSV Tools Column.
    """
    sql_column_kwargs = {}
    sql_type_kwargs = {}

    column_types = {
        bool: Boolean,
        #int: Integer, see special case below
        float: Float,
        datetime.datetime: DateTime,
        datetime.date: Date,
        datetime.time: Time,
        NoneType: String,
        six.text_type: String
    }

    if column.type in column_types:
        sql_column_type = column_types[column.type]
    elif column.type is int:
        column_max = max([v for v in column if v is not None])
        column_min = min([v for v in column if v is not None])

        if column_max > SQL_INTEGER_MAX or column_min < SQL_INTEGER_MIN:
            sql_column_type = BigInteger
        else:
            sql_column_type = Integer
    else:
        raise ValueError('Unexpected normalized column type: %s' % column.type)

    if no_constraints is False:
        if column.type is NoneType:
            sql_type_kwargs['length'] = NULL_COLUMN_MAX_LENGTH
        elif column.type is six.text_type:
            sql_type_kwargs['length'] = column.max_length()

        sql_column_kwargs['nullable'] = column.has_nulls()

    return Column(column.name, sql_column_type(**sql_type_kwargs), **sql_column_kwargs)

def get_connection(connection_string):
    engine = create_engine(connection_string)
    metadata = MetaData(engine)

    return engine, metadata

def make_table(csv_table, name='table_name', no_constraints=False, db_schema=None, metadata=None):
    """
    Creates a sqlalchemy table from a CSV Tools Table.
    """
    if not metadata:
        metadata = MetaData()

    sql_table = Table(csv_table.name, metadata, schema=db_schema)

    for column in csv_table:
        sql_table.append_column(make_column(column, no_constraints))

    return sql_table

def make_create_table_statement(sql_table, dialect=None):
    """
    Generates a CREATE TABLE statement for a sqlalchemy table.
    """
    if dialect:
        module = __import__('sqlalchemy.dialects.%s' % DIALECTS[dialect], fromlist=['dialect'])
        sql_dialect = module.dialect()
    else:
        sql_dialect = None

    return six.text_type(CreateTable(sql_table).compile(dialect=sql_dialect)).strip() + ';'