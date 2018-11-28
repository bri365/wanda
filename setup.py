
from setuptools import find_packages, setup

setup(
    name='wandapi',
    version='0.0.1',
    description='Bluewand REST API Server',
    author='Brian J Martin',
    author_email='bri365@gmail.com',
    packages=find_packages(exclude=['*.tests', '*.tests.*']),
    install_requires=[
        'eventlet',
        'falcon'
    ],
    test_suite='tests',
    zip_safe=False
)
