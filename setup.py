# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='dx2volca',
    version='0.1.0',
    description='Live translate dx7 dump for volca FM compatibility',
    long_description=readme,
    author='Alessio Degani',
    author_email='alessio.degani@gmail.com',
    url='https://github.com/adegani7dx2volca',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
