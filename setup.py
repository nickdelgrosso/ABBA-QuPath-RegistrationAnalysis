from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.readlines()

setup(
    name='ABBA-QuPath-RegistrationExporter',
    version='0.1',
    packages=find_packages(),
    url='',
    license='MIT',
    author='nickdg',
    author_email='Nicholas A. Del Grosso',
    description='A QuPath-Abba Registration Exporter Application for Mouse Sections',
    install_requires=requirements,
    entry_points={'console_scripts':[
        "regexport=regexport.app:main"
    ]}
)
