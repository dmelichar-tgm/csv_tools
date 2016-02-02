*********
CSV-Tools
*********

**Developer:** Daniel Melichar

**Class:** 5AHITM


Requirements
############

You will need a functional **Python3** installation. Using a `VirtualEnv <http://docs.python-guide.org/en/latest/dev/virtualenvs/>`_ is never wrong.


Installation
############

1. Clone this repo::

	git clone https://www.github.com/dmelichar-tgm/csv_tools

2. Create a Python virtual environment using virtualenvwrapper (optional, but recommended)::

	mkvirtualenv --python=python3 ~/.virtualenvs/csv_tools
	source ~/.virtualenvs/csv_tools/bin/activate


3. Install requirements::

	pip install -r requirements.txt

4. Execute the setup.py::

	python setup.py install

Usage
#####

After a succsesfull installation, you will be able to use the three main services provided by CSV-Tools: **lookat**, **convert**, and **insert** CSVs.

You can use these services by simply typing them into the console, i.e. use *lookat --help*

For a more detailed documentation, see the doc folder with the Sphinx documentation (use *make html*).



**Some examples**

Convert Excel to CSV::

    convert data.xls > data.csv

Convert a badly formatted CSV to a well formated CSV::

    convert data.csv

Query with SQL::

    insert --query "select snr from data where bezirk.name = 'Donaustadt'" test_data.csv > snr_22.csv

Import into PostgreSQL::

	insert --db postgresql://wadmin:password@localhost/wien_wahl  --insert examples/test_data.csv 

Print a CSV::
	
	lookat examples/test_data.csv


Resources and useful links
##########################

- Tshepang Lekhonkhobe: `Argparse Tutorial <https://docs.python.org/3/howto/argparse.html>`_
- PythonProgramming.net: `Reading CSV Files in Python <https://pythonprogramming.net/reading-csv-files-python-3/>`_
- Python Software Foundation: `CSV Documentation <https://docs.python.org/3/library/csv.html>`_
- Python Software Foundation: `Building and Distributing Packages with Setuptools <https://pythonhosted.org/setuptools/setuptools.html>`_
- CSVKit: `Documentation <https://csvkit.readthedocs.org/en/0.9.1/>`_
- OpenPyXL: `Documentation <https://openpyxl.readthedocs.org/en/2.3.3/>`_
- Stackoverflow (Various): `Custom exceptions in Python <https://stackoverflow.com/questions/1319615/proper-way-to-declare-custom-exceptions-in-modern-python>`_
- Six: `Documentation <https://pythonhosted.org/six/>`_


Aufgabenstellung #1 (A08 - Python und CSV)
##########################################

Wir wollen nun unser Wissen wie Python mit CSV-Dateien umgeht.

Die Aufgabenstellung: Erstellen Sie ein einfaches Beispiel anhand der Wiener Gemeinderatswahl

- Einlesen eines CSV-Files (unterschiedlicher Dialekt) in den Hauptspeicher
- Einlesen eines CSV-Files (unterschiedlicher Dialekt) und an vorhandene Daten im Hauptspeicher anhängen
- Ausgeben von eingelesen Daten in ein CSV-File (unterschiedliche Dialekte)

Viel Erfolg!



Aufgabenstellung #2 (A10 - Continuous Integration)
##################################################

*"Continuous Integration is a software development practice where members of a team integrate their work frequently, usually each person integrates at least daily - leading to multiple integrations per day. Each integration is verified by an automated build (including test) to detect integration errors as quickly as possible. Many teams find that this approach leads to significantly reduced integration problems and allows a team to develop cohesive software more rapidly. This article is a quick overview of Continuous Integration summarizing the technique and its current usage." M.Fowler*

Schreibe fünf Testfälle für dein CSV-Projekt und lass diese mithilfe von Jenkins automatisch bei jedem Build testen!

- Installiere auf deinem Rechner bzw. einer virtuellen Instanz das Continuous Integration System Jenkins
- Installiere die notwendigen Plugins für Jenkins (Git Plugin, Violations, Cobertura)
- Installiere Nose und Pylint (mithilfe von pip)
- Integriere dein CSV-Projekt in Jenkins, indem du es mit Git verbindest
- Schreibe fünf Unit Tests für dein CSV-Projekt
- Konfiguriere Jenkins so, dass deine Unit Tests automatisch bei jedem Build durchgeführt werden inkl. Berichte über erfolgreiche / fehlgeschlagene Tests und Coverage
- Protokolliere deine Vorgehensweise (inkl. Zeitaufwand, Konfiguration, Probleme) und die Ergebnisse (viele Screenshots!)

Viel Spaß!
