set +e
PYTHONPATH=''
cd /home/vagrant/CSV-Tools
chmod -R 777 .
nosetests-3.4 --with-xunit --all-modules --traverse-namespace --with-coverage --cover-package=csv_tools --cover-inclusive
chmod -R 777 .
python3 -m coverage xml --include=csv_tools*
chmod -R 777 .
pylint -f parseable -d I0011,R0801 csv_tools
chmod -R 777 .