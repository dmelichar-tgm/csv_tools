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

Query with SQL::

    insert --query "select snr from data where bezirk.name = 'Donaustadt'" test_data.csv > snr_22.csv

Import into PostgreSQL::

	insert --db postgresql://wadmin:password@localhost/wien_wahl  --insert examples/test_data.csv 

Print a CSV::
	
	lookat examples/test_data.csv


Resources and useful links
##########################



Aufgabenstellung (A08 - Python und CSV)
#######################################

Wir wollen nun unser Wissen wie Python mit CSV-Dateien umgeht.

Die Aufgabenstellung: Erstellen Sie ein einfaches Beispiel anhand der Wiener Gemeinderatswahl

- Einlesen eines CSV-Files (unterschiedlicher Dialekt) in den Hauptspeicher
- Einlesen eines CSV-Files (unterschiedlicher Dialekt) und an vorhandene Daten im Hauptspeicher anhängen
- Ausgeben von eingelesen Daten in ein CSV-File (unterschiedliche Dialekte)

Viel Erfolg!