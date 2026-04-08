import os
from setuptools import setup, find_packages

install_requires = []
with open('requirements.txt') as reqs:
    for line in reqs.readlines():
        req = line.strip()
        if not req or req.startswith('#'):
            continue
        install_requires.append(req)

setup(
    name='orangebook',
    description='X-ray Data Booklet (orange book) binding energies and Phi XPS databook ',
    url='https://github.com/apsIEX/orangebook',
    maintainer='Jessica McChesney; Amitayush Jha Thakur',
    maintainer_email='jmcchesn@anl.gov; ajhathakur@anl.gov',
    version='1.0',
    packages=find_packages(),
    install_requires=install_requires,
    scripts=[],
    dependency_links=[],
    package_data={'': ['PHI_XPS/*.tiff','orangebook_BE.csv','orangebook_EE.csv','electron_configurations.csv,oxidation_states.csv','interpolated_results/*.csv']}

)

