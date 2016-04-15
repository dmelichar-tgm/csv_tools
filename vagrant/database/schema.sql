DROP DATABASE IF EXISTS wienwahl;
CREATE DATABASE wienwahl;
USE wienwahl;

CREATE TABLE election (
  nr INTEGER AUTO_INCREMENT,
  dt DATE,
  seats INTEGER,
  PRIMARY KEY(nr)
);

CREATE TABLE constituency (
  nr INTEGER,
  name VARCHAR(64),
  PRIMARY KEY(nr)
);

CREATE TABLE district (
  nr INTEGER,
  cnr INTEGER,
  name VARCHAR(64),
  PRIMARY KEY(nr),
  FOREIGN KEY(cnr) REFERENCES constituency(nr)
);

CREATE TABLE party (
  nr INTEGER AUTO_INCREMENT,
  abbr VARCHAR(16),
  name VARCHAR(64),
  PRIMARY KEY(nr)
);

CREATE TABLE candidacy (
  pnr INTEGER,
  cnr INTEGER,
  enr INTEGER,
  listplace INTEGER,
  PRIMARY KEY(pnr, cnr, enr),
  FOREIGN KEY(pnr) REFERENCES party(nr),
  FOREIGN KEY(cnr) REFERENCES constituency(nr),
  FOREIGN KEY(enr) REFERENCES election(nr)
);

CREATE TABLE judicaldistrict (
  enr INTEGER,
  dnr INTEGER,
  nr INTEGER,
  electivecnt INTEGER,
  invalidcnt INTEGER,
  votecnt INTEGER,
  PRIMARY KEY(enr, dnr, nr),
  FOREIGN KEY(enr) REFERENCES election(nr),
  FOREIGN KEY(dnr) REFERENCES district(nr)
);

CREATE TABLE votes (
  enr INTEGER,
  dnr INTEGER,
  jdnr INTEGER,
  pnr INTEGER,
  cnt INTEGER,
  PRIMARY KEY(enr, dnr, jdnr, pnr),
  FOREIGN KEY(enr, dnr, jdnr) REFERENCES judicaldistrict(enr, dnr, nr),
  FOREIGN KEY(pnr) REFERENCES party(nr)
);

CREATE TABLE totalvotes (
  enr INTEGER,
  pnr INTEGER,
  cnt INTEGER,
  PRIMARY KEY(enr, pnr),
  FOREIGN KEY(enr) REFERENCES election(nr),
  FOREIGN KEY(pnr) REFERENCES party(nr)
);

CREATE TABLE projection (
  enr INTEGER,
  ts TIME,
  PRIMARY KEY(enr, ts),
  FOREIGN KEY(enr) REFERENCES election(nr)
);

CREATE TABLE projectionresult (
  enr INTEGER,
  pnr INTEGER,
  ts TIME,
  percentage REAL,
  PRIMARY KEY(enr, pnr, ts),
  FOREIGN KEY(enr) REFERENCES election(nr),
  FOREIGN KEY(pnr) REFERENCES party(nr),
  FOREIGN KEY(enr, ts) REFERENCES projection(enr, ts)
);

INSERT INTO election(dt, seats) VALUES('2015-10-11', 100);

INSERT INTO constituency(nr, name) VALUES(1, 'Wahlkreis Zentrum');
INSERT INTO constituency(nr, name) VALUES(2, 'Wahlkreis Innen-West');
INSERT INTO constituency(nr, name) VALUES(3, 'Wahlkreis Leopoldstadt');
INSERT INTO constituency(nr, name) VALUES(4, 'Wahlkreis Landstraße');
INSERT INTO constituency(nr, name) VALUES(5, 'Wahlkreis Favoriten');
INSERT INTO constituency(nr, name) VALUES(6, 'Wahlkreis Simmering');
INSERT INTO constituency(nr, name) VALUES(7, 'Wahlkreis Meidling');
INSERT INTO constituency(nr, name) VALUES(8, 'Wahlkreis Hietzing');
INSERT INTO constituency(nr, name) VALUES(9, 'Wahlkreis Penzing');
INSERT INTO constituency(nr, name) VALUES(10, 'Wahlkreis Rudolfsheim-Fünfhaus');
INSERT INTO constituency(nr, name) VALUES(11, 'Wahlkreis Ottakring');
INSERT INTO constituency(nr, name) VALUES(12, 'Wahlkreis Hernals');
INSERT INTO constituency(nr, name) VALUES(13, 'Wahlkreis Währing');
INSERT INTO constituency(nr, name) VALUES(14, 'Wahlkreis Döbling');
INSERT INTO constituency(nr, name) VALUES(15, 'Wahlkreis Brigittenau');
INSERT INTO constituency(nr, name) VALUES(16, 'Wahlkreis Floridsdorf');
INSERT INTO constituency(nr, name) VALUES(17, 'Wahlkreis Donaustadt');
INSERT INTO constituency(nr, name) VALUES(18, 'Wahlkreis Liesing');

INSERT INTO district(cnr, nr, name) VALUES(1, 1, 'Innere Stadt');
INSERT INTO district(cnr, nr, name) VALUES(3, 2, 'Leopoldstadt');
INSERT INTO district(cnr, nr, name) VALUES(4, 3, 'Landstraße');
INSERT INTO district(cnr, nr, name) VALUES(1, 4, 'Wieden');
INSERT INTO district(cnr, nr, name) VALUES(1, 5, 'Margareten');
INSERT INTO district(cnr, nr, name) VALUES(1, 6, 'Mariahilf');
INSERT INTO district(cnr, nr, name) VALUES(2, 7, 'Neubau');
INSERT INTO district(cnr, nr, name) VALUES(2, 8, 'Josefstadt');
INSERT INTO district(cnr, nr, name) VALUES(2, 9, 'Alsergrund');
INSERT INTO district(cnr, nr, name) VALUES(5, 10, 'Favoriten');
INSERT INTO district(cnr, nr, name) VALUES(6, 11, 'Simmering');
INSERT INTO district(cnr, nr, name) VALUES(7, 12, 'Meidling');
INSERT INTO district(cnr, nr, name) VALUES(8, 13, 'Hietzing');
INSERT INTO district(cnr, nr, name) VALUES(9, 14, 'Penzing');
INSERT INTO district(cnr, nr, name) VALUES(10, 15, 'Rudolfsheim-Fünfhaus');
INSERT INTO district(cnr, nr, name) VALUES(11, 16, 'Ottakring');
INSERT INTO district(cnr, nr, name) VALUES(12, 17, 'Hernals');
INSERT INTO district(cnr, nr, name) VALUES(13, 18, 'Währing');
INSERT INTO district(cnr, nr, name) VALUES(14, 19, 'Döbling');
INSERT INTO district(cnr, nr, name) VALUES(15, 20, 'Brigittenau');
INSERT INTO district(cnr, nr, name) VALUES(16, 21, 'Floridsdorf');
INSERT INTO district(cnr, nr, name) VALUES(17, 22, 'Donaustadt');
INSERT INTO district(cnr, nr, name) VALUES(18, 23, 'Liesing');

INSERT INTO party(abbr, name) VALUES('SPOE', 'Sozialdemokratische Partei Österreichs');
INSERT INTO party(abbr, name) VALUES('FPOE', 'Freiheitliche Partei Österreichs');
INSERT INTO party(abbr, name) VALUES('OEVP', 'Österreichische Volkspartei');
INSERT INTO party(abbr, name) VALUES('GRUE', 'Grüne Partei Österreichs');
INSERT INTO party(abbr, name) VALUES('NEOS', 'NEOS - Veränderung für Wien');
INSERT INTO party(abbr, name) VALUES('WWW', 'Wir Wollen Wahlfreiheit');
INSERT INTO party(abbr, name) VALUES('ANDAS', 'Wien anders');
INSERT INTO party(abbr, name) VALUES('GFW', 'Gemeinsam für Wien');
INSERT INTO party(abbr, name) VALUES('SLP', 'Sozialistische LinksPartei');
INSERT INTO party(abbr, name) VALUES('WIFF', 'Wir für Floridsdorf');
INSERT INTO party(abbr, name) VALUES('M', 'Männerpartei - für ein faires Miteinander');
INSERT INTO party(abbr, name) VALUES('FREIE', 'Freidemokraten');

INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(1,1,1,1);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(1,1,2,2);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(1,1,3,3);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(1,1,4,4);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(1,1,5,5);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(1,1,6,6);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(1,1,7,7);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(1,1,8,8);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(2,1,1,1);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(2,1,2,2);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(2,1,3,3);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(2,1,4,4);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(2,1,5,5);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(2,1,6,6);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(2,1,7,7);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(2,1,8,8);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(3,1,1,1);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(3,1,2,2);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(3,1,3,3);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(3,1,4,4);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(3,1,5,5);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(3,1,6,6);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(3,1,7,7);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(3,1,8,8);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(4,1,1,1);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(4,1,2,2);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(4,1,3,3);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(4,1,4,4);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(4,1,5,5);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(4,1,6,6);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(4,1,7,7);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(4,1,8,8);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(5,1,1,1);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(5,1,2,2);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(5,1,3,3);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(5,1,4,4);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(5,1,5,5);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(5,1,6,6);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(5,1,7,7);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(5,1,8,8);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(6,1,1,1);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(6,1,2,2);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(6,1,3,3);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(6,1,4,4);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(6,1,5,5);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(6,1,6,6);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(6,1,7,7);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(6,1,8,8);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(7,1,1,1);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(7,1,2,2);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(7,1,3,3);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(7,1,4,4);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(7,1,5,5);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(7,1,6,6);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(7,1,7,7);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(7,1,8,8);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(8,1,1,1);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(8,1,2,2);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(8,1,3,3);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(8,1,4,4);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(8,1,5,5);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(8,1,6,6);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(8,1,7,7);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(8,1,8,8);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(9,1,1,1);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(9,1,2,2);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(9,1,3,3);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(9,1,4,4);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(9,1,5,5);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(9,1,6,6);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(9,1,7,7);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(9,1,8,8);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(10,1,1,1);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(10,1,2,2);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(10,1,3,3);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(10,1,4,4);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(10,1,5,5);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(10,1,6,6);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(10,1,7,7);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(10,1,8,8);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(11,1,1,1);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(11,1,2,2);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(11,1,3,3);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(11,1,4,4);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(11,1,5,5);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(11,1,6,6);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(11,1,7,7);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(11,1,8,8);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(12,1,1,1);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(12,1,2,2);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(12,1,3,3);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(12,1,4,4);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(12,1,5,5);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(12,1,6,6);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(12,1,7,7);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(12,1,8,8);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(13,1,1,1);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(13,1,2,2);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(13,1,3,3);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(13,1,4,4);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(13,1,5,5);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(13,1,6,6);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(13,1,7,7);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(13,1,8,8);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(14,1,1,1);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(14,1,2,2);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(14,1,3,3);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(14,1,4,4);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(14,1,5,5);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(14,1,6,6);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(14,1,7,7);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(14,1,8,8);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(15,1,1,1);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(15,1,2,2);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(15,1,3,3);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(15,1,4,4);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(15,1,5,5);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(15,1,6,6);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(15,1,7,7);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(15,1,8,8);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(16,1,1,1);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(16,1,2,2);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(16,1,3,3);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(16,1,4,4);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(16,1,5,5);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(16,1,6,6);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(16,1,7,7);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(16,1,8,8);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(17,1,1,1);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(17,1,2,2);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(17,1,3,3);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(17,1,4,4);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(17,1,5,5);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(17,1,6,6);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(17,1,7,7);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(17,1,8,8);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(18,1,1,1);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(18,1,2,2);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(18,1,3,3);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(18,1,4,4);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(18,1,5,5);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(18,1,6,6);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(18,1,7,7);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(18,1,8,8);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(1,1,12,12);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(15,1,9,9);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(16,1,10,10);
INSERT INTO candidacy(cnr, enr, pnr, listplace) VALUES(17,1,11,11);
--
DELIMITER //
CREATE TRIGGER trigger_vote_insert AFTER INSERT ON votes FOR EACH ROW
BEGIN
	IF (SELECT enr FROM totalvotes WHERE enr = NEW.enr AND pnr = NEW.pnr) THEN
		UPDATE totalvotes SET cnt = cnt + NEW.cnt WHERE enr=NEW.enr AND pnr=NEW.pnr;
	ELSE
		INSERT INTO totalvotes VALUES(NEW.enr, NEW.pnr, NEW.pnr);
	END IF;
END;//
DELIMITER ;
--
DELIMITER //
CREATE TRIGGER trigger_vote_update AFTER UPDATE ON votes FOR EACH ROW
BEGIN
	UPDATE totalvotes SET cnt = cnt + (NEW.cnt - OLD.cnt) WHERE enr=NEW.enr AND pnr=NEW.pnr;
END;//
DELIMITER ;
--
DELIMITER //
CREATE TRIGGER trigger_vote_delete AFTER DELETE ON votes FOR EACH ROW
BEGIN
	UPDATE totalvotes SET cnt = cnt - OLD.cnt WHERE enr=OLD.enr AND pnr=OLD.pnr;
END;//
DELIMITER ;
--
DELIMITER //
CREATE PROCEDURE create_projection(IN enr INT, IN ts TIME)
BEGIN
	DECLARE totalVotes INT DEFAULT 0;
	DECLARE n INT DEFAULT 0;
	DECLARE i INT DEFAULT 0;
--
	INSERT INTO projection VALUES(enr, ts);
--
	SELECT SUM(cnt) FROM totalvotes INTO totalVotes;
	SELECT COUNT(*) FROM party INTO n;
	SET i=1;
	WHILE i<=n DO
		INSERT INTO projectionresult VALUES(enr, i, ts, COALESCE((SELECT cnt FROM totalvotes WHERE enr = enr AND pnr = i)/totalVotes * 100, 0));
		SET i = i + 1;
	END WHILE;
END; //
DELIMITER ;