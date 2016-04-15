#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
***************************
Database Management for GUI
***************************

This is currently only set up for MySQL
"""

import datetime

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy.util import OrderedSet

__author__ = "Daniel Melichar"
__copyright__ = "Copyright 2015"
__credits__ = ["Daniel Melichar"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Daniel Melichar"
__email__ = "dmelichar@student.tgm.ac.at"
__status__ = "Deployed"

class DatabaseManager:
    def __init__(self, connectionstring, electiondate):
        self.electiondate = electiondate
        self.engine = create_engine(connectionstring)
        self.conn = self.engine.connect()
        self.session = Session(self.engine)

        self.Base = automap_base()
        self.Base.prepare(self.engine, reflect=True)
        self.Election = self.Base.classes.election
        self.Constituency = self.Base.classes.constituency
        self.District = self.Base.classes.district
        self.JudicalDistrict = self.Base.classes.judicaldistrict
        self.Party = self.Base.classes.party
        self.Candidacy = self.Base.classes.candidacy
        self.Votes = self.Base.classes.votes
        self.TotalVotes = self.Base.classes.totalvotes
        self.Projection = self.Base.classes.projection
        self.ProjectionResult = self.Base.classes.projectionresult

        self.enr = first(self.session.query(self.Election.nr).filter(self.Election.dt == self.electiondate).all())
        if self.enr is None:
            raise Exception("Invalid election date")
        else:
            self.enr = self.enr[0]

    def close(self):
        self.conn.close()
        self.engine.dispose()

    def write(self, data):
        self.session.query(self.ProjectionResult).filter(self.ProjectionResult.enr == self.enr).delete(
            synchronize_session=False)
        self.session.query(self.Projection).filter(self.Projection.enr == self.enr).delete(synchronize_session=False)
        self.session.query(self.TotalVotes).filter(self.TotalVotes.enr == self.enr).delete(synchronize_session=False)
        self.session.query(self.Votes).filter(self.Votes.enr == self.enr).delete(synchronize_session=False)
        self.session.query(self.JudicalDistrict).filter(self.JudicalDistrict.enr == self.enr).delete(
            synchronize_session=False)

        parties = {}
        for key in data[0].keys():
            if key not in ["SPR", "BZ", "WBER", "ABG", "UNG", "T", "WV", "WK"]:
                parties[key] = self.session.query(self.Party.nr).filter(self.Party.abbr == key).first()[0]

        districts = []
        votes = []

        for line in data:
            districts.append(self.JudicalDistrict(
                enr=self.enr,
                dnr=int(line["BZ"]),
                nr=int(line["SPR"]),
                electivecnt=int(line["WBER"]),
                invalidcnt=int(line["UNG"]),
                votecnt=int(line["ABG"])
            ))
            for party, pnr in parties.items():
                votes.append(self.Votes(
                    enr=self.enr,
                    dnr=int(line["BZ"]),
                    jdnr=int(line["SPR"]),
                    pnr=pnr,
                    cnt=int(line[party])
                ))

        self.session.bulk_save_objects(districts)
        self.session.bulk_save_objects(votes)
        self.session.commit()

    def load(self):

        header = OrderedSet(["WK", "BZ", "SPR", "WBER", "ABG", "UNG"])
        parties = {}
        for party in self.session.query(self.Party).all():
            parties[party.nr] = party.abbr
            header.add(party.abbr)

        query = "SELECT constituency.nr AS cnr, district.nr AS dnr, judicaldistrict.nr AS jdnr, judicaldistrict.electivecnt, " \
                "judicaldistrict.votecnt, judicaldistrict.invalidcnt, votes.pnr, votes.cnt " \
                "FROM constituency " \
                "INNER JOIN district ON constituency.nr = district.cnr " \
                "INNER JOIN judicaldistrict ON district.nr = judicaldistrict.dnr " \
                "AND judicaldistrict.enr = '" + str(self.enr) + "' " \
                                                                "INNER JOIN votes ON votes.enr = '" + str(
            self.enr) + "' " \
                        "AND votes.dnr = district.nr " \
                        "AND votes.jdnr = judicaldistrict.nr;"
        result = self.session.execute(query)

        data = {}
        for row in result:
            key = str(row["cnr"]) + str(row["dnr"]) + str(row["jdnr"])
            if key not in data:
                data[key] = {
                    "WK": row["cnr"],
                    "BZ": row["dnr"],
                    "SPR": row["jdnr"],
                    "WBER": row["electivecnt"],
                    "ABG": row["votecnt"],
                    "UNG": row["invalidcnt"],
                    "T": 4,
                    "WV": 1,
                }
            data[key][parties[row["pnr"]]] = row["cnt"]

        return list(data.values())

    def create_projection(self):
        """
        Cudos an Rene Hollander
        """
        ts = datetime.datetime.now().time().strftime("%H:%M:%S")

        connection = self.engine.raw_connection()
        cursor = connection.cursor()
        cursor.callproc("create_projection", [self.enr, ts])
        cursor.close()
        connection.commit()
        self.session.commit()

        result = self.session.query(self.Party.abbr, self.ProjectionResult.percentage) \
            .select_from(self.Party).join(self.ProjectionResult, self.Party.nr == self.ProjectionResult.pnr) \
            .filter(self.ProjectionResult.enr == self.enr, self.ProjectionResult.ts == ts) \
            .all()
        data = {}
        for row in result:
            data[row.abbr] = float(row.percentage)
        return data

def first(the_iterable, condition=lambda x: True):
    for i in the_iterable:
        if condition(i):
            return i