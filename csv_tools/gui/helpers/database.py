#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
***************************
Database Management for GUI
***************************

This is currently only set up for MySQL
"""

import datetime
from sqlalchemy import create_engine
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

DATABASE = "wien_wahl"
USERNAME = "wadmin"
PASSWORD = "password"
WAHLTERMIN = "2015-10-11"

class DatabaseManager:

    def __init__(self):
        self.engine = create_engine("mysql+mysqldb://" + USERNAME + ":" + PASSWORD + "@localhost/" + DATABASE + "?charset=utf8")
        base = automap_base()
        base.prepare(self.engine, reflect=True)
        self.session = Session(self.engine)
        self.classes = base.classes

    def get_session(self):
        return self.session

    def get_raw_connection(self):
        return self.engine.raw_connection()

    def get_class(self, entity):
        return getattr(self.classes, entity)

    def write_from_csv_list(self, datalist):

        # TODO: REWRITE

        session = self.get_session()

        # delete previous data
        session.execute('DELETE FROM Stimmabgabe')
        session.execute("DELETE FROM Sprengel")
        session.execute("DELETE FROM Wahl")

        Wahl = self.get_class("Wahl")
        wahl = Wahl(termin=WAHLTERMIN, mandate=100)
        session.add(wahl)

        Sprengel = self.get_class("Sprengel")
        Stimmabgabe = self.get_class("Stimmabgabe")

        parties = []
        for key in datalist[0].keys():
            if key not in ["SPR", "BZ", "WBER", "ABG.", "UNG.", "T", "WV", "WK"]:
                parties.append(key)

        for line in datalist:
            sprengel = Sprengel(sprengelnr=int(line["SPR"]),
                                bezirknr=int(line["BZ"]),
                                termin=wahl.termin,
                                wahlberechtigte=int(line["WBER"]),
                                abgegebene=int(line["ABG."]),
                                ungueltige=int(line["UNG."]),
                                )
            session.add(sprengel)
            for party in parties:
                stimmabgabe = Stimmabgabe(sprengelnr=int(line["SPR"]),
                                          bezirknr=int(line["BZ"]),
                                          termin=wahl.termin,
                                          abkuerzung=party,
                                          anzahl=int(line[party])
                                          )
                session.add(stimmabgabe)

        session.commit()

    def load_into_csv_list(self):
        # TODO: REWRITE

        session = self.get_session()

        query = "SELECT Wahlkreis.wahlkreisnr, Bezirk.bezirknr, Sprengel.sprengelnr, Sprengel.wahlberechtigte, " \
                "Sprengel.abgegebene, Sprengel.ungueltige, Stimmabgabe.abkuerzung, Stimmabgabe.anzahl " \
                "FROM Wahlkreis " \
                "INNER JOIN Bezirk ON Wahlkreis.wahlkreisnr = Bezirk.wahlkreisnr " \
                "INNER JOIN Sprengel ON Bezirk.bezirknr = Sprengel.bezirknr " \
                "AND Sprengel.termin = '" + WAHLTERMIN + "' " \
                                                              "INNER JOIN Stimmabgabe ON Stimmabgabe.termin = '" + WAHLTERMIN + "' " \
                                                                                                                                     "AND Stimmabgabe.Bezirknr = Bezirk.bezirknr " \
                                                                                                                            "AND Stimmabgabe.sprengelnr = Sprengel.sprengelnr;"
        result = session.execute(query).fetchall()

        header = OrderedSet(["WK", "BZ", "SPR", "WBER", "ABG.", "UNG."])
        datalist = []
        line = {}
        first_party = None
        for i in range(0, len(result)):
            current_party = result[i]["abkuerzung"]
            if first_party is None or current_party == first_party:
                if line:
                    datalist.append(line)
                line = {}
                first_party = current_party
                line["WK"] = result[i]["wahlkreisnr"]
                line["BZ"] = result[i]["bezirknr"]
                line["SPR"] = result[i]["sprengelnr"]
                line["WBER"] = result[i]["wahlberechtigte"]
                line["ABG."] = result[i]["abgegebene"]
                line["UNG."] = result[i]["ungueltige"]
            line[current_party] = result[i]["anzahl"]
            header.add(current_party)

        return datalist, list(header)

    def create_results(self):

        termin = WAHLTERMIN
        zeitpunkt = datetime.now().time().strftime("%H:%M:%S")

        connection = self.get_raw_connection()
        cursor = connection.cursor()
        cursor.callproc("erzeugeHochrechnung", [termin, zeitpunkt])
        cursor.close()
        connection.commit()

        session = self.get_session()
        session.commit()
        query = "SELECT * FROM HRErgebnis WHERE termin = '" + termin + "' AND zeitpunkt = '" + zeitpunkt + "'"
        result = session.execute(query).fetchall()

        line = {}
        header = []
        datalist = []
        for i in range(0, len(result)):
            line[result[i]["abkuerzung"]] = result[i]["prozent"]
            header.append(result[i]["abkuerzung"])
        datalist.append(line)

        return datalist, header