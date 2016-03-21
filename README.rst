*********
CSV-Tools
*********

**Developer:** Daniel Melichar

**Class:** 5AHITM


Requirements
############

It is recommended to use the provided Virtual Development Environment for the entire project. For this, the only requirements you have is a functional **vagrant** installation as well as **XQuartz** if you're on OSX.
You can set up PyCharm to use the virtual machine's interpreter, see `here <https://www.jetbrains.com/pycharm/help/configuring-remote-python-interpreters.html>`_.

However, if you want to run everything locally, see requirements below.

You will need a functional **Python3** installation. Using a `VirtualEnv <http://docs.python-guide.org/en/latest/dev/virtualenvs/>`_ is never wrong. You will also need to install the requirements via pip, see in Installation.

For the Jenkins part, you'll need a functional Vagrant installation.

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


Usage (GUI)
###########

.. image:: gui-screenshot.png
   :alt: gui-screenshot
   :align: center


Usage (Terminal)
################

After a succsesfull installation, you will be able to use the three main services provided by CSV-Tools: **lookat**, **convert**, and **insert** CSVs.

You can use these services by simply typing them into the console, i.e. use *lookat --help*

For a more detailed documentation, see the doc folder with the Sphinx documentation (use *make html*).



**Some examples**

Convert Excel to CSV:

    convert data.xls > data.csv

Convert a badly formatted CSV to a well formated CSV:

    convert data.csv

Query with SQL:

    insert --query "select snr from data where bezirk.name = 'Donaustadt'" test_data.csv > snr_22.csv

Import into PostgreSQL:

    insert --db postgresql://wadmin:password@localhost/wien_wahl  --insert examples/test_data.csv

Print a CSV:

    lookat examples/test_data.csv


Virtual Development Environment (with Jenkins)
##############################################

Go to the vagrant directory and type:

    vagrant up

This will install and configure the machine. After that, Jenkins will be available at **127.0.0.0:8080**.
You can access `Vagrant <https://www.vagrantup.com/docs/>`_ with the typical commands and use it as needed.

The entire Vagrantfile is setup in a way which allows for you to only use it and not any interpreters you have on your host.
In a nutshell, after the Vagrant is initialized and while it's running, connect to it with *vagrant ssh*, then you just have to run the program.

To test if everything is working properly type in the following commands (while in the vagrant directory):

    # Connect to the server
    
    vagrant ssh
    
    
    # Open the 'Hello World' window
    
    /usr/bin/python3 /home/vagrant/CSV-Tools/vagrant/HelloWorld-PySide.py


Please note that some modifications may be needed in the *Vagrantfile* and *install.sh* Script - especially the Paths. 


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
- Jenkins: `Wiki <https://wiki.jenkins-ci.org/display/JENKINS/Home>`_
- bhfsteve: `Automated python unit testing, code coverage and code quality analysis with Jenkins <http://bhfsteve.blogspot.co.at/2012/04/automated-python-unit-testing-code.html>`_
- Mark Summerfiled: `Rapid GUI Programming with Python and Qt <https://www.cs.washington.edu/research/projects/urbansim/books/pyqt-book.pdf>`_
- Qt Wiki: `PySide Binaries MacOSX <https://wiki.qt.io/PySide_Binaries_MacOSX>`_
- Martin (Coderwall): `Run graphical programs within Vagrantboxes <https://coderwall.com/p/ozhfva/run-graphical-programs-within-vagrantboxes>`_


Aufgabenstellungen 
##################

**#1 (A08 - Python und CSV)**

Wir wollen nun unser Wissen wie Python mit CSV-Dateien umgeht.

Die Aufgabenstellung: Erstellen Sie ein einfaches Beispiel anhand der Wiener Gemeinderatswahl

- Einlesen eines CSV-Files (unterschiedlicher Dialekt) in den Hauptspeicher
- Einlesen eines CSV-Files (unterschiedlicher Dialekt) und an vorhandene Daten im Hauptspeicher anhängen
- Ausgeben von eingelesen Daten in ein CSV-File (unterschiedliche Dialekte)

Viel Erfolg!

**#2 (A10 - Continuous Integration)**

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

**#3 (INSY: GUI-Struktur)**

Erstelle eine GUI-Basis-Struktur lt. `Tafelbild <https://elearning.tgm.ac.at/pluginfile.php/66538/mod_label/intro/20160210_083641.jpg>`_

Erweitere die Menüeinträge mittel QActions (derzeit nur Dummy-Methoden)

Mittels Crtl-Q wird das Programm verlassen (mittels Qt Designer im SIgnal/Slot-Editor festlegen)

Abgabe: 3 Files

.ui-file;

converted .py

ausführbare Klasse, welche das converted .py verwendet und das Fenster anzeigbar macht.

**#4 UNDO/REDO-FUNKTIONALITÄT**

1 Erstellen Sie folgende Aktionen:

    - Kopieren (einer Zelle)
    - Einfügen (einer Zelle)
    - Auschneiden (des Inhalts einer Zelle)
    - Erzeugen einer neuen Zeile (unterhalb der aktuellen Zelle)
    - Duplizieren der aktuellen Zeile (inklusive einfügen unterhalb der aktuellen Zelle)
    - Löschen der aktuellen Zeile
    - Undo (letzte Aktion rückgängig machen)
    - Redo (letzte verfügbare Aktion wiederholen)

2. Erstelle Sie eine History aller Kommandos.

3. Verbinden Sie die Aktionen mit dem Menü

4. Einbindung des TableModels

5. Einbinden des Data Access Layer(DAL)

6. Testen Sie die Funktionalität

7. Geben Sie alle notwendigen Pythonfiles (inklusive Verzeichnisstruktur) in einem Archiv (.zip) ab.

Viel Erfolg!
