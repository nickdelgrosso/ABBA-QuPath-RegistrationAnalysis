from setuptools import setup, find_packages

long_description = """
# ABBA-QuPath Registration Exporter

A Python app and Groovy script that helps export transformed cell detections
from ABBA-registered data stored in QuPath projects.

## Installation

```
pip install ABBA-QuPath-RegistrationExporter
```

## Running

```
regexport
```
"""

setup(
    name='ABBA-QuPath-RegistrationExporter',
    version='0.2.1',
    packages=find_packages(),
    url='',
    license='MIT',
    author='Nicholas A. Del Grosso and Estelle Nassar',
    author_email='delgrosso.nick@gmail.com',
    description='A QuPath-Abba Registration Exporter Application for Mouse Sections',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        'numpy~=1.21.2',
        'matplotlib~=3.4.3',
        'pandas~=1.3.2',
        'qtpy~=1.11.0',
        'vtk~=9.0.3',
        'vedo~=2021.0.5',
        'pyqt5~=5.15.4',
        'treelib~=1.6.1',
        'traitlets~=5.1.0',
        'bg-atlasapi',
        'pyarrow',
    ],
    extras_require={
        'dev': [ # to include as dev, try pip install -e .[dev]
            'pytest_runner',
            'pytest',
            'pytest-bdd',
            'coverage',
            # 'pytest-qt',
            ],
    },
    entry_points={'console_scripts':[
        "regexport=regexport.main:main"
    ]},
    package_data={
        'regexport': ['qupath_scripts/*.groovy'],
    }
)
