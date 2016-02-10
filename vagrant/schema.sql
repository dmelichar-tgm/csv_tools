-- Autor: Dainel Melichar
-- Wien-Wahl (Gemeinderatswahl): Schema
-- 02.01.2016

DROP SCHEMA wien_wahl;
CREATE SCHEMA wien_wahl;

SET NAMES 'utf8';

DROP DATABASE IF EXISTS wien_wahl;
CREATE DATABASE wien_wahl;

-- ####################################################### --
-- ####################################################### --

-- LOGINS
-- User: wadmin
-- Password: password

GRANT ALL PRIVILEGES ON wien_wahl.* TO 'wadmin'@'localhost' IDENTIFIED BY 'password';
FLUSH PRIVILEGES;

USE wien_wahl;

-- ####################################################### --
-- ####################################################### --

CREATE TABLE wahl (
	termin DATE PRIMARY KEY,
	mandate INT NOT NULL	
);

-- ####################################################### --
-- ####################################################### --

CREATE TABLE wahlkreis (
	nummer INT PRIMARY KEY,
	name TEXT NOT NULL
);

-- ####################################################### --
-- ####################################################### --

CREATE TABLE partei (
	kbez	VARCHAR(5) PRIMARY KEY,
	lbez 	TEXT NOT NULL
);

-- ####################################################### --
-- ####################################################### --

CREATE TABLE bezik (
	nummer INT PRIMARY KEY,
	name TEXT NOT NULL,
	wahlkreis_nummer INT NOT NULL REFERENCES wahlkreis(nummer)
);

-- ####################################################### --
-- ####################################################### --

CREATE TABLE wahlsprengl (
	nummer INT NOT NULL,
	-- Ungueltige Stimmen
	ustimmen INT NOT NULL,
	-- Abgegebene Stimmen
	astimmen INT NOT NULL,
	berechtigt INT NOT NULL,
	bezirks_nummer INT REFERENCES bezirk(nummer),
	wahl_termin DATE REFERENCES wahl(termin),
	PRIMARY KEY (nummer, bezirks_nummer, wahl_termin)
);

-- ####################################################### --
-- ####################################################### --

CREATE TABLE kanidatur (
	listenplatz INT NOT NULL,
	partei_kbez VARCHAR(5) REFERENCES partei(kbez),
	wahlkreis_nummer INT REFERENCES wahlkreis(nummer),
	wahl_termin DATE REFERENCES wahl(termin),
	PRIMARY KEY (partei_kbez, wahlkreis_nummer, wahl_termin)
);

-- ####################################################### --
-- ####################################################### --

CREATE TABLE parteistimmen (
	-- Gesamt Stimmen
	gstimmen INT NOT NULL,
	partei_kbez VARCHAR(5) REFERENCES partei(kbez),
	wahlsprengl_nummer INT REFERENCES wahlsprengl(nummer),
	PRIMARY KEY (partei_kbez, wahlsprengl_nummer)
);

-- ####################################################### --
-- ####################################################### --



