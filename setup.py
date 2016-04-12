from setuptools import setup

# TODO: what are python modules..

import sys, os
sys.path.append(os.path.realpath(__file__))


setup(
    name='CSV-Tools',
    version='0.0.1',
    packages=['csv_tools', 'csv_tools.convert', 'csv_tools.services', 'csv_tools.gui'],
    url='www.github.com/dmelichar-tgm/csv_tools',
    license='GPL',
    author='Daniel Melichar',
    author_email='dmelichar@student.tgm.ac.at',
    description='Some CSV Tools that will help with the next assignment',
    long_description=open('README.rst').read(),
    entry_points ={
        'console_scripts': [
            'lookat = csv_tools.services.look_at_csv:launch_new_instance',
            'insert = csv_tools.services.insert_csv:launch_new_instance',
            'convert = csv_tools.services.convert_to_csv:launch_new_instance',
            'csvtools = csv_tools.gui:launch_new_instance'
        ]
    }
)
