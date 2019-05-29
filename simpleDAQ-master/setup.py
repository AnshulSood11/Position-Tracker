from setuptools import setup, find_packages

with open('README.rst') as f:
    long_description = f.read()

setup(name='simpleDAQ',
    version='0.1-alpha',
    description='Simple networked data acquisition system for sensors',
    author='Nick Touran',
    url='https://github.com/partofthething/simpleDAQ',
    packages=find_packages(),
    license='MIT',
    long_description=long_description,
    install_requires=['numpy', 'matplotlib'],
     )
