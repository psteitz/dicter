from setuptools import setup, find_packages

setup(
    name='dicter',
    version='0.1',
    packages=find_packages(exclude=['tests*']),
    license='Apache 2.0',
    description='A tool for analyzing datasets represented as lists of python dictionaries.',
    long_description=open('README.md').read(),
    install_requires=[],
    url='https://github.com/psteitz/dicter',
    author='Phil Steitz',
    author_email='phil@steitz.com'
)